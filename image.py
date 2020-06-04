
import sys
import serial
import struct
from PIL import Image
import numpy as np
import actions_image
port = 'COM4'
sp = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                   xonxoff=False, rtscts=False, stopbits=serial.STOPBITS_ONE, timeout=None, dsrdtr=True)
sp.setDTR(True)  # dsrdtr is ignored on Windows.

nbr = 1
liste_pixels = actions_image.cree_liste_pixel(nbr)

for i in range(nbr):
    sp.write(b'snap')
    sp.flush()
    size = struct.unpack('<L', sp.read(4))[0]
    img = sp.read(size)

    with open("img.jpg", "wb") as f:
        f.write(img)

    image = Image.open('img.jpg')
    actions_image.remplir_listes_pixels(
        i, liste_pixels, image, (164, 36), (35, 105), (162, 202), (285, 106))
    # image.show()
sp.close()
actions_image.affiche_liste_pixel(liste_pixels)

#affiche_matrice(image, get_matriceR(image))
# affiche_image(image, get_matriceR(image),
#               get_matriceG(image), get_matriceB(image))
# print(get_matriceR(image))
