#!/bin/bash
#Install pip3
sudo apt install python3-pip
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
#Joblib
sudo pip3 install joblib