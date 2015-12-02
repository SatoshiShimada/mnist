
import random
import numpy as np
import matplotlib.pyplot as plt

class Network():
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = sigmoid_vec(np.dot(w, a) + b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        if test_data: n_test = len(test_data)
        n = len(training_data)
        for j in xrange(epochs):
            random.shuffle(training_data)
            mini_batches = [
                    training_data[k:k+mini_batch_size]
                    for k in xrange(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                print( "Epoch {0}: {1} / {2}".format(j, self.evaluate(test_data), n_test))
            else:
                print("Epoch {0} complete".format(j))

    def update_mini_batch(self, mini_batch, learning_rate):
        N = len(mini_batch)
        #nabla_b = [np.zeros(b.shape) for b in self.biases]
        #nabla_w = [np.zeros(w.shape) for w in self.weights]
        #######
        ## X ##
        ## D ##
        #######
        X = []
        D = []
        for x, y in mini_batch:
            X.append(x)
            D.append(y)
        X = np.array(X).reshape((self.sizes[0], N)) # 784: number of neuron of input layer
        D = np.array(D).reshape((self.sizes[-1], N)) # 10: number of neuron of output layer

        #######
        ## U ##
        ## Z ##
        #######
        U = [X]
        Z = [X]
        for x in xrange(1, self.num_layers):
            U.append(np.dot(self.weights[x - 1], Z[x - 1]) + np.dot(self.biases[x - 1], np.ones((1, N))))
            Z.append(sigmoid_vec(U[-1]))
        #######
        ## Y ##
        #######
        Y = Z[-1]

        Delta = [np.zeros(w.shape) for w in self.weights]
        #Delta[-1] = self.cost_derivative(D, Y)
        Delta[-1] = self.cost_derivative(Y, D)
        for x in xrange(1, self.num_layers - 1):
            Delta[-x-1] = sigmoid_prime_vec(U[-x-1]) * np.dot(self.weights[-x].transpose(), Delta[-x])

        for x in xrange(1, self.num_layers):
            dw = (1/N) * np.dot(Delta[x - 1], Z[x - 1].transpose())
            db = (1/N) * np.dot(Delta[x - 1], np.ones((N, 1)))
            dw = learning_rate * dw * (-1.0)
            db = learning_rate * db * (-1.0)
            self.weights[x - 1] += dw
            self.biases[x - 1] += db

    def evaluate(self, test_data):
        test_results = [(np.argmax(self.feedforward(x)), y)
               for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        return (output_activations-y)

    def save_data(self):
        np.savetxt('biases1.csv', self.biases[0], delimiter=',')
        np.savetxt('weights1.csv', self.weights[0], delimiter=',')
        np.savetxt('biases2.csv', self.biases[1], delimiter=',')
        np.savetxt('weights2.csv', self.weights[1], delimiter=',')

    def load_data(self):
        self.biases[0] = np.loadtxt('biases1.csv', delimiter=',')
        self.biases[0] = self.biases[0].reshape((30, 1))
        self.weights[0] = np.loadtxt('weights1.csv', delimiter=',')
        self.biases[1] = np.loadtxt('biases2.csv', delimiter=',')
        self.biases[1] = self.biases[1].reshape((10, 1))
        self.weights[1] = np.loadtxt('weights2.csv', delimiter=',')

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

sigmoid_vec = np.vectorize(sigmoid)

def sigmoid_prime(z):
    return sigmoid(z)*(1-sigmoid(z))

sigmoid_prime_vec = np.vectorize(sigmoid_prime)

