
import numpy as np
try:
    import Image
except:
    from PIL import Image

def load_image(filename, label):
    img = Image.open(filename)

    data = []
    width, height = img.size
    for y in range(height):
        for x in range(width):
            p = img.getpixel((x, y))
            data.append(p[0] * 0.2989 + p[1] * 0.5870 + p[2] * 0.1140)
    return (np.array(data), label) # answer = 2
