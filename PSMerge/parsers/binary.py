#!/usr/bin/env python

from parsers.parser import Parser

import tensorflow as tf
import pandas as pd
import numpy as np

#from utils.utils import get_dir

def __make_all_values_same_length__(val, **kwargs):
  result = str(val)
  length_val = len(str(val))
  max_length_feature = kwargs.pop('max_length_feature')

  if length_val < max_length_feature:
    fill_with_n_zeroes = max_length_feature - length_val
    new_val = ('0' * fill_with_n_zeroes) + str(val)
    result = new_val

  return result

class BinToCSV(Parser):
  def parse(self):
    assert self.dataframe is not None, 'Please specify the dataframe to parse'

    df = self.dataframe
    n_features = df.columns.size
    for x in range(n_features):
      serie = df.iloc[:, x]
      max_length_feature = len(str(serie.max()))
      df.iloc[:, x] = serie.apply(__make_all_values_same_length__, max_length_feature=max_length_feature)

    return df
