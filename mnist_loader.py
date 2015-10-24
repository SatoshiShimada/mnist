#!/usr/bin/python
# coding: utf-8

import binascii
import numpy as np

def load_data_from_file():
    filenames = (
        'train-images-idx3-ubyte',
        'train-labels-idx1-ubyte',
        't10k-images-idx3-ubyte',
        't10k-labels-idx1-ubyte')
    magic_number_dict = {
        'train-images': '00000803',
        'train-lables': '00000801',
        'test-images' : '00000803',
        'test-lables' : '00000801' }
    tr_img = [] # training images
    tr_lbl = [] # training lables
    te_img = [] # test images
    te_lbl = [] # test lables
    for filename in filenames:
        data = []
        f = open(filename, 'rb')
        # read header
        buf = binascii.hexlify(f.read(4))
        if buf == magic_number_dict['train-images']:
            number_of_item = int(
                binascii.hexlify(f.read(4)), 16)
            number_of_rows = int(
                binascii.hexlify(f.read(4)), 16)
            number_of_columns = int(
                binascii.hexlify(f.read(4)), 16)
            tr_img = data
        elif buf == magic_number_dict['train-lables']:
            number_of_item = int(
                binascii.hexlify(f.read(4)), 16)
            tr_lbl = data
        elif buf == magic_number_dict['test-images']:
            number_of_item = int(
                binascii.hexlify(f.read(4)), 16)
            number_of_rows = int(
                binascii.hexlify(f.read(4)), 16)
            number_of_columns = int(
                binascii.hexlify(f.read(4)), 16)
            te_img = data
        elif buf == magic_number_dict['test-lables']:
            number_of_item = int(
                binascii.hexlify(f.read(4)), 16)
            te_lbl = data
        # read data (pixel or label)
        print number_of_item
        if buf == magic_number_dict['train-images'] or\
           buf == magic_number_dict['test-images' ]:
            for n in range(number_of_item):
                data_list = []
                for i in range(number_of_rows * number_of_columns):
                    read_data = binascii.hexlify(f.read(1))
                    data_list.append(int(read_data, 16))
                data.append(data_list)
            print number_of_rows,
            print number_of_columns
        else:
            for n in range(number_of_item):
                read_data = binascii.hexlify(f.read(1))
                data.append(int(read_data, 16))
        f.close()
        print ""
    return (tr_img, tr_lbl, te_img, te_lbl)

def mnist_load_data():
    data = load_data_from_file()
    training_inputs = [np.reshape(x, (784, 1)) for x in data[0]]
    training_results = [vectorized_result(y) for y in data[1]]
    training_data = zip(training_inputs, training_results)
    test_inputs = [np.reshape(x, (784, 1)) for x in data[2]]
    test_data = zip(test_inputs, data[3])
    return (training_data, test_data)

def vectorized_result(j):
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e

