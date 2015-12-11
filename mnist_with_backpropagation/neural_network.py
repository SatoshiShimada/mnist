#!/usr/bin/python2
# coding: utf-8

import numpy as np
import random
import sys

class Neural_Network(object):
    def __init__(self, layers):
        self.num_layers = len(layers)
        self.layer = layers
        self.weights = [np.random.randn(x, y) for x, y in zip(layers[1:], layers[:-1])]
        self.biases  = [np.random.randn(x, 1) for x in layers[1:]]
        self.test_data = None
        self.p = [0.9 for x in xrange(self.num_layers)]

    def set_test(self, test_data):
        self.test_data = test_data

    def feed_forward(self, data):
        count = 0
        for x, y in data:
            a = x.reshape((self.layer[0], 1))
            for w, b, delta_p in zip(self.weights, self.biases, self.p):
                w = w * delta_p
                a = sigmoid_vec(np.dot(w, a) + b)
            if np.argmax(a) == y:
                count += 1
        print "Result: [{0:d} / {1:d}] ({2:f}%)".format(count, len(data), 100.0 * count / len(data))

    def train(self, training_data, epochs, mini_batch_size, learning_rate):
        for count in xrange(epochs):
            random.shuffle(training_data)
            mini_batches = [training_data[x: x+mini_batch_size] for x in xrange(0, len(training_data), mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, learning_rate)
            print 'Epoch {0:d} done'.format(count)
            if self.test_data:
                self.feed_forward(self.test_data)

    def update_mini_batch(self, mini_batch, learning_rate):
        N = len(mini_batch)
        dropout_weight = []
        for count, x in zip(xrange(self.num_layers-1), self.p):
            div = 1 - x
            buf = self.weights[count]
            if div == 1:
                for x in xrange(self.layer[count] / div):
                    buf[np.random.randint(0, buf.shape(0))][np.random.randint(0, buf.shape(1))] = 0.0
            dropout_weight.append(buf)

        X = []
        D = []
        for x, d in mini_batch:
            X.append(x)
            D.append(d)
        X = np.array(X).reshape((self.layer[0], N))
        D = np.array(D).reshape((self.layer[-1], N))

        # feed forward
        U = [np.zeros((n, N)) for n in self.layer[1:]]
        Z = [np.zeros((n, N)) for n in self.layer]
        Z[0] = X
        for l in xrange(1, self.num_layers):
            #buf = np.dot(self.weights[l-1], Z[l-1]) + np.dot(self.biases[l-1], np.ones((1, N))) 
            buf = np.dot(dropout_weight[l-1], Z[l-1]) + np.dot(self.biases[l-1], np.ones((1, N))) 
            U[l-1] = buf
            Z[l] = sigmoid_vec(U[l-1])

        Y = Z[-1]

        # back propagation
        # calc error
        Delta = [np.zeros((l, N)) for l in self.layer[1:]]
        Delta[-1] = Y - D
        for l in xrange(2, self.num_layers):
            #Delta[-l] = sigmoid_prime_vec(U[-l]) * np.dot(self.weights[-l+1].transpose(), Delta[-l+1])
            Delta[-l] = sigmoid_prime_vec(U[-l]) * np.dot(dropout_weight[-l+1].transpose(), Delta[-l+1])
        
        prev_delta_w = [np.zeros((x, y)) for x, y in zip(self.layer[1:], self.layer[:-1])]
        prev_delta_b = [np.zeros((x, 1)) for x in self.layer[1:]]
        alpha = 0.5
        lambda_ = 0.0001
        for l in xrange(1, self.num_layers):
            dw = (1/N) * np.dot(Delta[l-1], Z[l-1].transpose())
            db = (1/N) * np.dot(Delta[l-1], np.ones((N, 1)))

            #delta_w = -1.0 * learning_rate * (dw + lambda_ * self.weights[l-1]) + alpha * prev_delta_w[l-1]
            delta_w = -1.0 * learning_rate * (dw + lambda_ * dropout_weight[l-1]) + alpha * prev_delta_w[l-1]
            delta_b = -1.0 * learning_rate * db + alpha * prev_delta_b[l-1]
            self.weights[l-1] += delta_w
            self.biases[l-1] += delta_b

            prev_delta_w.append(delta_w)
            prev_delta_b.append(delta_b)

    def save_parameter(self, path = 'parameter/'):
        for count in xrange(self.num_layers - 1):
            filename_w = "{0}weights{1:0>3}.csv".format(path, count)
            filename_b = "{0}biases{1:0>3}.csv".format(path, count)
            np.savetxt(filename_w, self.weights[count], delimiter=',')
            np.savetxt(filename_b, self.biases[count], delimiter=',')

    def load_parameter(self, path = 'parameter/'):
        for count in xrange(self.num_layers - 1):
            filename_w = "{0}weights{1:0>3}.csv".format(path, count)
            filename_b = "{0}biases{1:0>3}.csv".format(path, count)
            self.weights[count] = np.loadtxt(filename_w, delimiter=',')
            self.biases[count] = np.loadtxt(filename_b, delimiter=',').reshape((-1, 1))

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def sigmoid_prime(x):
    return sigmoid(x) * (1.0 - sigmoid(x))

sigmoid_vec = np.vectorize(sigmoid)
sigmoid_prime_vec = np.vectorize(sigmoid_prime)
