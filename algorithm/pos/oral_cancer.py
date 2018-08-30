#!/usr/bin/env python 

import tensorflow as tf
import pandas as pd
from utils import utils as adan_utils

def processing(df_training=None, args=None):
  assert df_training is not None, 'The dataframe is missed'
  assert args is not None, 'The args are missed'

  conf = adan_utils.parse_json_file(args.configuration_file)

  features_ = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
  features = []

  for key in features_:
    features.append(tf.feature_column.numeric_column(key=key))

  return df_training, features
