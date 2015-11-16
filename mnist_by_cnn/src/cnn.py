#!/usr/bin/python2
# coding: utf-8

import numpy as np
import mnist_loader_with_pickle

import network

parameter_output = True

## Convolution

## create filter as random value
filter_size = 4
filter_count = 20
filter_channels = 1 # Gray scale image
w = np.random.randn(filter_count, filter_channels, filter_size, filter_size)
## create biases
biases = np.random.randn(filter_count, 1)

## load mnist data
training_data, validation_data, test_data = \
    mnist_loader_with_pickle.load_data_wrapper()

image_width = 28
image_height = 28
data = training_data[0][0].reshape((image_width, image_height))

fmapsize_width = image_width - 2 * int(filter_size / 2)
fmapsize_height = image_height - 2 * int(filter_size / 2)
filtered_data = []
for filters in w:
    for filter_ in filters:
        dat = []
        for n1 in xrange(fmapsize_height):
            for n2 in xrange(fmapsize_width):
                buf = [x[n2: n2+filter_size] for x in data[n1: n1+filter_size]]
                dat.append(np.dot(np.array(buf), filter_).sum())
        filtered_data.append(dat)

## feature maps (filter_count)
feature_maps = np.array(filtered_data)
if parameter_output == True:
    np.savetxt('../parameter/out1.csv', feature_maps, delimiter=',')

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
if parameter_output == True:
    np.savetxt('../parameter/out2.csv', feature_maps, delimiter=',')

## Added Biases
#output = feature_maps + biases (!!miss!! not list addition)
fmap_buf = []
for f, a in zip(feature_maps, biases):
    buf = []
    [ buf.append(x + a) for x in f]
    fmap_buf.append(buf)
feature_maps = np.array(fmap_buf)
if parameter_output == True:
    np.savetxt('../parameter/out3.csv', feature_maps, delimiter=',')

## Activation function
# sigmoid, tanh, ReLU
result = []
[result.append(network.sigmoid_vec(x)) for x in feature_maps]
feature_maps = np.array(result)
if parameter_output == True:
    np.savetxt('../parameter/out4.csv', feature_maps, delimiter=',')

