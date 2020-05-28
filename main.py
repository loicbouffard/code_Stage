import serial
import time
import numpy as np
from PIL import Image
import json


def affiche_image(pixelsR, pixelsG, pixelsB):
    array = np.zeros([240, 320, 3], dtype=np.uint8)
    for i in range(240):
        for j in range(320):
            array[i, j] = (pixelsR[i][j], pixelsG
                           [i][j], pixelsB[i][j])
    img = Image.fromarray(array)
    img.show()


def convert_tuple(pixelsR, pixelsG, pixelsB):
    pixels = []
    listTemp = []
    for i in range(240):
        for j in range(320):
            tuplePixel = (pixelsR[i][j], pixelsG
                          [i][j], pixelsB[i][j])
            listTemp.append(tuplePixel)
        pixels.append(listTemp)
    return np.array(pixels, dtype=np.uint8)


if __name__ == "__main__":
    port = serial.Serial('COM4', baudrate=115200)
    port.reset_input_buffer()
    pixelsR = []
    pixelsG = []
    pixelsB = []
    port.write(b'0101')
    time.sleep(0.04)

    k = 0
    while(len(pixelsB) != 240):
        p = port.readline()
        # print(p)
        if k == 0:
            pixelsR.append(json.loads(p))
            k = 1
        elif k == 1:
            pixelsG.append(json.loads(p))
            k = 2
        else:
            pixelsB.append(json.loads(p))
            k = 0
    print('fin recolte données')

    affiche_image(pixelsR, pixelsG, pixelsB)

    port.close()
