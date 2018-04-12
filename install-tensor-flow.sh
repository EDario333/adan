#!/bin/bash

# Latest versions from 2018-04-12:
# Bazel: 0.12.0 (the last version is the 0.13.0, but it seems that still it's on developing). Please see the releases page: https://github.com/bazelbuild/bazel/releases
# numpy: 1.14.1
# six: 1.11.0
# pandas: 0.22.0
# TensorFlow: 1.8

# Next one is deprecated!
# Just here for past-reference. If you have any trouble with Bazel 0.13.0, try with this
install_bazel_0_11_0() {
#   From the sources I got the error message:
#   Building Bazel from scratch
#   ERROR: Must specify PROTOC if not bootstrapping from the distribution artifact

#   wget https://github.com/bazelbuild/bazel/archive/0.11.0.tar.gz
#   tar xvf bazel-0.11.0.tar.gz

#   Since you are bootstrapping Bazel on a system that does not have Bazel installed, you need to download the distribution artifact from.
#   Taken from: https://github.com/bazelbuild/bazel/issues/3801

  wget https://github.com/bazelbuild/bazel/releases/download/0.11.0/bazel-0.11.0-dist.zip

  mkdir bazel-0.11.0
  unzip bazel-0.11.0-dist.zip -d bazel-0.11.0
  cd bazel-0.11.0

  ./compile.sh
}

# The last version is the 0.13.0, but it seems that still it's on developing). Please see the releases page: https://github.com/bazelbuild/bazel/releases
# Use this one under your own consideration
install_bazel_0_13_0() {
  git clone https://github.com/bazelbuild/bazel.git
  git checkout release-0.13.0

  cd bazel

  ./compile.sh
}

install_bazel_0_12_0() {
#   From the sources I got the error message:
#   Building Bazel from scratch
#   ERROR: Must specify PROTOC if not bootstrapping from the distribution artifact

#   wget https://github.com/bazelbuild/bazel/archive/0.11.0.tar.gz
#   tar xvf bazel-0.11.0.tar.gz

#   Since you are bootstrapping Bazel on a system that does not have Bazel installed, you need to download the distribution artifact from.
#   Taken from: https://github.com/bazelbuild/bazel/issues/3801

  wget https://github.com/bazelbuild/bazel/releases/download/0.12.0/bazel-0.12.0-dist.zip

  mkdir bazel-0.12.0
  unzip bazel-0.12.0-dist.zip -d bazel-0.12.0
  cd bazel-0.12.0

  ./compile.sh
}

install_six_1_11_0() {
  wget https://pypi.python.org/packages/16/d8/bc6316cf98419719bd59c91742194c111b6f2e85abac88e496adefaf7afe/six-1.11.0.tar.gz#md5=d12789f9baf7e9fb2524c0c64f1773f8
  tar xvf six-1.11.0.tar.gz
  cd six-1.11.0
  python setup.py install
}

install_pandas_0_22_0() {
  wget https://files.pythonhosted.org/packages/08/01/803834bc8a4e708aedebb133095a88a4dad9f45bbaf5ad777d2bea543c7e/pandas-0.22.0.tar.gz
  tar xvf pandas-0.22.0.tar.gz
  cd pandas-0.22.0
  python setup.py install
}

install_tensor_flow_1_8() {
#   git clone https://github.com/tensorflow/tensorflow.git
  cd ~/virtualenvs/adan/adan/third-party/tensorflow
  git checkout r1.8
  ./configure

  pip install wheel
  pip install --upgrade pip
  bazel build --config=opt //tensorflow/tools/pip_package:build_pip_package
  bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
  # Documentation says run:
  # sudo pip install /tmp/tensorflow_pkg/*.whl
  # But I got the error: tensorflow-1.6.0-cp36-cp36m-linux_x86_64.whl is not a supported wheel on this platform
  # So I used:
  python3 -m pip install /tmp/tensorflow_pkg/tensorflow-1.8.0rc0-cp36-cp36m-linux_x86_64.whl
  # For more details please see: https://www.tensorflow.org/install/install_sources & https://stackoverflow.com/questions/33622613/tensorflow-installation-error-not-a-supported-wheel-on-this-platform
}

install_all() {
  mkdir third-party
  cd third-party

  install_bazel_0_12_0
  cd ..

  install_six_1_11_0
  cd ..

  install_pandas_0_22_0
  cd ..

  PATH=$PATH:~/virtualenvs/adan/adan/third-party/bazel-0.12.0/output/
  install_tensor_flow_1_8
}

install_all
