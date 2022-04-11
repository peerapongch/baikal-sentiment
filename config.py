import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

# PROCESS RETRY
N_RETRY = 10
WAIT = 5

# TEMP DATA PATHS
DATA_PATH = './data'
RAW_DATA_PATH = os.path.join(DATA_PATH, 'data_raw.pickle')
PRE_DATA_PATH = os.path.join(DATA_PATH, 'data_pre.pickle')
PRED_PATH = os.path.join(DATA_PATH, 'data_pred.pickle')
AGG_PATH = os.path.join(DATA_PATH, 'data_agg.pickle')

# CONNECTIVITY SETTINGS
BASTION_HOST = "178.128.31.43"
BASTION_USER = "root"
BASTION_PASS = "POC_2020AION"

DB_HOST = '10.130.143.184'
DB_PORT = 27017
DB_USER = 'root'
DB_PASS = 'POC_2020AION'
DB_AUTH_SOURCE = 'admin'
DB_AUTH_MECH = 'SCRAM-SHA-1'
DB_NAME = 'aion'

LOCAL_BIND_HOST = '127.0.0.1'
LOCAL_BIND_PORT = 27017

# DAILY DATA INGESTATION RULE
LAST_N_DAYS = 3
INGESTATION_RULE = [
  {
    "$match": {
      'source': {
        '$eq':'twitter'
        },
      'created_on': {
        '$gte': datetime.now() - relativedelta(days=LAST_N_DAYS), 
        '$lt': datetime.now()
        },
    },
  }
]
# SAMPLE_SIZE = 1000
# INGESTATION_RULE = [
#   {
#     "$match": {
#       'source': {
#         '$eq':'twitter'
#         },
#       'created_on': {
#         '$gte': datetime.now() - relativedelta(days=LAST_N_DAYS), 
#         '$lt': datetime.now()
#         },
#     },
#   },
#   {
#     "$sample": {
#       "size": SAMPLE_SIZE
#       }
#   }
# ]

# MODEL CONFIG
ORGANIZATION = 'peerapongch'
MODEL_NAME = 'baikal-sentiment-ball'
PRETRAINED_NAME = f'{ORGANIZATION}/{MODEL_NAME}'
MODEL_MAX_LENGTH = 416
USE_GPU = True
BATCH_SIZE = 16

# UPLOAD CONFIG
UPLOAD_TO_COLLECTION = 'user_posts_temp'