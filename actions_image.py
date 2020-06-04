import numpy as np
from PIL import Image


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


def cree_liste_pixel(nbr):
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
    return [(pR1, pG1, pB1), (pR2, pG2, pB2), (pR3, pG3, pB3), (pR4, pG4, pB4)]


def remplir_listes_pixels(i, liste_matrice, image, pos1, pos2, pos3, pos4):
    p1 = image.getpixel(pos1)
    p2 = image.getpixel(pos2)
    p3 = image.getpixel(pos3)
    p4 = image.getpixel(pos4)

    liste_matrice[0][0][i] = p1[0]  # pR1
    liste_matrice[0][1][i] = p1[1]  # pG1
    liste_matrice[0][2][i] = p1[2]  # pB1

    liste_matrice[1][0][i] = p2[0]  # pR2
    liste_matrice[1][1][i] = p2[1]  # pG2
    liste_matrice[1][2][i] = p2[2]  # pB2

    liste_matrice[2][0][i] = p3[0]  # pR3
    liste_matrice[2][1][i] = p3[1]  # pG3
    liste_matrice[2][2][i] = p3[2]  # pB3

    liste_matrice[3][0][i] = p4[0]  # pR4
    liste_matrice[3][1][i] = p4[1]  # pG4
    liste_matrice[3][2][i] = p4[2]  # pB4


def affiche_liste_pixel(liste_pixels):
    print('pR1')
    print(liste_pixels[0][0])
    print('pG1')
    print(liste_pixels[0][1])
    print('pB1')
    print(liste_pixels[0][2])

    print('pR2')
    print(liste_pixels[1][0])
    print('pG2')
    print(liste_pixels[1][1])
    print('pB2')
    print(liste_pixels[1][2])

    print('pR3')
    print(liste_pixels[2][0])
    print('pG3')
    print(liste_pixels[2][1])
    print('pB3')
    print(liste_pixels[2][2])

    print('pR4')
    print(liste_pixels[3][0])
    print('pG4')
    print(liste_pixels[3][1])
    print('pB4')
    print(liste_pixels[3][2])
