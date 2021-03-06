D_GF = 32
D_DF = 64
D_WORD = 300
D_HIDDEN = 256
D_Z = 100
D_COND = 100

GENERATOR_LR = 2e-4
DISCRIMINATOR_LR = 1e-4
DAMSM_LR = 2e-3

RESIDUALS = 2

IMG_WEIGHT_INIT_RANGE = 0.1

P_DROP = 0.4

GAN_BATCH = 2 #20
BATCH = 48

BASE_SIZE = 64

BRANCH_NUM = 3

CAPTIONS = 10

CAP_MAX_LEN = 18

END_TOKEN = '<END>'
UNK_TOKEN = '<UNK>'

DEVICE = 'cuda'

GAMMA_1 = 4.0
GAMMA_2 = 5.0
GAMMA_3 = 10.0
LAMBDA = 5.0

MIN_WORD_FREQ = 1

MODEL_DIR = 'models'
DAMSM_MODEL_DIR = MODEL_DIR + '/damsm'
GAN_MODEL_DIR = MODEL_DIR + '/gan'
OUT_DIR = 'output'
