
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
            self.save_data()
            self.load_data()
            if test_data:
                print( "Epoch {0}: {1} / {2}".format(j, self.evaluate(test_data), n_test))
            #else:
            #    print("Epoch {0} complete".format(j))

    def update_mini_batch(self, mini_batch, eta):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w-(eta/len(mini_batch))*nw
                for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(eta/len(mini_batch))*nb
                for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        activation = x
        activations = [x]
        zs = []
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid_vec(z)
            activations.append(activation)

        delta = self.cost_derivative(activations[-1], y) * \
                sigmoid_prime_vec(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())

        for l in xrange(2, self.num_layers):
            z = zs[-l]
            spv = sigmoid_prime_vec(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * spv
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        #test_results = [(np.argmax(self.feedforward(x)), y)
        #       for (x, y) in test_data]
        #return sum(int(x == y) for (x, y) in test_results)
        for (x, y) in test_data:
            print "label: " + str(y),
            x = x.reshape((784, 1))
            a = np.argmax(self.feedforward(x))
            print "result: " + str(a)
            plt.imshow(x.reshape((28, 28)))
            plt.gray()
            plt.show()

    def cost_derivative(self, output_activations, y):
        return (output_activations-y)

    def save_data(self):
        #np.save('biases.npy', self.biases)
        #np.save('weights.npy', self.weights)
        np.savetxt('biases1.csv', self.biases[0], delimiter=',')
        np.savetxt('weights1.csv', self.weights[0], delimiter=',')
        np.savetxt('biases2.csv', self.biases[1], delimiter=',')
        np.savetxt('weights2.csv', self.weights[1], delimiter=',')

    def load_data(self):
        #self.biases = np.load('biases.npy')
        #self.weights = np.load('weights.npy')
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

