
import numpy as np
import image

def load_image(filename, label):
    pic_size = (28, 28)
    img = image.image(filename)

    img.resize(pic_size)
    data = []
    width, height = (pic_size)
    for y in range(height):
        for x in range(width):
            p = img.img.getpixel((x, y))
            data.append(p[0] * 0.2989 + p[1] * 0.5870 + p[2] * 0.1140)
    return (np.array(data), label)
