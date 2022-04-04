import pymongo
import pickle
from sshtunnel import SSHTunnelForwarder
from tqdm import tqdm

from config import *
from .BaikalSentiment import run_preprocess

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
  print('-'*30)
  print('Loading data and save in temp dir')

  # open connection to db
  db, connection = connect_db()

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
    read_dir=RAW_DATA_PATH,
    write_dir=PRE_DATA_PATH
  )

def predict():
  pass

def upload():
  # aggregate and upload
  pass

if __name__=='__main__':
  # instantiate db connection

  # then
  load_data()
  preprocess()
  # predict()
  # upload()