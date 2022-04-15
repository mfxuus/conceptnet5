import argparse
import csv
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_distances

from config import (
    ORIGINAL_NUMBERBATCH_EN_HDF,
    ORIGINAL_NUMBERBATCH_EN_DIM50_HDF,
    RETROFITTED_HDF,
    RETROFITTED_DIM50_HDF,
    ADDITIONAL_EDGES_RETROFIT_CSV
)


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
