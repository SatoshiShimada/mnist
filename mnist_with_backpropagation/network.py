#!/usr/bin/python2
# coding: utf-8

import random
import sys
import numpy as np

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def sigmoid_prime(x):
    return sigmoid(x) * (1.0 - sigmoid(x))

sigmoid_vec = np.vectorize(sigmoid)
sigmoid_prime_vec = np.vectorize(sigmoid_prime)

class Network():
    def __init__(self, layers):
        """
        initialize parameter of network
        """
        self.layers = len(layers)
        self.layer = layers
        self.w = [np.random.randn(x, y) for x, y in zip(layers[1:], layers[:-1])]
        self.b = [np.random.randn(x, 1) for x in layers[1:]]
        self.Errors = []

    def __del__(self):
        if self.Errors:
            data = np.array(self.Errors)
            #abs_vec = np.vectorize(lambda x: abs(x))
            #data = abs_vec(data)
            np.savetxt('errors.csv', data, delimiter=',')

    def train(self, training_data, epoch=10, mini_batch_size=2, learning_rate=0.5, error_log=False):
        """
        training for network parameter with training data
        """
        self.Error_log=error_log
        for count in xrange(epoch):
            #mini_batches = np.random.shuffle(training_data)
            random.shuffle(training_data)
            ## split traing sample for mini_batches
            mini_batch = [training_data[x:x + mini_batch_size] for x in xrange(0, len(training_data), mini_batch_size)]
            for m in mini_batch:
                self.update_mini_batch(m, learning_rate)
            print "Epoch [%d] done." % count

    def update_mini_batch(self, mini_batch, learning_rate):
        N = len(mini_batch)
        Ninv = 1.0 / len(mini_batch)
        rate = 0.5
        rate2 = 0.01

        U = [] # output before activation
        Z = [] # output after activation
        X = [] # input data for training
        D = [] # desire of output
        Y = [] # output of network
        for x, y in mini_batch:
            X.append(x)
            D.append(y)
        X = np.array(X).ravel().reshape((self.layer[0], N))
        Z.append(X)
        U.append(X)
        for l, w, b in zip(xrange(self.layers), self.w, self.b):
            U.append(np.dot(w, Z[l]) + np.dot(b, np.ones((1, N))))
            Z.append(sigmoid_vec(U[-1]))
        Y.append(Z[-1])
        Y = np.array(Y).reshape((self.layer[-1], N))
        D = np.array(D).reshape((self.layer[-1], N))

        ## Back propagation
        ## calculate delta
        Delta = [0] * self.layers
        Delta[-1] = Y - D
        if self.Error_log:
            self.Errors.append(sum(Y - D))
        for l in xrange(2, self.layers):
            active = sigmoid_prime_vec(U[-l])
            buf = np.dot(self.w[-l+1].transpose(), Delta[-l+1])
            Delta[-l] = np.multiply(active, buf)
        
        for l, w in zip(xrange(1, self.layers), self.w):
            dw = Ninv * np.dot(Delta[l], Z[l-1].transpose())
            db = Ninv * np.dot(Delta[l], np.ones((N, 1)))
            dw = -1.0 * dw * learning_rate
            db = -1.0 * db * learning_rate
            self.w[l-1] += dw
            self.b[l-1] += db

    def feed_forward(self, data):
        count = 0
        for x, y in data:
            for w, b in zip(self.w, self.b):
                x = sigmoid_vec(np.dot(w, x).reshape((-1, 1)) + b)
            if y == np.argmax(x):
                count += 1
        print "Test done."
        print "[ %d / %d ] : [%f%%]" % (count, len(data), float(count) / len(data) * 100)

    def save_parameter(self):
        path = "parameter/"
        for i in xrange(len(self.w)):
            np.savetxt(path + "weight%03d.csv" % i, self.w[i], delimiter=',')
        for i in xrange(len(self.b)):
            np.savetxt(path + "biases%03d.csv" % i, self.b[i], delimiter=',')

    def load_parameter(self):
        path = "parameter/"
        for i in xrange(len(self.w)):
            self.w[i] = np.loadtxt(path + "weight%03d.csv" % i, delimiter=',')
        for i in xrange(len(self.b)):
            self.b[i] = np.loadtxt(path + "biases%03d.csv" % i, delimiter=',')

