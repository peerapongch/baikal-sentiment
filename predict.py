import pymongo
import pickle
from sshtunnel import SSHTunnelForwarder
from tqdm import tqdm

from config import *
from BaikalSentiment.Preprocessor import run_preprocess

def connect_db():
  print('-'*30)
  print('Establishing Connection with Aion MongoDB')
  # define ssh tunnel
  server = SSHTunnelForwarder(
      BASTION_HOST,
      ssh_username = BASTION_USER,
      ssh_password = BASTION_PASS,
      remote_bind_address=(DB_HOST, DB_PORT),
      local_bind_address=(LOCAL_BIND_HOST, LOCAL_BIND_PORT)
  )

  # tunnel and bind port
  server.start()

  # connection
  connection = pymongo.MongoClient(
      host = server.local_bind_host,
      port = server.local_bind_port,
      username = DB_USER,
      password = DB_PASS,
      authSource = DB_AUTH_SOURCE,
      authMechanism = DB_AUTH_MECH
  )
  db = connection[DB_NAME]

  return db, connection

def load_data(
  ingestation_rule = INGESTATION_RULE
  ):

  # open connection to db
  db, connection = connect_db()
  
  print('-'*30)
  print('Loading data and save in temp dir')

  # query data
  posts = db.user_posts.aggregate(ingestation_rule)

  data = [x for x in posts]

  # save as pickle
  pickle.dump(
    data,
    open(RAW_DATA_PATH, 'wb')
  )

  # close connection
  connection.close()

def preprocess():
  # clean and split
  print('-'*30)
  print('Running Cleaning and Preprocessing')
  
  run_preprocess(
    read_dir = RAW_DATA_PATH,
    write_dir = PRE_DATA_PATH,
    batch_size = BATCH_SIZE,
    pretrained_name = PRETRAINED_NAME,
    model_max_length = MODEL_MAX_LENGTH,
    use_gpu = USE_GPU
  )

def predict():
  print('-'*30)
  print('Running Prediction')

  run_prediction(
    read_dir = PRE_DATA_PATH,
    write_dir = PRED_PATH
  )

def aggregate():
  # TODO: rule wrt to split
  print('-'*30)
  print('Aggregating prediction')
  
  # TODO: convert pd to list
  run_aggregator(
    raw_dir = RAW_DATA_PATH,
    pred_dir = PRED_PATH,
    write_dir = AGG_PATH
  )

def upload():
  # aggregate and upload
  db, connection = connect_db()
  collection = db[UPLOAD_TO_COLLECTION]

  print('-'*30)
  print(f'Uploading to {UPLOAD_TO_COLLECTION}')

  data = pickle.load(
    open(AGG_PATH,'rb')
  )

  for d in tqdm(data):
    collection.insert_one(d)


if __name__=='__main__':
  # instantiate db connection

  # then
  load_data()
  preprocess()
  predict()
  aggregate()
  upload()

  print('done!')