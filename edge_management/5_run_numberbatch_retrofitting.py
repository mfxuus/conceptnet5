import argparse
import pandas as pd
from sklearn.decomposition import PCA

from conceptnet5.vectors import retrofit, evaluation, formats

from config import ORIGINAL_NUMBERBATCH_EN, ADDITIONAL_EDGES_CSV, ORIGINAL_NUMBERBATCH_EN_HDF, ORIGINAL_NUMBERBATCH_EN_DIM50_HDF, RETROFITTED_HDF, RETROFITTED_DIM50_HDF


def create_hdf_data(reduced_dimension=False):
    '''
    Data available at:
    https://github.com/commonsense/conceptnet-numberbatch
    and
    https://zenodo.org/record/4911598
    and
    https://zenodo.org/record/4916056
    '''
    df = pd.read_csv(ORIGINAL_NUMBERBATCH_EN, sep=" ", index_col=0, skiprows=[0], header=None)
    df = df[df.index.notnull()]
    if reduced_dimension:
        pca = PCA(n_components=50)
        pca.fit(df.T)
        df_pca = pd.DataFrame(pca.components_.T, index=df.index)
        print(df_pca)
        df_pca.to_hdf(ORIGINAL_NUMBERBATCH_EN_DIM50_HDF, 'mat', mode='w', format='table', encoding='utf-8')
    print(df)
    df.to_hdf(ORIGINAL_NUMBERBATCH_EN_HDF, 'mat', mode='w', format='table', encoding='utf-8')
    print('HDF file crated.')


def apply_retrofitting(reduced_dimension, nshards=1):
    '''
    https://github.com/mfxuus/conceptnet5/blob/master/conceptnet5/vectors/retrofit.py
    '''
    """
    Quote:
    Retrofitting is a process of combining information from a machine-learned
    space of term vectors with further structured information about those
    terms. It was originally presented in this 2015 NAACL paper by Manaal
    Faruqui, Jesse Dodge, Sujay Jauhar, Chris Dyer, Eduard Hovy, and Noah
    Smith, "Retrofitting Word Vectors to Semantic Lexicons":
    
        https://www.cs.cmu.edu/~hovy/papers/15HLT-retrofitting-word-vectors.pdf
    
    This function implements a variant that I've been calling "wide
    retrofitting", which extends the process to learn vectors for terms that
    were outside the original space.
    
    `row_labels` is the list of terms that we want to have vectors for.
    
    `dense_frame` is a DataFrame assigning vectors to some of these terms.
    
    `sparse_csr` is a SciPy sparse square matrix, whose rows and columns are
    implicitly labeled with `row_labels`. The entries of this matrix are
    positive for terms that we know are related from our structured data.
    (This is an awkward form of input, but unfortunately there is no good
    way to represent sparse labeled data in Pandas.)
    
    `sharded_retrofit` is responsible for building `row_labels` and `sparse_csr`
    appropriately.
    """
    dense_hdf_filename = ORIGINAL_NUMBERBATCH_EN_HDF
    #TODO: I only used additional edges
    conceptnet_filename = ADDITIONAL_EDGES_CSV
    output_filename = RETROFITTED_HDF

    if reduced_dimension:
        dense_hdf_filename = ORIGINAL_NUMBERBATCH_EN_DIM50_HDF
        output_filename = RETROFITTED_DIM50_HDF

    retrofit.sharded_retrofit(dense_hdf_filename=dense_hdf_filename,
                              conceptnet_filename=conceptnet_filename,
                              output_filename=output_filename,
                              nshards=nshards)
    retrofit.join_shards(output_filename, nshards)
    print('Retrofitting done.')


if __name__ == '__main__':
    '''
    python 5_run_numberbatch.py
    python 5_run_numberbatch.py --dimension50 --from-txt
    '''

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--dimension50',
        action='store_true',
        default=False,
        help='Use data with reduced dimension of 50.',
    )
    parser.add_argument(
        '--from-txt',
        action='store_true',
        default=False,
        help='Build hdf files first.',
    )
    parser.add_argument(
        '--nshards',
        type=int,
        help='Number of shards'
    )

    args = parser.parse_args()

    if args.from_txt:
        create_hdf_data(args.dimension50)
    apply_retrofitting(args.dimension50, int(args.nshards))