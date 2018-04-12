#!/bin/bash

# Latest versions from 2018-04-12:
# TensorFlow: 1.8

cd third-party/tensorflow
git clone https://github.com/tensorflow/models.git
cd models
git checkout v1.8.0
