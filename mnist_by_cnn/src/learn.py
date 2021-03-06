#!/usr/bin/python2
# coding: utf-8

# import library
#import sys
#import numpy as np
# import my library
#import network
import mnist_loader_with_pickle
#import read
import cnn

if __name__ == '__main__':
    ## read mnist data
    training_data, validation_data, test_data = \
        mnist_loader_with_pickle.load_data_wrapper()
    #ball_data = read.load_ball()
    #training_data = training_data + ball_data

    ## create cnn
    nn = cnn.CNN((4, 20, 1), (28, 28), output=False)
    nn.process(training_data[0:11])

    ## create network
    ## input  layer: 784 (28 * 28)
    ## hidden layer: 30 * 1
    ## output layer: 11 (digits and ball)
    #net = network.Network([784, 30, 11])

    ## execute training
    #net.SGD(training_data, 30, 10, 3.0, test_data=test_data)

    #net.save_data()
    #net.evaluate(test_data)
