#!/usr/bin/python2
# coding: utf-8

import mnist_loader_with_pickle
import cnn

training_data, buf1, buf2 = \
    mnist_loader_with_pickle.load_data_wrapper()

net = cnn.CNN((4, 20, 1), (28, 28), output=False)
net.process(training_data)
