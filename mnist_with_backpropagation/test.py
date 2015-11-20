import network

import numpy as np

logic_and = np.array( \
    ((0.0, 0.0, 0.0), (0.0, 1.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 1.0)))
net = network.Network([2,3,1])
net.learning(np.array(logic_and))

net.feed_forward(logic_and)
