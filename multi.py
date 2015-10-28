#!/usr/bin/python2
# coding: utf-8

import network
import mnist_loader_with_pickle
import numpy as np
import read
import sys

if __name__ == '__main__':
    training_data, validation_data, test_data = \
        mnist_loader_with_pickle.load_data_wrapper()
    net = network.Network([784, 30, 10])
    #net.SGD(training_data, 30, 10, 3.0, test_data=test_data)
    img = read.load_image(sys.argv[1], int(sys.argv[2]))
    test_data = (img, )
    net.load_data()
    net.evaluate(test_data)
