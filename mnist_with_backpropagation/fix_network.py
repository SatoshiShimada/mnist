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

    def train(self, training_data, epoch=10, mini_batch_size=2, learning_rate=0.5):
        """
        training for network parameter with training data
        """
        for count in xrange(epoch):
            mini_batches = np.random.shuffle(training_data)
            ## split traing sample for mini_batches
            mini_batch = [training_data[x:x + mini_batch_size] for x in xrange(0, len(training_data), mini_batch_size)]
            for m in mini_batch:
                self.update_mini_batch(m, learning_rate)

    def update_mini_batch(self, mini_batch, learning_rate):
        N = len(mini_batch)
        Ninv = 1.0 / len(mini_batch)
        U = []
        Z = []
        Y = []
        D = []
        for x, desire in mini_batch:
            u = [x] # First value is input data
            z = [x] # Output of input layer is input data
            for l, w, b in zip(xrange(1, self.layers), self.w, self.b):
                u.append(np.dot(w, z[l - 1]) + np.dot(b, np.ones(self.layer[l])))
                z.append(sigmoid_vec(u[l]))
            D.append(desire.ravel())
            Y.append(z[-1].ravel())
            U.append(u)
            Z.append(z)

        Y = np.array(Y)
        D = np.array(D)

        Ubuf = []
        Zbuf = []
        for x in xrange(self.layers):
            Ubuf.append([])
            Zbuf.append([])
        for u, z in zip(U, Z):
            i = 0
            for a, b in zip(u, z):
                Ubuf[i].append(a)
                Zbuf[i].append(b)
                i += 1
        U = []
        Z = []
        for u, z in zip(Ubuf, Zbuf):
            U.append(np.reshape(np.concatenate(u), (N, -1)).transpose())
            Z.append(np.reshape(np.concatenate(z), (N, -1)).transpose())

        ## Back propagation
        ## calculate delta
        Delta = [0] * self.layers
        Delta[-1] = np.subtract(D, Y).transpose()
        for l in xrange(self.layers - 2, 0, -1):
            active = sigmoid_prime_vec(U[l])
            buf = np.dot(self.w[l].transpose(), Delta[l + 1])
            dlt = np.multiply(active, buf)
            Delta[l] = dlt
        
        for l, w in zip(xrange(1, self.layers), self.w):
            dw = np.multiply(np.dot(Delta[l], Z[l - 1].transpose()), Ninv)
            db = np.multiply(np.dot(Delta[l], np.ones(N)), Ninv)
            dw = dw * learning_rate * -1.0
            db = db * learning_rate * -1.0
            self.w[l - 1] += dw
            self.b[l - 1] += db

    def feed_forward(self, data):
        for x, y in data:
            print x,
            for w, b in zip(self.w, self.b):
                x = sigmoid_vec(np.dot(w, x) + b)
            print y,
            print x

    def save_parameter(self):
        path = "parameter/"
        for i in xrange(len(self.w)):
            np.savetxt(path + "weight%03d.csv" % i, self.w[i], delimiter=',')
        for i in xrange(len(self.b)):
            np.savetxt(path +"biases%03d.csv" % i, self.b[i], delimiter=',')

    def load_parameter(self):
        path = "parameter/"
        for i in xrange(len(self.w)):
            self.w[i] = np.loadtxt(path + "weight%03d.csv" % i, delimiter=',')
        for i in xrange(len(self.b)):
            self.b[i] = np.loadtxt(path + "biases%03d.csv" % i, delimiter=',')

