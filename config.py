import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

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
LAST_N_DAYS = 1
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
    }
  }
]
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
#       'domain': 'การเมือง',
#       'subdomain': {
#         '$in': [
#           'บุคคล',
#           'พรรคการเมือง',
#           'นโยบายรัฐบาล',
#           'นโยบายเร่งด่วน',
#           'ประเด็นเฝ้าระวัง'
#           ]
#         },
#     }
#   },
#   {
#     "$sample": {
#       "size": 10000
#       }
#   }
# ]
