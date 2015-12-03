#!/usr/bin/python2
# coding: utf-8

import numpy as np
import sys

import network_nnadl_modify as network

class Logic():
    logic_and  = [[[0, 0], 0], [[0, 1], 0], [[1, 0], 0], [[1, 1], 1]]
    logic_or   = [[[0, 0], 0], [[0, 1], 1], [[1, 0], 1], [[1, 1], 1]]
    logic_exor = [[[0, 0], 0], [[0, 1], 1], [[1, 0], 1], [[1, 1], 0]]

class MNIST():
    def __init__(self):
        import mnist_loader_with_pickle as loader
        self.training_data, self.validation_data, self.test_data = loader.load_data_wrapper()

def vectorized(x):
    a = np.zeros((2, 1))
    a[x] = 1.0
    return a

if __name__ == '__main__':
    is_mnist = True

    ## MNIST dataset
    if is_mnist:
        mnist = MNIST()
        train_data = mnist.training_data
        test_data  = mnist.test_data
        net = network.Network([784, 30, 10])

        net.SGD(train_data, 30, 10, 3.0, test_data=test_data)
        #net.SGD(train_data, 1, 10, 2.0, test_data=test_data)
    ## LOGIC dataset
    else:
        data = Logic()
        ## create test data
        #buf = data.logic_and
        buf = data.logic_or
        #buf = data.logic_exor
        train_data = [[np.array(x).reshape((2, 1)), vectorized(y)] for x, y in buf]
        test_data = [[np.array(x).reshape((2, 1)), y] for x, y in buf]

        net = network.Network([2,3,2])
        net.SGD(train_data, 500, 1, 0.5, test_data=test_data)

