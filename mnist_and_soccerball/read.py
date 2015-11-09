
import numpy as np
try:
    import Image
except:
    from PIL import Image
import mnist_loader_with_pickle as loader

def load_image_rgb(filename, label):
    img = Image.open(filename)

    data = []
    width, height = img.size
    for y in range(height):
        for x in range(width):
            p = img.getpixel((x, y))
            data.append(p[0] * 0.2989 + p[1] * 0.5870 + p[2] * 0.1140)
    return (np.array(data), label)

def load_image(filename, label):
    img = Image.open(filename)

    data = []
    width, height = img.size
    for y in range(height):
        for x in range(width):
            p = img.getpixel((x, y))
            data.append(p[0])
    return (np.array(data), loader.vectorized_result(label))

def load_ball():
    ball_data = []
    for n in xrange(1260):
        filename = 'ball_image/ball_' + "%04d" % (n + 1) + '.png'
        ret = load_image(filename, 10)
        ret = (ret[0].reshape((784, 1)), ret[1])
        ball_data.append(ret)
    return ball_data
    
