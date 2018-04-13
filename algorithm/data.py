#!/usr/bin/env python 

import tensorflow as tf
import pandas as pd
import random
import os

CSV_COLUMN_NAMES = ['Sepal_length', 'Sepal_width',
                    'Petal_length', 'Petal_width', 'Specie']
SPECIES = ['Setosa', 'Versicolor', 'Virginica']

def load_data(ds=None, label=None):
  assert ds is not None, 'Please specify the dataset path'
  assert label is not None, 'Please specify the feature (col) for the labels'

  """Returns the dataset """
  path = tf.keras.utils.get_file(ds.split('/')[-1], ds)

  ds = pd.read_csv(path, header=1)
  return ds
  #data_x, data_y = ds, ds.pop(label)
  
  #return (data_x, data_y)

def __get_file_name_without_extension__(args=None):
  assert args is not None, 'You missed some argument'
  file_name = args.data_set[args.data_set.rfind('/') + 1:]
  file_name = file_name[0:file_name.find('.')]

  return file_name

def __choose_random_features__(args=None, ds=None, label_serie=None):
  assert args is not None, 'You missed some argument'
  assert ds is not None, 'Please specify the dataset'
  assert label_serie is not None, 'Please specify the label\'s serie'

  n_series = len(ds.columns)
  ssfe = int(n_series * args.starting_percent_features)

  series = []
  processed = []
  new_x = pd.DataFrame()

  x = random.randint(0, n_series-1)

  while len(new_x.columns) < ssfe:
    while x in processed:
      x = random.randint(0, n_series-1)
    processed.append(x)
    serie = ds[ds.columns[x]]
    new_x = pd.concat([new_x, serie], 'columns')
    x = random.randint(0, n_series-1)

  new_x = pd.concat([new_x, label_serie], 'columns')

  #file_name = args.data_set[args.data_set.rfind('/') + 1:]
  #file_name = file_name[0:file_name.find('.')]
  file_name = __get_file_name_without_extension__(args)
  file_name += '-' + str(ssfe) + 'features-all-data.csv'
  new_x.to_csv(file_name, index=False)

  return new_x

def __choose_random_data__(args=None, x=None, y=None):
  assert args is not None, 'You missed some argument'
  assert x is not None, 'Please specify the x dataset'
  assert y is not None, 'Please specify the y dataset'

  ds = pd.DataFrame(x)
  tsda = len(ds)

  n_series = len(ds.columns)
  ssfe = int(n_series * args.starting_percent_features)
  
  sstr = int(tsda * args.starting_percent_training)
  ds_training = ds.sample(sstr)

  file_name_ = __get_file_name_without_extension__(args)
  file_name = file_name_ + '-' + str(ssfe) + 'features-training-data-'
  file_name += str(sstr) + '-rows.csv'
  ds_training.to_csv(file_name, index=False)

  ds_test = ds[~ds.isin(ds_training).all(1)]
  file_name = file_name_ + '-' + str(ssfe) + 'features-test-data-'
  file_name += str(tsda-sstr) + '-rows.csv'
  ds_test.to_csv(file_name, index=False)

  train_y = ds_training.pop(args.label)
  train_x = ds_training
  
  test_y = ds_test.pop(args.label)
  test_x = ds_test
  #ds = pd.concat([ds, x], 'columns')

  return (train_x, train_y), (test_x, test_y)

def generate_data(args=None):
  assert args is not None, 'You missed some argument'
  assert args.data_set is not None, 'Please specify the dataset'

  ds = load_data(args.data_set, args.label)
  train_y = ds.pop(args.label)
  train_x = __choose_random_features__(args, ds, train_y)

  (train_x, train_y), (test_x, test_y) = __choose_random_data__(args, train_x, train_y)

  return (train_x, train_y), (test_x, test_y)
  
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
