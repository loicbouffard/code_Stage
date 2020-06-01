
import sys
import serial
import struct
from PIL import Image
import numpy as np
port = 'COM4'
sp = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                   xonxoff=False, rtscts=False, stopbits=serial.STOPBITS_ONE, timeout=None, dsrdtr=True)
sp.setDTR(True)  # dsrdtr is ignored on Windows.
nbr = 1
pR1 = [0]*nbr
pG1 = [0]*nbr
pB1 = [0]*nbr
pR2 = [0]*nbr
pG2 = [0]*nbr
pB2 = [0]*nbr
pR3 = [0]*nbr
pG3 = [0]*nbr
pB3 = [0]*nbr
pR4 = [0]*nbr
pG4 = [0]*nbr
pB4 = [0]*nbr


def listesPixels(i, image, x1, y1, x2, y2, x3, y3, x4, y4):
    p1 = image.getpixel((x1, y1))
    p2 = image.getpixel((x2, y2))
    p3 = image.getpixel((x3, y3))
    p4 = image.getpixel((x4, y4))
    pR1[i] = p1[0]
    pG1[i] = p1[1]
    pB1[i] = p1[2]

    pR2[i] = p2[0]
    pG2[i] = p2[1]
    pB2[i] = p2[2]

    pR3[i] = p3[0]
    pG3[i] = p3[1]
    pB3[i] = p3[2]

    pR4[i] = p4[0]
    pG4[i] = p4[1]
    pB4[i] = p4[2]


for i in range(nbr):
    sp.write(b'snap')
    sp.flush()
    size = struct.unpack('<L', sp.read(4))[0]
    img = sp.read(size)

    with open("img.jpg", "wb") as f:
        f.write(img)

    image = Image.open('img.jpg')
    listesPixels(i, image, 164, 36, 35, 105, 162, 202, 285, 106)
    # image.show()
sp.close()
print('pR1')
print(pR1)
print('pG1')
print(pG1)
print('pB1')
print(pB1)

print('pR2')
print(pR2)
print('pG2')
print(pG2)
print('pB2')
print(pB2)

print('pR3')
print(pR3)
print('pG3')
print(pG3)
print('pB3')
print(pB3)

print('pR4')
print(pR4)
print('pG4')
print(pG4)
print('pB4')
print(pB4)


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


#affiche_matrice(image, get_matriceR(image))
# affiche_image(image, get_matriceR(image),
#               get_matriceG(image), get_matriceB(image))
# print(get_matriceR(image))
