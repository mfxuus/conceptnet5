import argparse
import csv
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_distances
from sklearn.neighbors import NearestNeighbors

import weat

from config import (
    ORIGINAL_NUMBERBATCH_EN_HDF,
    # ORIGINAL_NUMBERBATCH_EN_DIM50_HDF,
    RETROFITTED_HDF,
    # RETROFITTED_DIM50_HDF,
    ADDITIONAL_EDGES_RETROFIT_CSV,
    ADDITIONAL_EDGES_INPUT,
    STEREOSET_TERMS,
    KGC_RETROFITTED_HDF,
)

GENDER = [t[:12] for t in STEREOSET_TERMS['gender']]  # some gender terms are not touched.
DEMO_PROFESSION = [['ceo'], ['assistant']]

# TODO: Add your own test terms here.


def get_touched_nodes():
    nodes = set()
    with open(ADDITIONAL_EDGES_RETROFIT_CSV, 'r', encoding="utf8") as r_file:
        datareader = csv.reader(r_file, delimiter='\t')
        for row in datareader:
            nodes.add(row[0])
            nodes.add(row[1])
    nodes = list(nodes)
    print(f'Number of touched nodes: {len(nodes)}')
    return nodes


def get_edges():
    """Returns an adjacency graph of words and their edges."""
    ret = {}
    with open(ADDITIONAL_EDGES_INPUT, 'r') as f:
            for line in f:
                node_1, node_2, rel_type, weight = [x.strip() for x in line.split(',')]
                node_1 = node_1.strip().lower().replace(' ', '_')
                node_2 = node_2.strip().lower().replace(' ', '_')
                if node_1 not in ret:
                    ret[node_1] = set()
                ret[node_1].add(node_2)
                if node_2 not in ret:
                    ret[node_2] = set()
                ret[node_2].add(node_1)
    return ret


def load_embedding(file):
    df = pd.read_hdf(file, 'mat', encoding='utf_8')
    df = df[df.index.notnull()]
    return df


# Word Embedding Association Test
def get_weat_score(targets, attributes, embeddings):
    # only get existing indices
    targets = [embeddings.index.intersection(targets[i]) for i in range(len(targets))]
    attributes = [embeddings.index.intersection(attributes[i]) for i in range(len(attributes))]

    # TODO: (Maybe) random drop if dimension is not the same
    # assert(len(targets[0]) == len(targets[1]))
    # assert(len(attributes[0]) == len(attributes[1]))

    target1 = embeddings.loc[targets[0]].to_numpy()
    target2 = embeddings.loc[targets[1]].to_numpy()

    attribute1 = embeddings.loc[attributes[0]].to_numpy()
    attribute2 = embeddings.loc[attributes[1]].to_numpy()

    score = weat.weat_differential_association(target1, target2, attribute1, attribute2)
    # p = weat.weat_p_value(target1, target2, attribute1, attribute2)
    return score

# TODO: p score in the WEAT paper


 # K-nn 
def get_knn(target_word, k, old_embeddings, new_embeddings, edges):
    """Returns a list of words which are the k nearest neighbours to the target word, sorted by distance."""
    # only get existing indices
    target_emb = old_embeddings.loc[target_word].to_numpy().reshape(1, -1)
    nbrs = NearestNeighbors(n_neighbors=k+1, algorithm='ball_tree').fit(old_embeddings)
    distances, old_indices = nbrs.kneighbors(target_emb)

    target_emb = new_embeddings.loc[target_word].to_numpy().reshape(1, -1)
    nbrs = NearestNeighbors(n_neighbors=k+1, algorithm='ball_tree').fit(new_embeddings)
    distances, new_indices = nbrs.kneighbors(target_emb)

    old_neighbours = old_embeddings.iloc[old_indices[0]].copy().iloc[1:]
    old_neighbours = list(old_neighbours.index)
    new_neighbours = new_embeddings.iloc[new_indices[0]].copy().iloc[1:]
    new_neighbours = list(new_neighbours.index)
    print(f"K-NN for {target_word}")
    # print("Old:", old_neighbours)
    # print("New:", new_neighbours)

    print("New terms found:", [n for n in new_neighbours if n not in edges[target_word] and n not in old_neighbours])


def run_weat_test(targets, attributes, numberbatch_embeddings, retrofitted_embeddings):
    original_weat_score = get_weat_score(targets, attributes, numberbatch_embeddings)
    retrofitted_weat_score = get_weat_score(targets, attributes, retrofitted_embeddings)

    print('WEAT evaluation')
    print(f'targets:\n {targets[0][:]}\n vs. \n {targets[1][:]}')
    print(f'attributes:\n {attributes[0][:]}\n vs. \n {attributes[1][:]}')
    print(f'scores:\n original: {original_weat_score}\n retrofitted: {retrofitted_weat_score}')
    # print(f'p values:\n original: {original_weat_p}\n retrofitted: {retrofitted_weat_p}')

def analysis(reduced_dimension=False, from_kgc=False):
    numberbatch_file = ORIGINAL_NUMBERBATCH_EN_HDF
    retrofitted_file = RETROFITTED_HDF

    # if reduced_dimension:
    #     numberbatch_file = ORIGINAL_NUMBERBATCH_EN_DIM50_HDF
    #     retrofitted_file = RETROFITTED_DIM50_HDF
    if from_kgc:
        retrofitted_file = KGC_RETROFITTED_HDF

    numberbatch_df = load_embedding(numberbatch_file)
    retrofitted_df = load_embedding(retrofitted_file)

    print('numberbatch_df')
    print(numberbatch_df)
    print('retrofitted_df')
    print(retrofitted_df)

    touched_nodes = get_touched_nodes()
    numberbatch_df_touched = numberbatch_df[numberbatch_df.index.isin(touched_nodes)]
    retrofitted_df_touched = retrofitted_df[retrofitted_df.index.isin(touched_nodes)]

    # first len(numberbatch_df_touched) rows of each df are the same
    # (retrofit may have additional rows, which we will ignore)
    retrofitted_df_touched = retrofitted_df_touched[:len(numberbatch_df_touched)]
    # sanity check (orders of rows)
    assert np.all(retrofitted_df_touched.index == numberbatch_df_touched.index)
    distance_mat = cosine_distances(numberbatch_df_touched, retrofitted_df_touched)
    # take diagonal
    distance_arr = pd.Series(np.diag(distance_mat), index=[numberbatch_df_touched.index])

    distance_arr.sort_values(inplace=True)
    print('Top cosine_distances:')
    print(distance_arr[-20:])
    print('Lowest cosine_distances:')
    print(distance_arr[:20])

    # Find the knn of the words with the lowest 10 cosine distances
    print()
    edges = get_edges()
    for word in distance_arr[:20].index:
        get_knn(word[0], 30, numberbatch_df_touched, retrofitted_df_touched, edges)
        print()
    print()

    # Word Embedding Association Test Demo
    run_weat_test(targets=GENDER,
                  attributes=DEMO_PROFESSION,
                  numberbatch_embeddings=numberbatch_df_touched,
                  retrofitted_embeddings=retrofitted_df_touched)
    # TODO: add more tests here
    run_weat_test(targets=GENDER,
                  attributes=[['scientist', 'researcher', 'professor', 'academic'],
                              ['performing_artist', 'tailor', 'musician', 'guitarist']],
                  numberbatch_embeddings=numberbatch_df_touched,
                  retrofitted_embeddings=retrofitted_df_touched)


if __name__ == '__main__':
    '''
    python 6_evaluate_embeddings.py
    python 6_evaluate_embeddings.py --dimension50
    '''

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--dimension50',
        action='store_true',
        default=False,
        help='Use data with reduced dimension of 50.',
    )
    parser.add_argument(
        '--from-kgc',
        action='store_true',
        default=False,
        help='From knowledge graph completion edges',
    )

    args = parser.parse_args()

    analysis(args.dimension50, from_kgc=args.from_kgc)
