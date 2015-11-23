#!/usr/bin/python2
# coding: utf-8

import numpy as np

import network

class Logic():
    logic_and = [[np.array([0,0]), np.array([0])], [np.array([0,1]), np.array([0])], [np.array([1,0]) ,np.array([0])], [np.array([1,1]), np.array([1])]]
    logic_or = [[np.array([0,0]), np.array([0])], [np.array([0,1]), np.array([1])], [np.array([1,0]) ,np.array([1])], [np.array([1,1]), np.array([1])]]
    logic_exor = [[np.array([0,0]), np.array([0])], [np.array([0,1]), np.array([1])], [np.array([1,0]) ,np.array([1])], [np.array([1,1]), np.array([0])]]

class MNIST():
    def __init__(self):
        import mnist_loader_with_pickle as loader
        self.training_data, self.validation_data, self.test_data = loader.load_data_wrapper()

if __name__ == '__main__':
    if True:
        mnist = MNIST()
        train_data = mnist.training_data
        test_data  = mnist.test_data
        net = network.Network([784, 30, 10])
        net.train(train_data, epoch=300, mini_batch_size=30, learning_rate=0.4)
    else:
        data = Logic()
        ## create test data
        logic_and_test  = np.array(data.logic_and)
        logic_or_test   = np.array(data.logic_or)
        logic_exor_test = np.array(data.logic_exor)

        train_data = data.logic_or
        test_data  = logic_or_test

        net = network.Network([2,3,1])
        net.train(train_data, epoch=300, mini_batch_size=1, learning_rate=0.5)
        net.feed_forward(test_data)

