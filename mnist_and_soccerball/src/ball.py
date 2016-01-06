#!/usr/bin/python2
# coding: utf-8

# import library
import numpy as np
# import my library
import network
import mnist_loader_with_pickle
import read

def evaluate_from_file(filename):
    ## read mnist data
    #training_data, validation_data, test_data = \
    #    mnist_loader_with_pickle.load_data_wrapper()
    ## load training data of ball from image
    #ball_data = read.load_ball()
    #training_data = training_data + ball_data

    ###########################################
    ## create network                        ##
    ## input  layer: 784 (28 * 28)           ##
    ## hidden layer: 30 * 1                  ##
    ## output layer: 11 (digits and ball)    ##
    ###########################################
    #net = network.Network([784, 30, 11])
    net = network.Network([784, 100, 10])

    ## execute training
    #net.SGD(training_data, 30, 10, 3.0, test_data=test_data)
    #net.save_data()
    #net.evaluate(test_data)

    net.load_data()
    data = read.load_image_rgb(filename, 0)
    ret = net.evaluate_data(data)

    return ret

if __name__ == '__main__':
    import sys
    ret = evaluate_from_file(sys.argv[1])
    print "%d,%f" % (ret[0], ret[1])

