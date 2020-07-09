#!/usr/bin/env python

import subprocess
import os
import datetime

n_times = 1

ROOT_DIR = '../../../'
FILE_NAME = 'premade_estimator'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

path = ROOT_DIR + 'models/tensorflow/samples/core/get_started'
results_dir = CURRENT_DIR + '/' + ROOT_DIR + 'results/tensorflow/iris-dataset/'
cmd = 'python3 {}/{}.py'.format(path, FILE_NAME)

def __install_pynput__():
  subprocess.call('python3 -m pip install pynput', shell=True)

def __open_dlg_save_output_as__():
  from pynput.keyboard import Key, Controller
  keyboard = Controller()

  with keyboard.pressed(Key.ctrl):
    keyboard.press(Key.shift)
    keyboard.press('s')
    keyboard.release(Key.shift)
    keyboard.release('s')

def __clean_screen__():
  from pynput.keyboard import Key, Controller
  keyboard = Controller()

  with keyboard.pressed(Key.ctrl):
    keyboard.press(Key.shift)
    keyboard.press('k')
    keyboard.release(Key.shift)
    keyboard.release('k')

def __save_output__(consecutive=1):
  global results_dir
  now = datetime.datetime.now()

  from pynput.keyboard import Key, Controller
  keyboard = Controller()
  file_name = results_dir + str(consecutive) + '-' + FILE_NAME + ' ('
  file_name += now.strftime('%Y-%m-%d') + ').html'
  keyboard.type(file_name)
  keyboard.press(Key.enter)
  keyboard.release(Key.enter)

def __parse_args__():
  global n_times, path, cmd, results_dir

  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('-r', '--repeat', help='The number of times to repeat the test [default: 1]')
  parser.add_argument('-ri', '--randomized-inputs', help='The inputs will be randomized? [default: false]', action='store_true')
  args = parser.parse_args()
  if args.repeat is not None:
    n_times = int(args.repeat)

  if args.randomized_inputs is True:
    path = ROOT_DIR + 'models/tensorflow/samples/core/get_started/randomized-inputs/'
    cmd = 'python3 {}/{}.py'.format(path, FILE_NAME)
    results_dir = CURRENT_DIR + '/' + ROOT_DIR + 'results/tensorflow/iris-dataset/randomized-inputs/'

def __run_tests__():
  global n_times, cmd
  import time
  started_total_time = datetime.datetime.now()

  for x in range(n_times):
    time.sleep(0.5)
    __clean_screen__()
    started = datetime.datetime.now()
    print('Starting at: ' + started.strftime('%Y-%m-%d %H:%M:%S'))
    subprocess.call(cmd, shell=True)
    finished = datetime.datetime.now()
    print('Finished at: ' + finished.strftime('%Y-%m-%d %H:%M:%S'))
    print('Total elapsed time: ' + str(finished-started))
    __open_dlg_save_output_as__()
    time.sleep(0.5)
    __save_output__(x+1)

  finished_total_time = datetime.datetime.now()
  print('Total elapsed time: ' + str(finished_total_time-started_total_time))

def main(*args):
  #__install_pynput__()
  __parse_args__()
  __run_tests__()

if __name__ == '__main__':
  import sys
  main(*sys.argv[1:])
