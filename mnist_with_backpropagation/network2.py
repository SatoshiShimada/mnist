#!/usr/bin/python2
# coding: utf-8

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
        self.b = [np.random.randn(x) for x in layers[1:]]

    def train(self, training_data, mini_batch_size=2, learning_rate=0.5):
        mini_batches = np.random.shuffle(training_data)
        ## split traing sample for mini_batches
        mini_batch = [training_data[x:x + mini_batch_size] for x in xrange(0, len(training_data), mini_batch_size)]
        for m in mini_batch:
            self.update_mini_batch(m, learning_rate)

    def update_mini_batch(self, mini_batch, learning_rate):
        #Y = [] # Output values
        #D = [] # Desired values
        N = len(mini_batch)
        n = 0
        for x, desire in mini_batch:
            #D.append(desire) # desired value
            D = desire
            U = [x] # First value is input data
            Z = [x] # Output of input layer is input data
            for l, w, b in zip(xrange(1, self.layers), self.w, self.b):
                U.append(np.dot(w, Z[l-1]) + np.dot(b, np.ones(self.layer[l])))
                Z.append(sigmoid_vec(U[l]))
            #Y.append(Z[-1])
            Y = Z[-1]

            ## Back propagation
            Delta = [0] * (self.layers - 1)
            Delta[self.layers - 2] = D - Y[0]
            for l in xrange(self.layers - 2, 0, -1):
                dlt = np.multiply(sigmoid_prime_vec(U[l]), np.dot(self.w[l], Delta[l]))
                Delta[l - 1] = dlt
            
            print self.w
            print self.b
            print U
            print Y
            print 'Z:'
            print Z
            print 'delta:'
            print Delta
            for l, w in zip(xrange(1, self.layers), self.w):
                Ninv = 1.0 / self.layer[l]
                dw = np.multiply(Delta[l - 1] * Z[l - 1].transpose(), Ninv)
                db = np.multiply(Delta[l - 1] * np.ones(self.layer[l]), Ninv)
                dw = dw * learning_rate * -1
                print 'dw:'
                print dw
                db = db * learning_rate * -1
                print '-------'
                print self.w[l - 1]
                print dw
                self.w[l - 1] += dw
                self.b[l - 1] += db
            n += 1

    def view(self):
        print 'weights:'
        print self.w
        print 'biases:'
        print self.b
