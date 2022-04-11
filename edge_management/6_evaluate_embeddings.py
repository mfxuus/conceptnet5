import argparse
import pandas as pd

from config import ORIGINAL_NUMBERBATCH_EN_HDF, ORIGINAL_NUMBERBATCH_EN_DIM50_HDF, RETROFITTED_HDF, RETROFITTED_DIM50_HDF


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

    print(numberbatch_df)
    print(retrofitted_df)


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
