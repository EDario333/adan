#!/usr/bin/env python 

import tensorflow as tf
import pandas as pd
import random
import os

CSV_COLUMN_NAMES = ['Sepal_length', 'Sepal_width',
                    'Petal_length', 'Petal_width', 'Specie']
LABELS = ['Setosa', 'Versicolor', 'Virginica']

def load_data(data_source=None):
  assert data_source is not None, 'Please specify the data source'

  """Returns the dataset """
  #path = tf.keras.utils.get_file(data_source.split('/')[-1], ds)
  path = tf.keras.utils.get_file(data_source.split('/')[-1], data_source)

  df = pd.read_csv(path, header=1)
  return df

def __get_file_name_without_extension__(args=None):
  assert args is not None, 'The args are missed!'
  file_name = args.data_source[args.data_source.rfind('/') + 1:]
  file_name = file_name[0:file_name.find('.')]

  return file_name

def __choose_random_features__(args=None, source_df=None):
  assert args is not None, 'The args are missed'
  assert source_df is not None, 'Please specify the source dataframe'

  tsfe = len(source_df.columns)
  ssfe = int(tsfe * args.starting_percent_features)

  series = []
  processed = []
  new_df = pd.DataFrame()

  x = random.randint(0, ssfe-1)

  while len(new_df.columns) < ssfe:
    while x in processed:
      x = random.randint(0, ssfe-1)
    processed.append(x)
    serie = source_df[source_df.columns[x]]
    new_df = pd.concat([new_df, serie], 'columns')
    x = random.randint(0, ssfe-1)

  #file_name = args.data_set[args.data_set.rfind('/') + 1:]
  #file_name = file_name[0:file_name.find('.')]
  filename = __get_file_name_without_extension__(args)
  filename += '-' + str(ssfe) + 'features-all-data.csv'
  new_df.to_csv(filename, index=False)

  return new_df

def __choose_random_data__(args=None, randomized_df=None):
  assert args is not None, 'The args are missed'
  assert randomized_df is not None, 'Please specify the randomized dataframe'

  df = pd.DataFrame(randomized_df)
  tsda = len(df)

  tsfe = len(df.columns)
  ssfe = int(tsfe * args.starting_percent_features)

  sstr = int(tsda * args.starting_percent_training)
  df_training = df.sample(sstr)

  file_name_ = __get_file_name_without_extension__(args)
  file_name = file_name_ + '-' + str(ssfe) + 'features-training-data-'
  file_name += str(sstr) + '-rows.csv'
  df_training.to_csv(file_name, index=False)

  df_testing = df[~df.isin(df_training).all(1)]
  file_name = file_name_ + '-' + str(ssfe) + 'features-test-data-'
  file_name += str(tsda-sstr) + '-rows.csv'
  df_testing.to_csv(file_name, index=False)

  n_rows_for_prediction = int(tsda * args.starting_percent_prediction) 
  df_predict = df.sample(n_rows_for_prediction)
  file_name = file_name_ + '-' + str(ssfe) + 'features-predict-data-'
  file_name += str(n_rows_for_prediction) + '-rows.csv'
  df_predict.to_csv(file_name, index=False)

  train_y = df_training.pop(args.label)
  #train_x = df_training

  test_y = df_testing.pop(args.label)
  #df_testing = df_testing

  predict_y = df_predict.pop(args.label)
  #predict_x = df_predict
  expected = []

  for row_index in predict_y:
    expected.append(LABELS[row_index])

  return (df_training, train_y), (df_testing, test_y), df_predict, expected

def read_source(args=None):
  assert args is not None, 'You missed some argument'
  assert args.data_source is not None, 'Please specify the data source'

  df = load_data(args.data_source)
  randomized_df = __choose_random_features__(args, df)
  randomized_df = pd.concat([randomized_df, df.pop(args.label)], 'columns')

  (df_train, train_y), (df_testing, test_y), df_predict, expected = __choose_random_data__(args, randomized_df)

  return (df_train, train_y), (df_testing, test_y), df_predict, expected
  
def train_input_fn(features, labels, batch_size):
  """An input function for training"""
  # Convert the inputs to a Dataset.
  dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

  # Shuffle, repeat, and batch the examples.
  dataset = dataset.shuffle(1000).repeat().batch(batch_size)

  # Return the dataset.
  return dataset

def eval_input_fn(features, labels, batch_size):
  """An input function for evaluation or prediction"""
  features=dict(features)
  if labels is None:
      # No labels, use only features.
      inputs = features
  else:
      inputs = (features, labels)

  # Convert the inputs to a Dataset.
  dataset = tf.data.Dataset.from_tensor_slices(inputs)

  # Batch the examples
  assert batch_size is not None, "batch_size must not be None"
  dataset = dataset.batch(batch_size)

  # Return the dataset.
  return dataset

# The remainder of this file contains a simple example of a csv parser,
#     implemented using a the `Dataset` class.

# `tf.parse_csv` sets the types of the outputs to match the examples given in
#     the `record_defaults` argument.
CSV_TYPES = [[0.0], [0.0], [0.0], [0.0], [0]]

def _parse_line(line):
  # Decode the line into its fields
  fields = tf.decode_csv(line, record_defaults=CSV_TYPES)

  # Pack the result into a dictionary
  features = dict(zip(CSV_COLUMN_NAMES, fields))

  # Separate the label from the features
  label = features.pop('Species')

  return features, label

def csv_input_fn(csv_path, batch_size):
  # Create a dataset containing the text lines.
  dataset = tf.data.TextLineDataset(csv_path).skip(1)

  # Parse each line.
  dataset = dataset.map(_parse_line)

  # Shuffle, repeat, and batch the examples.
  dataset = dataset.shuffle(1000).repeat().batch(batch_size)

  # Return the dataset.
  return dataset
