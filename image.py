
import sys
import serial
import struct
from PIL import Image
import numpy as np
port = 'COM4'
sp = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                   xonxoff=False, rtscts=False, stopbits=serial.STOPBITS_ONE, timeout=None, dsrdtr=True)
sp.setDTR(True)  # dsrdtr is ignored on Windows.
sp.write(b'snap')
sp.flush()
size = struct.unpack('<L', sp.read(4))[0]
img = sp.read(size)
sp.close()

with open("img.jpg", "wb") as f:
    f.write(img)

image = Image.open('img.jpg')
image.show()


def get_matriceR(image):
    matR = np.zeros((image.height, image.width), dtype=np.uint8)
    for i in range(image.height):
        for j in range(image.width):
            matR[i, j] = image.getpixel((j, i))[0]
    return matR


def get_matriceG(image):
    matG = np.zeros((image.height, image.width), dtype=np.uint8)
    for i in range(image.height):
        for j in range(image.width):
            matG[i, j] = image.getpixel((j, i))[1]
    return matG


def get_matriceB(image):
    matB = np.zeros((image.height, image.width), dtype=np.uint8)
    for i in range(image.height):
        for j in range(image.width):
            matB[i, j] = image.getpixel((j, i))[2]
    return matB


def affiche_image(image, pixelsR, pixelsG, pixelsB):
    array = np.zeros([image.height, image.width, 3], dtype=np.uint8)
    for i in range(image.height):
        for j in range(image.width):
            array[i, j] = (pixelsR[i, j], pixelsG
                           [i, j], pixelsB[i, j])
    img = Image.fromarray(array)
    img.show()


def affiche_matrice(image, matrice):
    for i in range(image.height):
        print(matrice[i])


affiche_matrice(image, get_matriceR(image))
# affiche_image(image, get_matriceR(image),
#               get_matriceG(image), get_matriceB(image))
# print(get_matriceR(image))
