#!/usr/bin/python2
# coding: utf-8

import numpy as np

import network3 as network

logic_and = [[np.array([0,0]), np.array([0])], [np.array([0,1]), np.array([0])], [np.array([1,0]) ,np.array([0])], [np.array([1,1]), np.array([1])]]
logic_and_test = np.array(logic_and)
net = network.Network([2,3,1])
net.train(logic_and, epoch=500, mini_batch_size=1, learning_rate=0.5)
net.feed_forward(logic_and_test)

