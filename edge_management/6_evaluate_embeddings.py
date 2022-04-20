import argparse
import csv
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_distances

import weat

from config import (
    ORIGINAL_NUMBERBATCH_EN_HDF,
    ORIGINAL_NUMBERBATCH_EN_DIM50_HDF,
    RETROFITTED_HDF,
    RETROFITTED_DIM50_HDF,
    ADDITIONAL_EDGES_RETROFIT_CSV,
    STEREOSET_TERMS,
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
    return score

# TODO: p score in the WEAT paper


def run_weat_test(targets, attributes, numberbatch_embeddings, retrofitted_embeddings):
    original_weat_score = get_weat_score(targets, attributes, numberbatch_embeddings)
    retrofitted_weat_score = get_weat_score(targets, attributes, retrofitted_embeddings)

    print('WEAT evaluation')
    print(f'targets:\n {targets[0][:]}\n vs. \n {targets[1][:]}')
    print(f'attributes:\n {attributes[0][:]}\n vs. \n {attributes[1][:]}')
    print(f'scores:\n original: {original_weat_score}\n retrofitted: {retrofitted_weat_score}')


def analysis(reduced_dimension=False):
    numberbatch_file = ORIGINAL_NUMBERBATCH_EN_HDF
    retrofitted_file = RETROFITTED_HDF

    if reduced_dimension:
        numberbatch_file = ORIGINAL_NUMBERBATCH_EN_DIM50_HDF
        retrofitted_file = RETROFITTED_DIM50_HDF

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

    # Word Embedding Association Test Demo
    run_weat_test(targets=GENDER,
                  attributes=DEMO_PROFESSION,
                  numberbatch_embeddings=numberbatch_df_touched,
                  retrofitted_embeddings=retrofitted_df_touched)
    # TODO: add more tests here



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

    args = parser.parse_args()

    analysis(args.dimension50)
