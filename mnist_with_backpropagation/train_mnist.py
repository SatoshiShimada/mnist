#!/usr/bin/python2
# coding: utf-8

import numpy as np

import neural_network as network
import mnist_loader_with_pickle as loader

if __name__ == '__main__':
    print 'network training'
    datapath = 'parameter/momentum_before/'

    training_data, validation_data, test_data = loader.load_data_wrapper()

    epochs = 30
    mini_batch_size = 1
    learning_rate = 0.01

    net = network.Neural_Network([784, 30, 10])
    net.set_test(test_data)
    train = True
    #train = False
    if train:
        #net.load_parameter(path=datapath)
        net.load_parameter('parameter/init_params/')
        net.train(training_data, epochs, mini_batch_size, learning_rate)
        #net.save_parameter(path=datapath)
    else:
        net.load_parameter(path=datapath)
        net.feed_forward(test_data)
