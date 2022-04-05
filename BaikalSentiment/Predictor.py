import pickle
import pyarrow as pa
from datasets import Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from tqdm import tqdm

def make_dataset(read_dir):
  data = pickle.load(open(read_dir,'rb'))
  dataset = Dataset(
      pa.Table.from_pandas(
          data, preserve_index=False
      )
  )
  return dataset

def prediction_pipeline(
  pretrained_name,
  model_max_length,
  use_gpu
):
  return pipeline(
    tokenizer = AutoTokenizer.from_pretrained(
      pretrained_name,
      model_max_length = model_max_length
    ),
    model = pretrained_name,
    device = 0 if use_gpu else -1
  )
  # note: model pulled from main revision of `pretrained_name` repo
  
def pred_adjust(sentiment_label):
  return int(sentiment_label.split('_')[1]) - 1

def run_prediction(
  read_dir = './data/data_in.pickle',
  write_dir = './data/data_out.pickle',
  batch_size = 1,
  pretrained_name = '',
  model_max_length = 512,
  use_gpu = False
):
  
  # TODO: figure out optimization of pipeline through a better dataloader
  # dataset = make_dataset(read_dir)
  dataset = pickle.load(open(read_dir,'rb'))

  pred_pipe = prediction_pipeline(
    pretrained_name,
    model_max_length,
    use_gpu
  )
  
  print('-'*30)
  print('Starting prediction')
  print(f'GPU: {use_gpu}')
  print(f'Batch size: {batch_size}')

  dataset['sentiment'] = [x['label'] for x in tqdm(
    pred_pipe(
      dataset['final_clean_text'].tolist(),
      batch_size = batch_size
    ),
    total = dataset.shape[0]
  )]

  dataset['adj_sentiment'] = [
    pred_adjust(x) for x in dataset['sentiment']
  ]

  pickle.dump(
    dataset,
    open(write_dir, 'wb')
    )


# make sure to output some progress so we can benchmark performance