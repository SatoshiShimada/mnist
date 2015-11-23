#!/usr/bin/python2

import numpy as np

if False:
    import network as network
    logic_and = np.array(((0.0, 0.0, 0.0), (0.0, 1.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 1.0)))
    net = network.Network([2,3,1])
    net.learning(np.array(logic_and))
    net.feed_forward(logic_and)
elif False:
    import network2 as network
    logic_and = [[np.array([1,2]), 1], [np.array([3,4]), 2]]
    net = network.Network([2,3,1])
    net.train(logic_and)
else:
    import network3 as network
    logic_and = [[np.array([0,0]), np.array([0])], [np.array([0,1]), np.array([0])], [np.array([1,0]) ,np.array([0])], [np.array([1,1]), np.array([1])]]
    logic_and_test = np.array(logic_and)
    net = network.Network([2,3,1])
    net.train(logic_and, epoch=500, mini_batch_size=1, learning_rate=0.5)
    net.feed_forward(logic_and_test)
