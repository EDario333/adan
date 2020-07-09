#!/usr/bin/env python

import tensorflow as tf
import pandas as pd
import numpy as np

import argparse
import requests
import urllib

import csv

from utils import __get_tmp_dir__, get_file_name_without_extension

from utils import ps_merge_dnf_singletons_mu2, get_dir

parser = argparse.ArgumentParser()

FN_WITHOUT_EXTENSION = 'data'

def __parse_args__():
  global parser

  parser.add_argument('-cf', '--configuration-file', help='The fille where all the data (variables, datasource, and so on) is located [at this point we only tried with JSON files]', type=str, required=True)

  parser.add_argument('-sptr', '--starting-percent-training', help='The percent of records/rows to consider for the training set [default: 0.66]', type=float, default=0.66)

  args = parser.parse_args()

  assert args.configuration_file is not None, 'Please specify the configuration file'

  return args

def __verify_args__(args):
  assert args is not None, 'You missed the args!'
  assert args.configuration_file is not None, 'Please specify the configuration file'
  
def __parse_json_file__(datasource):
  from requests.exceptions import InvalidSchema
  import json
  url = datasource
  res = None

  try:
    res = requests.get(url).json()
  except InvalidSchema as error:
    if str(error).index('file://'):
      file_ = open(url[len('file://'):], 'r')
      res = json.load(file_)
      file_.close()

  return res

def __read_conf_args__(json_file=None):
  assert json_file is not None, 'Please specify the json file'

  # It is n_bases the record/rows number?
  # If the answer is yes then we could use: df.count
  #n_bases = json_file['n_bases']

  # It is n_var the features/cols number?
  # If the answer is yes then we could use: len(df.columns)
  #n_vars = json_file['n_vars']

  datasource = json_file['datasource']
  output_dir = json_file['output_dir']

  #return n_bases, n_vars, datasource, output_dir
  return datasource, output_dir

def __load_data__(datasource):
  path = tf.keras.utils.get_file(datasource.split('/')[-1], datasource)

  return pd.read_csv(path, header=0)

def __generate_training_data__(original_df_training=None):
  assert original_df_training is not None, 'Please specify the original training dataframe'

  df_training = original_df_training.copy()
  lst_col = df_training.columns.values[df_training.columns.size-1]

  #for i=1:N_Bases

  #if mod(i,3)!=0
  #Literal_Aux_Training(1:N_Variables-1,N_Trainings)=num2str(abs(1-Literal_Matrix(1:N_Variables-1,i)));

  #Literal_Aux_Training(N_Variables,N_Trainings)=num2str(Literal_Matrix(N_Variables,i));
  df_training.iloc[:, df_training.columns != lst_col] = abs(1-df_training.iloc[:, df_training.columns != lst_col])

  return df_training

def __generate_test_data__(df=None, df_training=None):
  assert df is not None, 'Please specify the original dataframe (data source)'
  assert df_training is not None, 'Please specify the training dataframe'

  df_test = df[~df.isin(df_training).all(1)].copy()

  lst_col = df_test.columns.values[df_test.columns.size-1]

  #for i=1:N_Bases
  #if mod(i,3)==0
  #Literal_Aux(1:N_Variables-1,N_Tests)=num2str(abs(1-Literal_Matrix(1:N_Variables-1,i)));
      
  #Literal_Aux(N_Variables,N_Tests)=num2str(Literal_Matrix(N_Variables,i));
  df_test.iloc[:, df_test.columns != lst_col] = abs(1-df_test.iloc[:, df_test.columns != lst_col])

  return df_test

def __generate_dnf_file__(df_training=None, n_vars=None, filename=None, output_dir=None):
  assert df_training is not None, 'Please specify the datasource for the training'
  assert n_vars is not None, 'Please specify the variables number'
  assert filename is not None, 'Please specify the filename'
  assert output_dir is not None, 'Please specify the directory where it will be saved the file'

  n_trainings = len(df_training)

  features = df_training.columns

  possible_solutions = []
  solutions = []
  max_sum = 0;

  #state = []
  #state = np.zeros(n_vars, bool)

  #for feature in features:
    #state.append(0)

  for i in range(pow(2, n_vars)):
    val = bin(i)
    val = '0' * (n_vars - len(val[2:])) + val[2:]
    possible_solutions.append(val)

    #for j in range(n_vars):
      ##state[:j] = val[j]
      #print('i_Binary(j) = {}'.format(val[j]))
      #state[:j] = val[j]

    ac = 0

    for s in range(n_trainings):
      ps_conjoint = 0
      for j in range(n_vars):
        #if state[:j] == 1 and df_training.iat[s, j] == 1:
        #if np.take(state, j) == 1 and df_training.iat[s, j] == 1:
        if val[j] == '1' and df_training.iat[s, j] == 1:
          ps_conjoint = 1
          break

        #if state[:j] == 0 and df_training.iat[s, j] == 0:
        #if np.take(state, j) == 0 and df_training.iat[s, j] == 0:
        if val[j] == '0' and df_training.iat[s, j] == 0:
          ps_conjoint = 1
          break

      ac += ps_conjoint;

    if ac == max_sum:
      solutions.append(i)
    elif ac > max_sum:
      solutions = [i]
      max_sum = ac

  l = len(solutions)

  csvfile = open(output_dir + '/' + filename + '-dnf.csv', 'w')
  writer = csv.writer(csvfile)

  writer.writerow(features)

  for i in range(l):
    writer.writerow(possible_solutions[solutions[i]])

  csvfile.close()

  possible_solutions = [possible_solutions[i] for i in solutions]
  #return solutions, possible_solutions
  return possible_solutions

def __get_dnf_dataframe__(filename=None, output_dir=None):
  assert filename is not None, 'Please specify the filename'
  assert output_dir is not None, 'Please specify the output directory'

  #import os
  #pwd = os.path.dirname(os.path.abspath(__file__))

  #path_solution = 'file://' + pwd + '/' + filename + '-dnf.csv'
  path_solution = 'file://' + output_dir + '/' + filename + '-dnf.csv'
  path = tf.keras.utils.get_file(path_solution.split('/')[-1], path_solution)  
  df = pd.read_csv(path, header=0)

  return df
  
def __generate_b01_file__(df_test=None, filename=None, output_dir=None):
  assert df_test is not None, 'Please specify the testing dataframe'
  assert filename is not None, 'Please specify the filename'
  assert output_dir is not None, 'Please specify the directory where it will be saved the file'

  df_solution = __get_dnf_dataframe__(filename, output_dir)

  l = len(df_solution)
  n_vars = df_test.columns.size
  n_tests = len(df_test)
  
  row = ['B'] * len(df_test)

  nan = [np.NaN] * len(df_test)

  data = [row, row, nan]

  solution_test = pd.DataFrame(data)
  
  #solution_test.replace([np.NaN], [df_test.iloc[:, n_vars-1]], inplace=True)

  for idx, val in solution_test.iloc[2, :].iteritems():
    solution_test.iloc[2, idx] = df_test.iloc[idx, n_vars-1]

  for i in range(n_tests):
    for j in range(l):
      if df_solution.iloc[j, 0:n_vars-1].equals(df_test.iloc[i, 0:n_vars-1]):
        if df_solution.iat[j, n_vars-1] == 0:
          solution_test.iat[0, i] = 0
          if j < l and \
          df_solution.iloc[j+1, 0:n_vars-2].equals(df_test.iloc[i,0:n_vars-2]) and \
          df_solution.iat[j+1, n_vars-1] == 1:
            #Solution_Test(2,i)='1';
            solution_test.iat[1, i] = 1
        else:
            #Solution_Test(2,i)='1';
            solution_test.iat[1, i] = 1
        break

  solution_test = solution_test.transpose()

  #col_names = df_solution.columns.values
  #col_names = col_names[0:len(col_names)-1]

  #solution_test.to_csv(filename + '-B01.csv', index=False, header=col_names)
  solution_test.to_csv(output_dir + '/' + filename + '-B01.csv', index=False)
  return solution_test

def __generate_sol_file__(df=None, df_test=None, solution_test=None, filename=None, output_dir=None):
  assert df is not None, 'Please specify the original dataframe'
  assert df_test is not None, 'Please specify the testing dataframe'
  assert solution_test is not None, 'Please specify the solution test dataframe'
  assert filename is not None, 'Please specify the filename'
  assert output_dir is not None, 'Please specify the directory where it will be saved the file'

  constraints = df.copy()
  constraints = constraints.replace([0, 1], [np.NaN, np.NaN])

  df_solution = __get_dnf_dataframe__(filename, output_dir)

  n_tests = len(df_test)
  n_vars = df_test.columns.size
  l = len(df_solution)
  features = df_test.columns.values

  #for i=1:N_Tests
  for i in range(n_tests):
    #if (Solution_Test(1,i)==Solution_Test(2,i)) 
    if solution_test.iat[i, 0] == solution_test.iat[i, 1]:
      """
      All this block are the same to the other one. Please remove from here and put it out from the if (after the for)
      """
      #Constraints(1:N_Variables-1,1)=Literal_Test(i,1:N_Variables-1);
      constraints.iloc[0:n_vars-1, 0] = list(df_test.iloc[i, 0:n_vars-1])

      #Constraints(1:N_Variables-1,2)=Literal_Test(i,1:N_Variables-1);
      constraints.iloc[0:n_vars-1, 1] = list(df_test.iloc[i, 0:n_vars-1])

      #Constraints(N_Variables,1)='0'; 
      constraints.iloc[n_vars-1, 0] = 0
      
      #Constraints(N_Variables,2)='1';
      constraints.iloc[n_vars-1, 1] = 1

      #Aux=PSMergeCNFSingletonsmu2(N_Bases,N_Variables,Literal_Matrix,2,Constraints);
      aux = ps_merge_dnf_singletons_mu2(l, n_vars, df_solution.transpose(), 2, constraints)

      """
      Ends the block!
      """  

      #if size(Aux,1)==1
      #if aux[0] == 1:
      if aux.iat[0, 0] != np.NaN:
        #if Aux(1,N_Variables)=='0'
        if aux.iat[n_vars-1, 0] == 0:
          #Solution_Test(1,i)='0';
          solution_test.iat[i, 0] = 0
        #end

        #if Aux(1,N_Variables)=='1'  
        else:
          #Solution_Test(2,i)='1';
          solution_test.iat[i, 1] = 1
        #end
      #end

    #elseif Solution_Test(1,i)=='0' && Solution_Test(2,i)=='1'
    elif solution_test.iat[i, 0] == 0 and solution_test.iat[i, 1] == 1:
      """
      All this block are the same from the previous one. Please remove from here and put it out from the if (after the for)
      """

      #Constraints(1:N_Variables-1,1)=Literal_Test(i,1:N_Variables-1);
      constraints.iloc[0:n_vars-1, 0] = list(df_test.iloc[i, 0:n_vars-1])

      #Constraints(1:N_Variables-1,2)=Literal_Test(i,1:N_Variables-1)
      constraints.iloc[0:n_vars-1, 1] = list(df_test.iloc[i, 0:n_vars-1])

      #Constraints(N_Variables,1)='0'; 
      constraints.iloc[n_vars-1, 0] = 0
      
      #Constraints(N_Variables,2)='1';
      constraints.iloc[n_vars-1, 1] = 1

      #Aux=PSMergeDNFSingletonsmu2(N_Bases,N_Variables,Literal_Matrix,2,Constraints);
      aux = ps_merge_dnf_singletons_mu2(l, n_vars, df_solution.transpose(), 2, constraints)

      """
      Ends the block!
      """

      #if size(Aux,1)==1
      #if aux[0] == 1:
      if aux.iat[0,0] != np.NaN:
        #if Aux(1,N_Variables)=='0'
        if aux.iat[n_vars-1, 0] == 0:
          #Solution_Test(2,i)='B'; 
          solution_test.at[i, 1] = 'B'
        #end

        #if Aux(1,N_Variables)=='1'
        else:
          #Solution_Test(1,i)='B'; 
          solution_test.at[i, 0] = 'B'
        #end
      #end

  csvfile = open(output_dir + '/' + filename + '-sol.csv', 'w')
  writer = csv.writer(csvfile)

  writer.writerow(features)

  #for i=1:N_Tests
  for i in range(n_tests):
    #if Solution_Test(1,i)=='0' && Solution_Test(2,i)=='1' 
    if solution_test.iat[i, 0] == 0 and solution_test.iat[i, 1] == 1:
      #fprintf(fid1,'(%d) %c %c\n', i, 'B',Solution_Test(3,i));
      #writer.writerow([i, 'B', solution_test.at[2, i]])
      writer.writerow(['B', solution_test.iat[i, 2]])

    #elseif Solution_Test(1,i)=='0'
    elif solution_test.iat[i, 0] == 0:
      #fprintf(fid1,'(%d) %c %c\n', i, '0',Solution_Test(3,i));
      #writer.writerow([i, 0, solution_test.at[2, i]])
      writer.writerow([0, solution_test.iat[i, 2]])
    else:
      #fprintf(fid1,'(%d) %c %c\n', i,'1', Solution_Test(3,i));
      #writer.writerow([i, 1, solution_test.at[2, i]])
      writer.writerow([1, solution_test.iat[i, 2]])
    #end
  #end
  #status=fclose(fid1)
  csvfile.close()

  # Now we're gonna drop the empty cols
  #import os
  #pwd = os.path.dirname(os.path.abspath(__file__))
  #path = filename + '-sol.csv'
  path = output_dir + '/' + filename + '-sol.csv'
  #path = filename + '-sol.csv'

  path = tf.keras.utils.get_file(path, 'file://' + output_dir + '/' + path)

  df = pd.read_csv(path, header=0)
  df.dropna(axis='columns', inplace=True)
  df.to_csv(output_dir + '/' + filename + '-sol.csv', index=False)

  return solution_test

def __solve__(solution_test=None):
  assert solution_test is not None, 'Please specify the solution test dataframe'

  #d1 = 0;  dw1=0; d0=0; dw0=0;  d_or=0;  d_not=0;
  d1, dw1, d0, dw0, d_or, d_not = 0, 0, 0, 0, 0, 0;

  n_tests = len(solution_test)

  for i in range(n_tests):
    #if (Solution_Test(1,i)==Solution_Test(2,i))
    if solution_test.iat[i, 0] == solution_test.iat[i, 1]:
      d_not += 1
    #elseif Solution_Test(1,i)=='0' && Solution_Test(2,i)=='1', 
    elif solution_test.iat[i, 0] == 0 and solution_test.iat[i, 1] == 1:
      d_or += 1
    #elseif Solution_Test(1,i)==Solution_Test(3,i),  
    elif solution_test.iat[i, 0] == solution_test.iat[i, 2]:
      d0 += 1
    #elseif Solution_Test(2,i)==Solution_Test(3,i),
    elif solution_test.iat[i, 1] == solution_test.iat[i, 2]:
      d1 += 1
    #elseif Solution_Test(3,i)=='0', 
    elif solution_test.iat[i, 2] == 0:
      dw0 += 1
    #elseif Solution_Test(3,i)=='1',
    elif solution_test.iat[i, 2] == 1:
      dw1 += 1

  return [d1, dw1, d0, dw0, d_or, d_not]

def PSMergeCNFSingTrainTestThenReviseIW(args=None):
  global FN_WITHOUT_EXTENSION

  __verify_args__(args)

  conf = __parse_json_file__(args.configuration_file)

  datasource, output_dir = __read_conf_args__(conf)
  output_dir = output_dir[output_dir.index('://') + len('://'):]

  fn_without_extension = get_file_name_without_extension(conf['datasource'])

  df = __load_data__(conf['datasource'])

  # We must to ensure that for each feature/attr/column the number of digits will be the same
  from parsers.binary import BinToCSV
  parser = BinToCSV(dataframe=df)
  df = parser.parse()
  df.to_csv(get_dir(conf['output_dir']) + '/' + fn_without_extension + '.csv', index=False)

  n_bases = len(df)
  n_vars = df.columns.size

  #original_df_training = pd.DataFrame()
  #for x in range(len(df)):
    #if x % 3 != 0:
      #original_df_training = original_df_training.append(df.iloc[x-1, :])

  sptr = args.starting_percent_training
  original_df_training = df.sample(round(sptr * len(df)))

  df_training = __generate_training_data__(original_df_training)
  filename = output_dir + '/' + fn_without_extension + '-tra.csv'
  df_training.to_csv(filename, index=False)

  df_test = __generate_test_data__(df, original_df_training)
  filename = output_dir + '/' + fn_without_extension + '-tes.csv'
  df_test.to_csv(filename, index=False)

  solutions = __generate_dnf_file__(original_df_training, n_vars, fn_without_extension, output_dir)

  solution_test = __generate_b01_file__(df_test, fn_without_extension, output_dir)
  solution_test = __generate_sol_file__(df, df_test, solution_test, fn_without_extension, output_dir)

  solution = __solve__(solution_test)
  print(solution)

def main(*args):
  args = __parse_args__()
  PSMergeCNFSingTrainTestThenReviseIW(args=args)

if __name__ == '__main__':
  import sys
  main(*sys.argv[1:])
