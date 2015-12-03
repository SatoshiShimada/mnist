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

    def feed_forward(self, data):
        for x, y in data:
            a = x.reshape((2, 1))
            for w, b in zip(self.weights, self.biases):
                a = sigmoid_vec(np.dot(w, a) + b)
            print x
            print np.argmax(a),
            print np.argmax(y)

    def train(self, training_data, epochs, mini_batch_size, learning_rate):
        for count in xrange(epochs):
            random.shuffle(training_data)
            mini_batches = [training_data[x: x+mini_batch_size] for x in xrange(0, len(training_data), mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, learning_rate)

    def update_mini_batch(self, mini_batch, learning_rate):
        N = len(mini_batch)

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
            buf = np.dot(self.weights[l-1], Z[l-1]) + np.dot(self.biases[l-1], np.ones((1, N))) 
            U[l-1] = buf
            Z[l] = sigmoid_vec(U[l-1])

        Y = Z[-1]

        # back propagation
        # calc error
        Delta = [np.zeros((l, N)) for l in self.layer[1:]]
        Delta[-1] = Y - D
        for l in xrange(2, self.num_layers):
            Delta[-l] = sigmoid_prime_vec(U[-l]) * np.dot(self.weights[-l+1].transpose(), Delta[-l+1])
        
        for l in xrange(1, self.num_layers):
            dw = (1/N) * np.dot(Delta[l - 1], Z[l - 1].transpose())
            db = (1/N) * np.dot(Delta[l - 1], np.ones((N, 1)))

            delta_w = -1.0 * learning_rate * dw
            delta_b = -1.0 * learning_rate * db
            self.weights[l-1] += delta_w
            self.biases[l-1] += delta_b

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def sigmoid_prime(x):
    return sigmoid(x) * (1.0 - sigmoid(x))

sigmoid_vec = np.vectorize(sigmoid)
sigmoid_prime_vec = np.vectorize(sigmoid_prime)
