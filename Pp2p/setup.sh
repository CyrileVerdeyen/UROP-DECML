#!/bin/bash
#Scikit learn
sudo pip3 install -U scikit-learn
#Twisted
sudo pip3 install twisted
#Data file
sudo yum install wget
wget -O data.tar.gz "http://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"
tar -C ./tests -xvzf data.tar.gz
#Numpy
sudo pip3 install numpy