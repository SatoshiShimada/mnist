#!/usr/bin/python2
# coding: utf-8

import numpy as np
import sys

import network_nnadl as network

class Logic():
    logic_and = [[np.array([0,0]), np.array([1, 0])], [np.array([0,1]), np.array([1, 0])], [np.array([1,0]) ,np.array([1, 0])], [np.array([1,1]), np.array([0, 1])]]
    logic_or = [[np.array([0,0]), np.array([1, 0])], [np.array([0,1]), np.array([0, 1])], [np.array([1,0]) ,np.array([0, 1])], [np.array([1,1]), np.array([0, 1])]]
    logic_exor = [[np.array([0,0]), np.array([1, 0])], [np.array([0,1]), np.array([0, 1])], [np.array([1,0]) ,np.array([0, 1])], [np.array([1,1]), np.array([1, 0])]]

class MNIST():
    def __init__(self):
        import mnist_loader_with_pickle as loader
        self.training_data, self.validation_data, self.test_data = loader.load_data_wrapper()

if __name__ == '__main__':
    is_mnist = True

    ## MNIST dataset
    if is_mnist:
        mnist = MNIST()
        train_data = mnist.training_data
        test_data  = mnist.test_data
        net = network.Network([784, 30, 10])

        #net.SGD(train_data, 30, 10, 3.0, test_data=test_data)
        net.SGD(train_data, 1, 10, 3.0, test_data=test_data)
    ## LOGIC dataset
    else:
        data = Logic()
        ## create test data
        logic_and_test  = np.array([(x, np.argmax(y)) for x, y in data.logic_and])
        logic_or_test  = np.array([(x, np.argmax(y)) for x, y in data.logic_or])
        logic_exor_test  = np.array([(x, np.argmax(y)) for x, y in data.logic_exor])

        #train_data = data.logic_or
        #test_data  = logic_or_test
        #train_data = data.logic_and
        #test_data  = logic_and_test
        train_data = data.logic_exor
        test_data  = logic_exor_test

        net = network.Network([2,3,2])
        net.SGD(train_data, 200, 1, 3.0, test_data=test_data)

