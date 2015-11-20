#!/usr/bin/python2
# coding: utf-8

import numpy as np
import math

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

class Network():
    def __init__(self, layers):
        self.w = [np.random.randn(x[0], x[1]) for x in zip(layers[:-1], layers[1:])]
        self.b = [np.random.randn(1, x) for x in layers[1:]]

    def learning(self, train_data):
        """
        trainging by stochastic gradient descent and back propagation
        """
        for x in xrange(10):
            for data in train_data:
                self.backprop(data)

    def backprop(self, train_data):
        data = train_data[:-1]
        ideal = train_data[-1]
        hidden_weight = []
        for weight, bias in zip(self.w, self.b):
            buf = []
            for w, b in zip(weight.transpose(), bias[0]):
                buf.append(sigmoid((np.dot(w, data) + b).sum()))
            data = np.array(buf)
            hidden_weight.append(buf)
        error = (hidden_weight[-1] - ideal)[0]
        ## calculate error
        l = 1
        for weight, bias in zip(self.w[::-1], self.b[::-1]):
            buf = [w + error for w in weight]
            self.w[-l] = np.array(buf)
            l += l
        print self.w

    def feed_forward(self, train_data):
        for d in train_data:
            data = d[:-1]
            print data,
            for weight, bias in zip(self.w, self.b):
                hidden_weight = []
                for w, b in zip(weight.transpose(), bias[0]):
                    hidden_weight.append(sigmoid((np.dot(w, data) + b).sum()))
                data = np.array(hidden_weight)
            print hidden_weight
