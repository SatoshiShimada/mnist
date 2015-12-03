#!/usr/bin/python2
# coding: utf-8

import numpy as np
import sys
import copy

import neural_network as network

class Logic(object):
    logic_and  = [[[0, 0], 0], [[0, 1], 0], [[1, 0], 0], [[1, 1], 1]]
    logic_or   = [[[0, 0], 0], [[0, 1], 1], [[1, 0], 1], [[1, 1], 1]]
    logic_exor = [[[0, 0], 0], [[0, 1], 1], [[1, 0], 1], [[1, 1], 0]]

def vectorize(x):
    ret = np.zeros((2, 1))
    ret[x] = 1
    return ret

if __name__ == '__main__':
    print 'network training'
    logic = Logic()
    data = logic.logic_or

    training_data = [(np.array(x), vectorize(y)) for x, y in data]
    test_data     = [(np.array(x), y) for x, y in data]

    epochs = 300
    mini_batch_size = 1
    learning_rate = 1.0

    net = network.Neural_Network([2, 3, 2])
    net.train(training_data, epochs, mini_batch_size, learning_rate)
    net.feed_forward(test_data)
