import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


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


def cree_liste_RGB(nbr_image, nbr_pixel):
    liste_RGB = []
    for i in range(nbr_pixel):
        liste_RGB.append(([0]*nbr_image, [0]*nbr_image, [0]*nbr_image))
    return liste_RGB


def remplir_listes_RGB(iter, arg_liste_RGB, image, arg_liste_pixels):
    for i in range(len(arg_liste_pixels)):
        p = image.getpixel(arg_liste_pixels[i])
        arg_liste_RGB[i][0][iter] = p[0]  # pRi
        arg_liste_RGB[i][1][iter] = p[1]  # pGi
        arg_liste_RGB[i][2][iter] = p[2]  # pBi


def affiche_liste_RGB(liste_RGB, nbr_pixel):
    for i in range(nbr_pixel):
        for j in range(3):
            if j == 0:
                print('pR'+str(i+1))
            elif j == 1:
                print('pG'+str(i+1))
            else:
                print('pB'+str(i+1))
            print(liste_RGB[i][j])


def moyenne_colonne(matR, matG, matB):
    '''Permet d'obtenir la moyenne des valeurs RGB pour chaque colonne'''
    width = len(matR[0])
    height = len(matR)
    list_moyenne = ([0]*width, [0]*width, [0]*width)
    sommeR = 0
    sommeG = 0
    sommeB = 0
    for j in range(width):
        for i in range(height):
            sommeR += matR[i, j]
            sommeG += matG[i, j]
            sommeB += matB[i, j]
        list_moyenne[0][j] = sommeR/height
        list_moyenne[1][j] = sommeG/height
        list_moyenne[1][j] = sommeB/height
    return list_moyenne


def ligne_horizontale(matR, matG, matB, num_ligne):
    '''Permet d'obtenir les valeurs RGB d'une ligne '''
    width = len(matR[0])
    num_ligne -= 1
    ligne = ([0]*width, [0]*width, [0]*width)
    for j in range(width):
        ligne[0][j] = matR[num_ligne, j]
        ligne[1][j] = matG[num_ligne, j]
        ligne[2][j] = matB[num_ligne, j]
    return ligne


def enregistrer_liste_RGB(nom_fichier, liste_RGB, nbr_pixel=1):
    with open(nom_fichier + '.txt', "w") as f:
        for i in range(nbr_pixel):
            for j in range(3):
                if j == 0:
                    print('pR'+str(i+1), file=f)
                elif j == 1:
                    print('pG'+str(i+1), file=f)
                else:
                    print('pB'+str(i+1), file=f)
                print(liste_RGB[i][j], file=f)


def z_functionR(x, y, z, liste_RGB):
    for i in y:
        for j in x:
            z[i][j] = liste_RGB[i][0][j]
    return z


def z_functionG(x, y, z, liste_RGB):
    for i in y:
        for j in x:
            z[i][j] = liste_RGB[i][1][j]
    return z


def z_functionB(x, y, z, liste_RGB):
    for i in y:
        for j in x:
            z[i][j] = liste_RGB[i][2][j]
    return z


def plot_3D(liste_RGB, nbr_pixel, nbr_image, couleur='R'):
    x = np.arange(nbr_image)
    y = np.arange(nbr_pixel)
    z = np.zeros((nbr_pixel, nbr_image))
    X, Y = np.meshgrid(x, y)
    if couleur == 'R':
        Z = z_functionR(x, y, z, liste_RGB)
        couleur = 'red'
    elif couleur == 'G':
        Z = z_functionG(x, y, z, liste_RGB)
        couleur = 'green'
    elif couleur == 'B':
        Z = z_functionB(x, y, z, liste_RGB)
        couleur = 'blue'
    fig = plt.figure()
    ax = plt.axes(projection="3d")

    ax.plot_surface(X, Y, Z, color=couleur)
    ax.set_xlabel("nombre d'image")
    ax.set_ylabel('numéro du pixel')
    ax.set_zlabel('intensité lunineuse (R/G/B)')
    plt.show()
