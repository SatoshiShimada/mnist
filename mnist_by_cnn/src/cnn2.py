#!/usr/bin/python2
# coding: utf-8

import numpy as np

class CNN():
    def __init__(self, image_size):
        """
        +-----------------------+
        | convolution layer1    |
        | max-pooling layer1    |
        +-----------------------+
        |           |           |
        |           V           |
        +-----------------------+
        | convolution layer2    |
        | max-pooling layer2    |
        +-----------------------+
        |           |           |
        |           V           |
        +-----------------------+
        | full-connected layer3 |
        +-----------------------+
        """
        self.image_size = image_size

    def convolution(self, data):
        ## convolution
        filtsize = 2
        fmap_size = [size - 2 * np.floor(filtsize / 2) for size in self.image_size]
        for y in xrange(fmap_size / 2):
            for x in xrange(fmap_size / 2):
                max(data[x * 2]
