#!/usr/bin/env python 

import tensorflow as tf
import data

import argparse
parser = argparse.ArgumentParser()

BATCH_SIZE = 100
TRAIN_STEPS = 1000

def __parse_args__():
  global parser

  # Global args (for any tool)
  parser.add_argument('-ds', '--data-set', help='The dataset', type=str)
  parser.add_argument('-l', '--label', help='The label name', type=str)
  
  # Args from ADAN
  parser.add_argument('-tsta', '--test-set-target-accuracy', help='The desired accuracy for the test set', type=float, default=0.95)

  parser.add_argument('-sptr', '--starting-percent-training', help='The percent of records/rows to consider for the training set', type=float, default=0.75)
  
  parser.add_argument('-stpt', '--step-percent-training', help='How much will increment the sptr for each iteration', type=float, default=0.10)

  parser.add_argument('-spfe', '--starting-percent-features', help='The percent of features/cols to consider', type=float, default=0.75)

  parser.add_argument('-stpf', '--step-percent-features', help='How much will increment the spfe for each iteration', type=float, default=0.10)
  
  parser.add_argument('-sptt', '--starting-percent-test', help='The percent of records/rows to consider for the test set', type=float, default=0.10)

  parser.add_argument('-sppr', '--starting-percent-prediction', help='The percent of records/rows to consider for the prediction set', type=float, default=0.10)

  # Args from tensor flow
  parser.add_argument('-bs', '--batch-size', default=BATCH_SIZE, type=int, help='batch size')
  parser.add_argument('-ts', '--train-steps', default=TRAIN_STEPS, type=int,
                    help='number of training steps')

  args = parser.parse_args()

  assert args.data_set is not None, 'Please specify the dataset'
  assert args.label is not None, 'Please specify the label name'

  #return args.data_set, args.label, args.batch_size, args.train_steps
  return args

def __algorithm__(args=None):
  assert args is not None, 'You missed some argument'
  assert args.data_set is not None, 'Please specify the dataset path'
  assert args.label is not None, 'Please specify the label name'

  tsac = 0.0
  tsta = args.test_set_target_accuracy
  sptr = args.starting_percent_training
  stpt = args.step_percent_training
  spfe = args.starting_percent_features
  stpf = args.step_percent_features
  sptt = args.starting_percent_test
  sppr = args.starting_percent_prediction

  tf.app.run(__run_with_tensorflow__)
  
def __run_with_tensorflow__(argv):
  #global parser
  args = parser.parse_args(argv[1:])

  tsac = 0.0
  tsta = args.test_set_target_accuracy

  while tsac < tsta:
    # Fetch the data
    (train_x, train_y), (test_x, test_y) = data.generate_data(args)

    # Feature columns describe how to use the input.
    my_feature_columns = []
    for key in train_x.keys():
      my_feature_columns.append(tf.feature_column.numeric_column(key=key))

    # Build 2 hidden layer DNN with 10, 10 units respectively.
    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        # Two hidden layers of 10 nodes each.
        hidden_units=[10],
        # The model must choose between 3 classes.
        n_classes=3)

    # Train the Model.
    classifier.train(
        input_fn=lambda:data.train_input_fn(train_x, train_y,
                                                  args.batch_size),
        steps=args.train_steps)

    # Evaluate the model.
    eval_result = classifier.evaluate(
        input_fn=lambda:data.eval_input_fn(test_x, test_y,
                                                args.batch_size))

    test_accuracy = '{accuracy:0.3f}'.format(**eval_result)
    print('\nTest set accuracy: {}\n'.format(test_accuracy))

    # Generate predictions from the model
    expected = ['Setosa', 'Versicolor', 'Virginica']
    predict_x = {
        'SepalLength': [5.1, 5.9, 6.9],
        'SepalWidth': [3.3, 3.0, 3.1],
        'PetalLength': [1.7, 4.2, 5.4],
        'PetalWidth': [0.5, 1.5, 2.1],
    }

    predictions = classifier.predict(
        input_fn=lambda:data.eval_input_fn(predict_x,
                                                labels=None,
                                                batch_size=args.batch_size))

    template = ('\nPrediction is "{}" ({:.1f}%), expected "{}"')

    for pred_dict, expec in zip(predictions, expected):
      class_id = pred_dict['class_ids'][0]
      probability = pred_dict['probabilities'][class_id]

      print(template.format(data.LABELS[class_id],
                            100 * probability, expec))

    tsac = float(test_accuracy)

def main(*args):
  args = __parse_args__()
  __algorithm__(args)

if __name__ == '__main__':
  import sys
  tf.logging.set_verbosity(tf.logging.INFO)
  main(*sys.argv[1:])
