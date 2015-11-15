#!/usr/bin/python2
# coding: utf-8

import numpy as np
import mnist_loader_with_pickle

## Convolution

## create filter as random value
filter_size = 4
filter_count = 2
filter_channels = 1 # Gray scale image
w = np.random.randn(filter_count, filter_channels, filter_size, filter_size)

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
#np.savetxt('out.csv', feature_maps, delimiter=',')

## Pooling
## Max-pooling
for data in feature_maps:
    fmap = data.reshape((fmapsize_width, fmapsize_height))
    for y in xrange(fmapsize_height):
        buf = fmap[y:y+1]
        for x in xrange(fmapsize_width):
            print buf[x:x+1]
