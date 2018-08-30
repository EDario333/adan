#!/usr/bin/env python

from abc import ABCMeta, abstractmethod

class Parser:
  __metaclass__ = ABCMeta
  dataframe = None

  def __init__(self, dataframe=None):
    assert dataframe is not None, 'Please specify the dataframe to parse'
    self.dataframe = dataframe

  @abstractmethod
  def parse(self):
    pass
