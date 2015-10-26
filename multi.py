#!/usr/bin/python
# coding: utf-8

import network
# import mnist_loader
import mnist_loader_with_pickle

if __name__ == '__main__':
    # training_data, test_data = mnist_loader.mnist_load_data()
    training_data, validation_data, test_data = \
        mnist_loader_with_pickle.load_data_wrapper()
    net = network.Network([784, 30, 10])
    net.SGD(training_data, 30, 10, 3.0, test_data=test_data)
