import os
PROJECT_DIR = 'E:\\3_Courses\\conceptnet5\\'
SUBPROJECT_DIR = os.path.join(PROJECT_DIR, 'edge_management')
LOCAL_DATA_DIR = os.path.join(SUBPROJECT_DIR, 'local_data')
# Set to False if we only keep ENGLISH nodes (in the gml file)
ALL_LANGUAGES = False


# If we want to override any values above
from local_config import *




# Input file
# each line: node_1, node_2, relation type, weight
ADDITIONAL_EDGES_INPUT = os.path.join(SUBPROJECT_DIR, 'new_edges.txt')
# where we save the new assertions (output and formatted by script)
ADDITIONAL_EDGES_CSV = os.path.join(LOCAL_DATA_DIR, 'new_assertions.csv')
ADDITIONAL_EDGES_RETROFIT_CSV = os.path.join(LOCAL_DATA_DIR, 'new_assertions_retrofit.csv')
# where you've downloaded the assertions file
ORIGINAL_CSV = os.path.join(LOCAL_DATA_DIR, 'assertions.csv')
# ORIGINAL_NUMBERBATCH_ZIP = os.path.join(LOCAL_DATA_DIR, 'numberbatch-19.08-en.zip')
# ORIGINAL_NUMBERBATCH_DIM50_ZIP = os.path.join(LOCAL_DATA_DIR, 'numberbatch-19.08-en-pca-50.zip')
RETROFITTED_HDF = os.path.join(LOCAL_DATA_DIR, 'retrofitted.h5')
RETROFITTED_DIM50_HDF = os.path.join(LOCAL_DATA_DIR, 'retrofitted-pca-50.h5')
ORIGINAL_NUMBERBATCH_EN = os.path.join(LOCAL_DATA_DIR, 'numberbatch-en.txt')
ORIGINAL_NUMBERBATCH_EN_HDF = os.path.join(LOCAL_DATA_DIR, 'numberbatch-en.h5')
ORIGINAL_NUMBERBATCH_EN_DIM50_HDF = os.path.join(LOCAL_DATA_DIR, 'numberbatch-en-pca-50.h5')

VALID_RELATIONS = [
    '/r/Entails', '/r/Causes', '/r/Desires', '/r/dbpedia/leader',
    '/r/dbpedia/product', '/r/MadeOf', '/r/DefinedAs', '/r/HasContext',
    '/r/CapableOf', '/r/NotDesires', '/r/MotivatedByGoal', '/r/dbpedia/field',
    '/r/HasSubevent', '/r/HasLastSubevent', '/r/MannerOf', '/r/HasPrerequisite',
    '/r/ObstructedBy', '/r/Synonym', '/r/dbpedia/occupation',
    '/r/dbpedia/genre', '/r/SimilarTo', '/r/FormOf', '/r/DistinctFrom',
    '/r/CreatedBy', '/r/PartOf', '/r/AtLocation', '/r/EtymologicallyRelatedTo',
    '/r/dbpedia/genus', '/r/HasFirstSubevent', '/r/ExternalURL',
    '/r/DerivedFrom', '/r/LocatedNear', '/r/NotCapableOf', '/r/UsedFor',
    '/r/dbpedia/language', '/r/HasProperty', '/r/CausesDesire',
    '/r/ReceivesAction', '/r/InstanceOf', '/r/IsA', '/r/HasA',
    '/r/NotHasProperty', '/r/dbpedia/influencedBy', '/r/Antonym',
    '/r/NotUsedFor', '/r/SymbolOf', '/r/dbpedia/capital', '/r/RelatedTo',
    '/r/dbpedia/knownFor', '/r/EtymologicallyDerivedFrom'
]
