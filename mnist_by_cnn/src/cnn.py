#!/usr/bin/python2
# coding: utf-8

import numpy as np
import mnist_loader_with_pickle

import network

class CNN():
    def __init__(self, flt, image_size, output=False):
        """
        arguments:
            flt: list of filter (filter_size, filter_count, filter_channels)
            image_size: input image_size
        """
        self.filter_size = flt[0]
        self.filter_count = flt[1]
        self.filter_channels = flt[2] # Gray scale image
        ## create filter as random value
        self.w = np.random.randn(self.filter_count, self.filter_channels, self.filter_size, self.filter_size)
        ## create biases
        self.biases = np.random.randn(self.filter_count, 1)
        ## image size
        self.image_width = image_size[0]
        self.image_height = image_size[1]
        ## flag of parameter save to file
        self.parameter_output = output

    def process(self, training_data):
        """
        Convolution and Pooling
        Add biases, activation function
        """
        #data = training_data[0][0].reshape((self.image_width, self.image_height))
        for train in training_data:
            data = train[0].reshape((self.image_width, self.image_height))

            ## Convolution
            fmapsize_width = self.image_width - 2 * int(self.filter_size / 2)
            fmapsize_height = self.image_height - 2 * int(self.filter_size / 2)
            filtered_data = []
            for filters in self.w:
                for filter_ in filters:
                    dat = []
                    for n1 in xrange(fmapsize_height):
                        for n2 in xrange(fmapsize_width):
                            buf = [x[n2: n2+self.filter_size] for x in data[n1: n1+self.filter_size]]
                            dat.append(np.dot(np.array(buf), filter_).sum())
                    filtered_data.append(dat)

            ## feature maps (filter_count)
            feature_maps = np.array(filtered_data)
            if self.parameter_output == True:
                np.savetxt('../parameter/out1.csv', feature_maps, delimiter=',')

#####################################################################
# TODO: sepalate convolution, pooling, biases and activation function
#####################################################################
            ## Pooling
            ## Max-pooling
            ## Window size: 2x2
            fmap_buf = []
            for data in feature_maps:
                fmap_out = []
                fmap = data.reshape((fmapsize_width, fmapsize_height))
                for y in xrange(fmapsize_height / 2):
                    y *= 2
                    buf1, buf2 = fmap[y:y+2]
                    buf = []
                    count = 0
                    for a in zip(buf1, buf2):
                        buf.append(a[0])
                        buf.append(a[1])
                        if (count % 2) == 1:
                            fmap_out.append(max(buf))
                            buf = []
                        count += 1
                fmap_buf.append(fmap_out)
            feature_maps = np.array(fmap_buf)
            if self.parameter_output == True:
                np.savetxt('../parameter/out2.csv', feature_maps, delimiter=',')

            ## Added Biases
            fmap_buf = []
            for f, a in zip(feature_maps, self.biases):
                buf = []
                [buf.append(x + a) for x in f]
                fmap_buf.append(buf)
            feature_maps = np.array(fmap_buf)
            if self.parameter_output == True:
                np.savetxt('../parameter/out3.csv', feature_maps, delimiter=',')

            ## Activation function
            # sigmoid, tanh, ReLU
            result = []
            [result.append(network.sigmoid_vec(x)) for x in feature_maps]
            feature_maps = np.array(result)
            if self.parameter_output == True:
                np.savetxt('../parameter/out4.csv', feature_maps, delimiter=',')

