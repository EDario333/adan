#!/usr/bin/env python 

import tensorflow as tf
import data
import random
import time
import datetime

from utils import utils as adan_utils

import argparse
parser = argparse.ArgumentParser()

BATCH_SIZE = 100
TRAIN_STEPS = 1000

def __parse_args__():
  global parser

  # Global args (for any tool)
  parser.add_argument('-ds', '--data-source', help='The data source [at this point we only tried with CSV files]', type=str, required=True)

  parser.add_argument('-l', '--label', help='The label name', type=str, required=True)

  parser.add_argument('-sres', '--save-the-results', help='Do I have to save the output for each run?', action='store_true')

  parser.add_argument('-resd', '--results-dir', help='Where Do I have to save the output for each run?', type=str)

  # Args from ADAN
  parser.add_argument('-tsta', '--test-set-target-accuracy', help='The desired accuracy for the test set [default: 0.95]', type=float, default=0.95)

  parser.add_argument('-sptr', '--starting-percent-training', help='The percent of records/rows to consider for the training set', type=float, default=0.75)
  
  parser.add_argument('-stpt', '--step-percent-training', help='How much will increment the sptr for each iteration', type=float, default=0.01)

  parser.add_argument('-spfe', '--starting-percent-features', help='The percent of features/cols to consider', type=float, default=0.75)

  parser.add_argument('-stpf', '--step-percent-features', help='How much will increment the spfe for each iteration', type=float, default=0.10)
  
  #parser.add_argument('-sptt', '--starting-percent-test', help='The percent of records/rows to consider for the test set', type=float, default=0.10)

  parser.add_argument('-sppr', '--starting-percent-prediction', help='The percent of records/rows to consider for the prediction set', type=float, default=0.10)

  parser.add_argument('-psac', '--precision_test_accuracy', help='Number of decimals to consider for the tsac value', type=int, default=2)

  parser.add_argument('-hlan', '--hidden-layers-number', help='The number of hidden layers', type=int, default=1, required=True)

  parser.add_argument('-npla', '--neurons-per-layer', help='Number of neurons for each hidden layer', default=[1], type=int, nargs='+', required=True)

  parser.add_argument('-ltst', '--limit-train-steps', help='Limit the train steps number', type=int, default=1000)

  parser.add_argument('-nste', '--number-successful-tests', help='The number of times that we require reach the tsta', type=int, default=10)

  # Args from tensor flow
  parser.add_argument('-bs', '--batch-size', default=BATCH_SIZE, type=int, help='batch size')

  parser.add_argument('-ts', '--train-steps', default=TRAIN_STEPS, type=int, help='number of training steps')

  args = parser.parse_args()

  assert args.data_source is not None, 'Please specify the data source'
  assert args.label is not None, 'Please specify the label name'

  hlan = args.hidden_layers_number
  npla = args.neurons_per_layer

  msg = 'Missed the neurons number for layer(s): {} to {}'.format((len(npla) + 1), hlan)
  assert len(npla) >= hlan, msg

  if args.save_the_results:
    assert args.results_dir and args.results_dir is not None, 'Please specify the results dir. Usage: python adan.py -arg1 val1 -arg2 val2 ... -sres -resd the_results_dir'

  assert args.hidden_layers_number > 0, 'Please specify a valid hidden layers number'
  
  #return args.data_set, args.label, args.batch_size, args.train_steps
  return args

def __print_params__(n_test, args=None, ds_train_x=None, ds_test_y=None, ds_predict_y=None):
  assert args is not None, 'You missed some argument'
  assert ds_train_x is not None, 'You missed ds_train_x argument'
  assert ds_test_y is not None, 'You missed ds_test_y argument'
  assert ds_predict_y is not None, 'You missed ds_predict_y argument'
  
  print('Tests #{}, trying with:\n'.format(n_test))

  # Args from ADAN
  print('Starting percent training: ' + str(args.starting_percent_training) + ' (rows = ' + str(len(ds_train_x)) + ')')

  print('Step percent training: ' + str(args.step_percent_training) + '\n')

  print('Starting percent features: ' + str(args.starting_percent_features) + ' (features = ' + str(len(ds_train_x.columns)) + ')')

  print('Step percent features: ' + str(args.step_percent_features) + '\n')

  #print('Starting percent test: ' + str(args.starting_percent_test) + '\n')

  print('Starting percent prediction: ' + str(args.starting_percent_prediction) + ' (rows = ' + str(len(ds_predict_y)) + ')' + '\n')

  print('Precision test accuracy: ' + str(args.precision_test_accuracy) + ' decimals')

  print('Number of hidden layers: ' + str(args.hidden_layers_number))

  print('Number of neurons for each hidden layer: ' + str(args.neurons_per_layer))

  print('Limit of the train steps: ' + str(args.limit_train_steps))

  print('Number of times that we require reach the tsta: ' + str(args.number_successful_tests))

  # Args from tensor flow
  print('Batch size: ' + str(args.batch_size))
  print('Train steps: ' + str(args.train_steps))

def __algorithm__(args=None):
  assert args is not None, 'You missed some argument'
  assert args.data_source is not None, 'Please specify the data source'
  assert args.label is not None, 'Please specify the label name'

  tf.app.run(__run_with_tensorflow__)

def __run_with_tensorflow__(argv):
  #global parser
  args = parser.parse_args(argv[1:])

  tsac = 0.0
  tsta = args.test_set_target_accuracy
  sptr = args.starting_percent_training
  
  #News *********************************
  nste = args.number_successful_tests
  current_successful_tests = 0
  n_test = 1
  # ************************************

  # Build the hidden layers DNN with its units respectively
  hlan = args.hidden_layers_number
  npla = args.neurons_per_layer
  hidden_units = []
  for x in range(hlan):
    hidden_units.append(npla[x])

  started_total_time = datetime.datetime.now()
  print('Starting the tests at: ' + started_total_time.strftime('%Y-%m-%d %H:%M:%S'))

  while tsac < tsta or current_successful_tests < nste:
    try:
      time.sleep(0.5)
      adan_utils.clean_screen()
      started = datetime.datetime.now()
      print('Starting at: ' + started.strftime('%Y-%m-%d %H:%M:%S'))

      # Fetch the data
      (df_training, train_y), (df_testing, test_y), df_predict, expected = data.read_source(args)

      __print_params__(n_test, args, df_training, test_y, expected)

      # Feature columns describe how to use the input.
      features = []
      weights = []

      #a = tf.feature_column.numeric_column(key='none', shape=(1))
      for key in df_training.keys():
        features.append(tf.feature_column.numeric_column(key=key))
        #x = random.randint(1, len(train_y))

      #a = tf.feature_column.numeric_column(key='SepalWidth', shape=(104))

      #a.shape = [0, 1]
      #print(a)
      #quit()
      #classifier = tf.estimator.DNNClassifier(
          #feature_columns=features,
          #hidden_units=hidden_units,
          ## The model must choose between n classes.
          #n_classes=len(data.LABELS), model_dir='/home/edario/virtualenvs/adan/adan/algorithm/models/')
      classifier = tf.estimator.DNNClassifier(
        feature_columns=features,
        hidden_units=hidden_units,
        # The model must choose between n classes.
        n_classes=len(data.LABELS))

      #print(classifier)
      #quit()

      # Train the Model.
      classifier.train(
          input_fn=lambda:data.train_input_fn(df_training, train_y,
                                                    args.batch_size),
          steps=args.train_steps)

      # Evaluate the model.
      results = classifier.evaluate(
          input_fn=lambda:data.eval_input_fn(df_testing, test_y,
                                                  args.batch_size))

      #test_accuracy = '{accuracy:0.3f}'.format(**results)
      test_accuracy = '{accuracy}'.format(**results)
      test_accuracy = ('{0:.' + str(args.precision_test_accuracy) + 'f}').format(float(test_accuracy))

      print('\nTest set accuracy: {}\n'.format(test_accuracy))

      # Generate predictions from the model
      #expected = ['Setosa', 'Versicolor', 'Virginica']
      #predict_x = {
          #'SepalLength': [4.9, 5, 6.4],
          #'SepalWidth': [3.1, 2.3, 2.8],
          #'PetalLength': [1.5, 3.3, 5.6],
          #'PetalWidth': [0.1, 3.1, 2.2],
      #}
      ##predict_x = {
          ##'SepalLength': [5.1, 5.9, 6.9],
          ##'SepalWidth': [3.3, 3.0, 3.1],
          ##'PetalLength': [1.7, 4.2, 5.4],
          ##'PetalWidth': [0.5, 1.5, 2.1],
      ##}
      #expected, predict_x = data.get_data_to_predict(args)

      predictions = classifier.predict(
          input_fn=lambda:data.predict_input_fn(df_predict,
                                                  labels=None,
                                                  batch_size=args.batch_size))

      template = ('\nPrediction is "{}" ({:.1f}%), expected "{}"')

      for pred_dict, expec in zip(predictions, expected):
        class_id = pred_dict['class_ids'][0]
        probability = pred_dict['probabilities'][class_id]

        print(template.format(data.LABELS[class_id],
                              100 * probability, expec))

      tsac = float(test_accuracy)

      #print(args.starting_percent_training)
      args.starting_percent_training += args.step_percent_training
      #print(args.starting_percent_training)
      
      #News *********************************
      if tsac >= tsta:
        print('************* Succesfully reached the tsta! *************')
        print('*********************************************************')
        current_successful_tests += 1
      
      n_test += 1
      # ************************************

      finished = datetime.datetime.now()
      print('Finished at: ' + finished.strftime('%Y-%m-%d %H:%M:%S'))
      print('Total elapsed time: ' + str(finished-started))

      if args.save_the_results:
        adan_utils.open_dlg_save_output_as()
        time.sleep(0.5)
        if tsac >= tsta:
          adan_utils.save_output(args.results_dir, 'reached_tsta', n_test-1)
        else:
          adan_utils.save_output(args.results_dir, 'tsta_not_reached', n_test-1)
      #time.sleep(0.5)
    except ValueError:
      print(':)   FUNNY!')
      args.starting_percent_training = sptr
      args.train_steps += 1

    if args.train_steps > args.limit_train_steps:
      print(':D   FUNNY 2')
      args.starting_percent_training = sptr
      args.train_steps = TRAIN_STEPS
      args.starting_percent_features += args.step_percent_features

  finished_total_time = datetime.datetime.now()
  print('Total elapsed time: ' + str(finished_total_time-started_total_time))

def main(*args):
  args = __parse_args__()
  __algorithm__(args)

if __name__ == '__main__':
  import sys
  #tf.logging.set_verbosity(tf.logging.INFO)
  main(*sys.argv[1:])
