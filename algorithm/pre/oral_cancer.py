#!/usr/bin/env python 

from utils import utils as adan_utils

def processing(args=None):
  assert args is not None, 'The args are missed'

  # Nothing special to do!
  conf = adan_utils.parse_json_file(args.configuration_file)

  return args, conf
