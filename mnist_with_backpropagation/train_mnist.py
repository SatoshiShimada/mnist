#!/usr/bin/python2
# coding: utf-8

import numpy as np
import sys

import neural_network as network
import mnist_loader_with_pickle as loader

def vectorize(x):
    ret = np.zeros((2, 1))
    ret[x] = 1
    return ret

if __name__ == '__main__':
    print 'network training'

    training_data, validation_data, test_data = loader.load_data_wrapper()

    epochs = 1
    mini_batch_size = 10
    learning_rate = 2.0

    net = network.Neural_Network([784, 30, 10])
    net.train(training_data, epochs, mini_batch_size, learning_rate)
    net.feed_forward(test_data)
