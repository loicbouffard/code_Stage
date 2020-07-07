import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import serial
import serial.tools.list_ports
import time


def list_port():
    '''Retourne une liste des noms des ports séries disponible.'''
    list_port = []
    for port in serial.tools.list_ports.comports():
        list_port.append(port[0])
    return list_port


def init_port(nom):
    '''Crée objet port série et le retourne.'''
    sp = serial.Serial(nom, 1000000)
    sp.timeout = 0.4
    return sp


def capture(sp):
    '''Envoie la commande de capture à au capteur'''
    time.sleep(1)
    size = int(sp.readline().decode('utf-8'))

    img = sp.read(size)

    with open("img_ARDUCAM.jpg", "wb") as f:
        f.write(img)
    sp.reset_input_buffer()
    return Image.open('img_ARDUCAM.jpg')


def get_matriceR(image):
    '''Permet d'obtenir la matrice de pixels Rouge de l'image'''
    matR = np.zeros((image.height, image.width), dtype=np.uint8)
    for i in range(image.height):
        for j in range(image.width):
            matR[i, j] = image.getpixel((j, i))[0]
    return matR


def get_matriceG(image):
    '''Permet d'obtenir la matrice de pixels Verte de l'image'''
    matG = np.zeros((image.height, image.width), dtype=np.uint8)
    for i in range(image.height):
        for j in range(image.width):
            matG[i, j] = image.getpixel((j, i))[1]
    return matG


def get_matriceB(image):
    '''Permet d'obtenir la matrice de pixels Bleue de l'image'''
    matB = np.zeros((image.height, image.width), dtype=np.uint8)
    for i in range(image.height):
        for j in range(image.width):
            matB[i, j] = image.getpixel((j, i))[2]
    return matB


def affiche_image(pixelsR, pixelsG, pixelsB):
    '''Permet de reconstruire et d'afficher une image à partir des matrices de couleurs Rouge, Verte, Bleue'''
    height = len(pixelsR)
    width = len(pixelsR[0])
    array = np.zeros([height, width, 3], dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            array[i, j] = (pixelsR[i, j], pixelsG
                           [i, j], pixelsB[i, j])
    img = Image.fromarray(array)
    img.show()


def affiche_matrice(matrice):
    '''Permet d'afficher les valeurs d'une matrice selon une perspective horizontale'''
    for i in range(len(matrice)):
        print(matrice[i])


def cree_liste_RGB(nbr_image, nbr_pixel):
    '''Crée une liste de tuples qui contient des listes
    le nombre de tuples correspond au nombre de pixels analysés, les tuples sont des
    triplets qui correspond au trois couleurs RGB du pixel, les listes contenues dans
    les triplets correspondes au nombre d'images capturées (soit la valeur de l'intensité du pixel (R/G/B) de la n capture) '''
    liste_RGB = []
    for i in range(nbr_pixel):
        liste_RGB.append(([0]*nbr_image, [0]*nbr_image, [0]*nbr_image))
    return liste_RGB


def remplir_listes_RGB(iter, arg_liste_RGB, image, arg_liste_pixels):
    '''Permet de remplir une liste RGB à partir d'une image et d'une liste de pixels choisit'''
    for i in range(len(arg_liste_pixels)):
        p = image.getpixel(arg_liste_pixels[i])
        arg_liste_RGB[i][0][iter] = p[0]  # pRi
        arg_liste_RGB[i][1][iter] = p[1]  # pGi
        arg_liste_RGB[i][2][iter] = p[2]  # pBi


def affiche_liste_RGB(liste_RGB, nbr_pixel):
    '''Permet d'afficher à la console une liste RGB'''
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

    for j in range(width):
        sommeR = 0
        sommeG = 0
        sommeB = 0
        for i in range(height):
            sommeR += matR[i, j]
            sommeG += matG[i, j]
            sommeB += matB[i, j]
        list_moyenne[0][j] = round((sommeR/height), 1)
        list_moyenne[1][j] = round((sommeG/height), 1)
        list_moyenne[2][j] = round((sommeB/height), 1)
    return list_moyenne


def enregistrer_moyenne(liste_moyenne):
    '''Permet d'enregistrer la moyenne des colonnes dans un fichier .txt'''
    with open('moyenne_colonne.txt', 'w') as f:
        f.write('R:\n')
        f.write(str(liste_moyenne[0])+'\n')
        f.write('G:\n')
        f.write(str(liste_moyenne[1])+'\n')
        f.write('B:\n')
        f.write(str(liste_moyenne[2])+'\n')


def ligne_horizontale(matR, matG, matB, num_ligne):
    '''Permet d'obtenir les valeurs RGB d'une ligne horizontale'''
    width = len(matR[0])
    num_ligne -= 1
    ligne = ([0]*width, [0]*width, [0]*width)
    for j in range(width):
        ligne[0][j] = matR[num_ligne, j]
        ligne[1][j] = matG[num_ligne, j]
        ligne[2][j] = matB[num_ligne, j]
    return ligne


def enregistrer_liste_RGB(nom_fichier, liste_RGB, liste_pixels, nbr_pixel=1):
    '''Permet d'enregistrer une liste RGB dans un fichier texte qui prend la forme suivante:
    i correspond au numéro du pixel et la liste est valeur R/G/B du pixel pour le nombre de captures prises
    pRi
    [...]
    pGi
    [...]
    pBi
    [...]'''
    with open(nom_fichier + '.txt', "w") as f:
        print(liste_pixels, file=f)
        for i in range(nbr_pixel):
            for j in range(3):
                if j == 0:
                    print('pR'+str(i), file=f)
                elif j == 1:
                    print('pG'+str(i), file=f)
                else:
                    print('pB'+str(i), file=f)
                print(liste_RGB[i][j], file=f)


def z_functionR(x, y, z, liste_RGB):
    '''Permet de générer les valeurs des coordonées Z pour un affichage 3D (pixels Rouge)
    Utilisée seulement par la fonction plot_3D'''
    for i in y:
        for j in x:
            z[i][j] = liste_RGB[i][0][j]
    return z


def z_functionG(x, y, z, liste_RGB):
    '''Permet de générer les valeurs des coordonées Z pour un affichage 3D (pixels Vert)
    Utilisée seulement par la fonction plot_3D'''
    for i in y:
        for j in x:
            z[i][j] = liste_RGB[i][1][j]
    return z


def z_functionB(x, y, z, liste_RGB):
    '''Permet de générer les valeurs des coordonées Z pour un affichage 3D (pixels Bleu)
    Utilisée seulement par la fonction plot_3D'''
    for i in y:
        for j in x:
            z[i][j] = liste_RGB[i][2][j]
    return z


def plot_3D(liste_RGB, nbr_pixel, nbr_image):
    '''Permet d'afficher un graphique 3D des valeurs RGB des pixels choisis après une capture d'image
    Les coordonnées X correspondent aux nombre de captures prises, Y correspond au numéro du pixel depuis
    la liste prédéfinit et les coordonnées Z correspondent à l'intensité R, G ou B d'un pixel selon la capture'''
    x = np.arange(nbr_image)
    y = np.arange(nbr_pixel)
    zR = np.zeros((nbr_pixel, nbr_image))
    zG = np.zeros((nbr_pixel, nbr_image))
    zB = np.zeros((nbr_pixel, nbr_image))
    X, Y = np.meshgrid(x, y)
    ZR = z_functionR(x, y, zR, liste_RGB)

    ZG = z_functionG(x, y, zG, liste_RGB)

    ZB = z_functionB(x, y, zB, liste_RGB)

    fig = plt.figure(1)
    ax = plt.axes(projection="3d")
    if nbr_image == 1:
        ax.plot_wireframe(X, Y, ZR, color='red')
    else:
        ax.plot_surface(X, Y, ZR, color='red')
    ax.set_xlabel("nombre d'image")
    ax.set_ylabel('numéro du pixel')
    ax.set_zlabel('intensité lunineuse')

    fig = plt.figure(2)
    ax = plt.axes(projection="3d")

    if nbr_image == 1:
        ax.plot_wireframe(X, Y, ZG, color='green')
    else:
        ax.plot_surface(X, Y, ZG, color='green')
    ax.set_xlabel("nombre d'image")
    ax.set_ylabel('numéro du pixel')
    ax.set_zlabel('intensité lunineuse')

    fig = plt.figure(3)
    ax = plt.axes(projection="3d")

    if nbr_image == 1:
        ax.plot_wireframe(X, Y, ZB, color='blue')
    else:
        ax.plot_surface(X, Y, ZB, color='blue')
    ax.set_xlabel("nombre d'image")
    ax.set_ylabel('numéro du pixel')
    ax.set_zlabel('intensité lunineuse')
    plt.show()


def plot_moyenne(liste_moyenne):
    '''Permet d'afficher les moyennes R, G, B de chaque colonne sur un meme graphique'''
    x = np.arange(len(liste_moyenne[0]))
    R = liste_moyenne[0]
    G = liste_moyenne[1]
    B = liste_moyenne[2]
    plt.plot(x, R, 'r', x, G, 'g', x, B, 'b')
    plt.xlabel('numéro de colonne')
    plt.ylabel('intensité lumineuse')
    plt.show()
