import pandas as pd
from enum import Enum

class RandomizeBy(Enum):
  ROWS = 1
  COLS = 2
  BOTH = 3

def __randomize_inputs_by_rows__(pandas_dataframe_x, pandas_dataframe_y, y_name=None):
  assert y_name is not None, 'Please specify the name for the y axis'
  new_x = pandas_dataframe_x.sample(len(pandas_dataframe_x))
  y_values = []

  for row_index, row in new_x.iterrows():
    y_values.append(pandas_dataframe_y[row_index])

  #new_y = pd.DataFrame(data=y_values)
  new_y = pd.Series(data=y_values, name=y_name)
  
  return new_x, new_y

def __randomize_inputs_by_cols__(pandas_dataframe_x, pandas_dataframe_y):
  import random
  processed = []
  
  tope = len(pandas_dataframe_x.columns)
  series = []
  new_x = pd.DataFrame()

  x = random.randint(0, tope-1)
  while len(new_x.columns) < tope:
    while x in processed:
      x = random.randint(0, tope-1)
    processed.append(x)
    serie = pandas_dataframe_x[pandas_dataframe_x.columns[x]]
    new_x = pd.concat([new_x, serie], 'columns')
    x = random.randint(0, tope-1)

  return new_x, pandas_dataframe_y

def randomize_inputs(pandas_dataframe_x, pandas_dataframe_y, randomize_by=RandomizeBy.BOTH, y_name=None):
  if randomize_by is RandomizeBy.ROWS:
    return __randomize_inputs_by_rows__(pandas_dataframe_x, pandas_dataframe_y, y_name=y_name)
  elif randomize_by is RandomizeBy.COLS:
    return __randomize_inputs_by_cols__(pandas_dataframe_x, pandas_dataframe_y)
  
  new_x, new_y = __randomize_inputs_by_rows__(pandas_dataframe_x, pandas_dataframe_y, y_name=y_name)

  return __randomize_inputs_by_cols__(new_x, new_y)
