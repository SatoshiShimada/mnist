#!/usr/bin/python
# coding: utf-8

import network
import mnist_loader

if __name__ == '__main__':
    training_data, test_data =\
        mnist_loader.mnist_load_data()
    net = network.Network([784, 30, 10])
    net.SGD(training_data, 30, 10, 0.01, test_data=test_data)
