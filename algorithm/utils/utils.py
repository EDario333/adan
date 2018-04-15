#!/usr/bin/env python

import os
import datetime

ROOT_DIR = '../'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

results_dir = CURRENT_DIR + '/' + ROOT_DIR + 'results/'

def open_dlg_save_output_as():
  from pynput.keyboard import Key, Controller
  keyboard = Controller()

  with keyboard.pressed(Key.ctrl):
    keyboard.press(Key.shift)
    keyboard.press('s')
    keyboard.release(Key.shift)
    keyboard.release('s')

def clean_screen():
  from pynput.keyboard import Key, Controller
  keyboard = Controller()

  with keyboard.pressed(Key.ctrl):
    keyboard.press(Key.shift)
    keyboard.press('k')
    keyboard.release(Key.shift)
    keyboard.release('k')

def save_output(filename, consecutive=1):
  global results_dir
  now = datetime.datetime.now()

  from pynput.keyboard import Key, Controller
  keyboard = Controller()
  file_name = results_dir + str(consecutive) + '-' + filename + ' ('
  file_name += now.strftime('%Y-%m-%d_%H-%M-%S') + ').html'
  keyboard.type(file_name)
  keyboard.press(Key.enter)
  keyboard.release(Key.enter)
