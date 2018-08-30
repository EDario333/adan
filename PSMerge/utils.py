def read_txt_file_and_parse_to_csv(filename):
  import csv

  f = open(filename, 'r')

  line = f.readline()

  csvfile = open('data.csv', 'w')

  writer = csv.writer(csvfile)

  while line:
    line = line.strip()
    values = line.split(' ')
    row = []
    for val in values:
      print(val.index('('))
      if len(val.strip()) > 0 and val.strip() != ' ' and not val.index('('):
        row.append(val)
    writer.writerow(row)

    line = f.readline()

  f.close()
  csvfile.close()

def get_file_name_without_extension(data_source=None):
  #assert args is not None, 'You missed the args!'
  #assert args.data_source is not None, 'Please specify the data source'
  assert data_source is not None, 'Please specify the data source'
  #file_name = args.data_source[args.data_source.rfind('/') + 1:]
  file_name = data_source[data_source.rfind('/') + 1:]
  file_name = file_name[0:file_name.find('.')]

  return file_name

def __get_tmp_dir__():
  return '/tmp/'

def ps_merge_dnf_singletons_mu2(n_bases=None, n_vars=None, lm=None, n_constraints=None, lc=None):
  assert n_bases is not None, 'You must specify the number of bases'
  assert n_vars is not None, 'You must specify the variable numbers'
  assert lm is not None, 'You must specify the literal matrix'
  assert n_constraints is not None, 'You must specify the constraints number'
  assert lc is not None, 'You must specify the literal constraints'

  import numpy as np
  import pandas as pd

  #Solution_Set = [0];
  solution = []
  solution_set = []

  #Max_Sum = 0;
  max_sum = 0

  #state = zeros(1,N_Variables);
  #state = np.zeros((1, n_vars), dtype=bool)

  state = []

  #for i=1:N_Constraints
  for i in range(n_constraints):
    #i_Binary=Literal_Constraints(:,i);
    i_Binary = lc.iloc[:, i]

    #for j=1:N_Variables
    for j in range(n_vars):
      #state(j) = str2num(i_Binary(j));
      #state[j] = i_Binary[j]
      #state[:j] = i_Binary[j]
      state.append(i_Binary[j])
    #end

    #Sum = 0;
    sum_ = 0

    #for s = 1:N_Bases    % number of sources
    for s in range(n_bases):
      #ps_disjoint=0;
      ps_disjoint = 0

      #satisfied=0;
      satisfied = 0

      #%conjuncts=0;
      #for j = 1:N_Variables
      for j in range(n_vars):
        #if state(j)==0 ,
        #if state[j] == 0:
        #if np.take(state, j) == 0:
        if state[j] == 0:
          #satisfied=satisfied + abs(1-Literal_Matrix(j,s));
          satisfied += abs(1-lm.iat[j, s])
        #end
        #if state(j)==1, 
        #elif state[j] == 1:
        else:
          #satisfied=satisfied + Literal_Matrix(j,s); 
          satisfied += lm.iat[j, s]
        #end
      #end

      #ps_disjoint = satisfied/N_Variables;
      ps_disjoint = satisfied/n_vars

      #%PS(i,s)= max(ps_disjoint);
      #%Sum(i) = Sum(i) + PS(i,s);

      sum_ += ps_disjoint
    #end

    #I=i, SUM=Sum,
    #if (strcmp(num2str(Sum), num2str(Max_Sum)))
    if (sum_ == max_sum):
      #Solution_Set(sum(size(Solution_Set)))=i;
      solution_set.append(i)
    #elseif (Sum > Max_Sum)
    elif sum_ > max_sum:
      #Solution_Set = [i];
      solution_set = [i]
      #Max_Sum=Sum;
      max_sum = sum_
    #end
  #end

  #L=length(Solution_Set);
  l = len(solution_set)

  #for i=1:L
  #solution = []
  #solution = lm.copy()
  solution = pd.DataFrame()

  #col_names = [solution.columns.values[x] for x in range(1, solution.columns.size)]

  #solution = solution.drop(columns=col_names)
  #solution = solution.replace([0, 1], [np.NaN, np.NaN])

  for i in range(l):
    #Solution(i,:)=Literal_Constraints(:,Solution_Set(i))
    #solution.iloc[i, :] = lc.iloc[:, solution_set[i]]
    #solution.iloc[i, :] = list(lc.iloc[:, solution_set[i]])
    solution = pd.concat([lc.iloc[:, solution_set[i]]], axis='columns')
    #solution.iloc[i, :] = list(lc.iloc[:, solution_set[i]])
    #print('lc.iloc[:, solution_set[i]]')
    #print(solution)
    #quit()
    
    #solution.append(lc.iloc[:, solution_set[i]])

  solution.dropna(inplace=True)

  return solution

def get_dir(path=None):
  assert path is not None, 'Please specify the dir path'
  if 'file://' in path:
    return path[6:]
  return path
