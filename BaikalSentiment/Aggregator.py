import pickle
from tqdm import tqdm

def run_aggregation(
  raw_dir = './data/raw_data.pickle',
  pred_dir = './data/data_in.pickle',
  write_dir = './data/data_out.pickle'
):

  raw_data = pickle.load(open(raw_dir,'rb'))
  pred_data = pickle.load(open(pred_dir,'rb'))

  indexed_raw = {
      str(x['_id']):x for x in tqdm(raw_data)
  }
  
  print('-'*30)
  print('Updating sentiment label')

  for index, row in pred_data.iterrows():
    indexed_raw[row['_id']]['sentiment'] = row['adj_sentiment']

  data_list = list(indexed_raw.values())

  pickle.dump(
    data_list,
    open(write_dir,'wb')
    )