#!/usr/bin/python2
# coding: utf-8

import numpy as np

import neural_network as network
import mnist_loader_with_pickle as loader

import sys

if __name__ == '__main__':
    print 'network training'
    datapath = 'parameter/mnist_dropout/'
    #datapath = 'parameter/init_params/'

    training_data, validation_data, test_data = loader.load_data_wrapper()

    epochs = 50
    mini_batch_size = 1
    learning_rate = 0.01
    dropout_rate = (0.8, 0.9)

    net = network.Neural_Network([784, 30, 10], dropout_rate)
    net.set_test(test_data)
    net.set_validation(validation_data)
    train = True
    #train = False
    if train:
        #net.load_parameter(path=datapath)
        net.train(training_data, epochs, mini_batch_size, learning_rate)
        print 'save parameter? (y/n)'
        if 'y' in sys.stdin.readline():
            net.save_parameter(path=datapath)
            print 'Saved'
    else:
        net.load_parameter(path=datapath)
        net.feed_forward(test_data)
