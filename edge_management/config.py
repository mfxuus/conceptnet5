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

STEREOSET_TERMS = {
    'gender': [['man', 'son', 'father', 'boy', 'brother', 'grandfather', 'husband', 'schoolboy', 'gentleman', 'himself',
                'daddy', 'groom',
                'male', 'gentlemen', 'he', 'stepfather', 'boyfriend', 'him', 'his', 'sir'],
               ['woman', 'daughter', 'mother', 'girl', 'sister', 'grandmother', 'wife', 'schoolgirl', 'lady', 'herself',
                'mommy', 'bride',
                'female', 'ladies', 'she', 'stepmother', 'girlfriend', 'her', 'hers', 'ma am']],  # male-female
    'profession': [['barber'], ['coach'], ['businessperson'], ['football player'], ['construction worker'],
                   ['manager'], ['CEO'], ['accountant'], ['commander'], ['firefighter'], ['mover'],
                   ['software developer'], ['guard'], ['baker'], ['doctor'], ['athlete'], ['artist'], ['dancer'],
                   ['mathematician'], ['janitor'], ['carpenter'], ['mechanic'], ['actor'], ['handyman'],
                   ['musician'], ['detective'], ['politician'], ['entrepreneur'], ['model'], ['opera singer'],
                   ['chief'], ['lawyer'], ['farmer'], ['writer'], ['librarian'], ['army'], ['real-estate developer'],
                   ['broker'], ['scientist'], ['butcher'], ['electrician'], ['prosecutor'], ['banker'],
                   ['cook'], ['hairdresser'], ['prisoner'], ['plumber'], ['attorney'], ['boxer'], ['chess player'],
                   ['priest'], ['swimmer'], ['tennis player'], ['supervisor'], ['attendant'],
                   ['housekeeper'], ['maid'], ['producer'], ['researcher'], ['midwife'], ['judge'], ['umpire'],
                   ['bartender'], ['economist'], ['physicist'], ['psychologist'], ['theologian'], ['salesperson'],
                   ['physician'], ['sheriff'], ['cashier'], ['assistant'], ['receptionist'], ['editor'], ['engineer'],
                   ['comedian'], ['painter'], ['civil servant'], ['diplomat'], ['guitarist'], ['linguist'],
                   ['poet'], ['laborer'], ['teacher'], ['delivery man'], ['realtor'], ['pilot'], ['professor'],
                   ['chemist'], ['historian'], ['pensioner'], ['performing artist'], ['singer'], ['secretary'],
                   ['auditor'], ['counselor'], ['designer'], ['soldier'], ['journalist'], ['dentist'], ['analyst'],
                   ['nurse'], ['tailor'], ['waiter'], ['author'], ['architect'], ['academic'], ['director'],
                   ['illustrator'], ['clerk'], ['policeman'], ['chef'], ['photographer'], ['drawer'], ['cleaner'],
                   ['pharmacist'], ['pianist'], ['composer'], ['handball player'], ['sociologist']],  # uncategorized
    'race': [['Nigerian'], ['Ethiopia'], ['Europe'], ['European'], ['Russian'], ['Ukraine'], ['Sudan'], ['Afghanistan'],
             ['Iraq'], ['Yemen'], ['Ukrainian'], ['Russia'], ['Italy'], ['Somali'], ['Iran'], ['Afghan'], ['Indian'],
             ['Italian'], ['Australian'], ['Spanish'], ['Guatemalan'], ['Hispanic'], ['Venezuela'], ['Sudanese'],
             ['Oman'], ['Finnish'], ['Swedish'], ['Venezuelan'], ['Puerto'], ['Rican'], ['Ghanaian'], ['Moroccan'],
             ['Somalia'], ['Saudi'], ['Arabian'], ['Syria'], ['Chinese'], ['Pakistani'], ['China'], ['India'],
             ['Irish'], ['Britain'], ['France'], ['GreeceScotland'], ['Mexican'], ['Paraguayan'], ['Brazil'],
             ['African'], ['EritreanSierra'], ['Leonean'], ['Africa'], ['Jordan'], ['Indonesia'], ['Vietnam'],
             ['PakistanGerman'], ['Romania'], ['Brazilian'], ['Ecuadorian'], ['Mexico'], ['Puerto'], ['Rico'], ['Kenyan'],
             ['Liberian'], ['Cameroonian'], ['African'], ['Americans'], ['Kenya'], ['Liberia'], ['Sierra'], ['Leon'],
             ['Qatari'], ['Syrian'], ['Arab'], ['Saudi'], ['Arabia'], ['Lebanon'], ['Indonesian'], ['French'],
             ['Norweigan'], ['South'], ['Africa'], ['Jordanian'], ['Korea'], ['Singapore'], ['Romanian'], ['Crimean'],
             ['Native'], ['American'], ['Germany'], ['Ireland'], ['Ecuador'], ['Morocco'], ['Omani'], ['Iranian'],
             ['Iraqi'], ['Qatar'], ['Turkey'], ['Vietnamese'], ['Nepali'], ['Laos'], ['Bangladesh'], ['British'],
             ['Polish'], ['Greek'], ['Scottish'], ['Bolivian'], ['Guatemala'], ['Ghana'], ['Cameroon'], ['Japanese'],
             ['Taiwanese'], ['Bengali'], ['Nepal'], ['Albanian'], ['Albania'], ['Columbian'], ['Peruvian'],
             ['Argentian'], ['Spain'], ['Paraguay'], ['Ethiopian'], ['Egyptian'], ['Persian'], ['people'], ['Sweden'],
             ['Crimea'], ['Portuguese'], ['Argentina'], ['Chile'], ['Cape'], ['Verdean'], ['Turkish'], ['Yemeni'],
             ['Taiwan'], ['Austrian'], ['White'], ['people'], ['Finland'], ['Australia'], ['South'], ['African'],
             ['Eriteria'], ['Egypt'], ['Korean'], ['Dutch'], ['people'], ['Peru'], ['Poland'], ['Chilean'],
             ['Columbia'], ['Bolivia'], ['Laotian'], ['Lebanese'], ['Japan'], ['Norway'], ['Cape'], ['Verde'],
             ['Portugal'], ['Austria'], ['Singaporean'], ['Netherlands']],  # uncategorized
    'religion': [['islam', 'sharia', 'jihad', 'muslim', 'mohammed', 'quran'],
                 ['christian', 'church', 'bible', 'holy trinity'],
                 ['hindu', 'brahmin']],  # islam-christian-hindu
}