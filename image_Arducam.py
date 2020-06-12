
import serial
import time
import liste_actions
import actions_image
from PIL import Image


def init_port():
    sp = serial.Serial('COM5', 1000000)
    sp.timeout = 0.4
    return sp


def ecrit_image(sp):
    '''Écrit les données reçu de l'arduino dans un fichier .jpg'''
    time.sleep(1)
    size = int(sp.readline().decode('utf-8'))

    img = sp.read(size)

    with open("img_ARDUCAM.jpg", "wb") as f:
        f.write(img)
    sp.reset_input_buffer()
    return Image.open('img_ARDUCAM.jpg')


def ecrit_image_RAW(sp):
    '''Écrit les données reçu de l'arduino dans un fihcier .raw'''
    time.sleep(1)
    size = 640*480
    img = sp.read(size)
    with open("img_ARDUCAM.raw", "wb") as f:
        f.write(img)
    sp.reset_input_buffer()


# nombre de captures à prendre
# nbr_image = 10
# liste des coordonnées des pixels à analyser
# liste_pixels = [(132, 96), (132, 97), (132, 98), (132, 99), (132, 100), (132, 101), (132, 102), (132, 103),
#                 (132, 104), (132, 105), (132, 106), (132, 107), (129,
#                                                                  156), (129, 157), (129, 158), (129, 159), (129, 160),
#                 (129, 161), (129, 162), (129, 163), (129, 164), (129, 165), (129, 166), (127, 215), (127, 216), (127, 217), (127, 218), (127, 219), (127, 220), (127, 221), (127, 222), (127, 223), (127, 224), (127, 225)]
# nombre de pixels à comptabiliser les valeurs RGB
# nbr_pixel = len(liste_pixels)


if __name__ == "__main__":
    sp = init_port()
    action = ""
    image = 0
    liste_pixels = [(140, 61), (140, 62), (140, 63), (140, 64), (140, 65), (140, 66), (140, 67), (140, 68), (140, 69), (140, 70), (140, 71), (
        140, 72), (140, 73), (140, 74), (140, 75), (137, 125), (137, 126), (137, 127), (137, 128), (137, 129), (137, 130), (137, 131), (137, 132)]
    nbr_pixel = len(liste_pixels)
    nbr_image = 1
    while(action != 'exit'):
        if action == 'capture':
            image = ecrit_image(sp)
        elif action == 'captureRAW':
            ecrit_image_RAW(sp)

        time.sleep(2.5)
        while(sp.in_waiting > 0):
            print(sp.readline())
        sp.reset_input_buffer()

        action = input('action: ')
        if (action in liste_actions.dic_actions):
            commande = liste_actions.dic_actions[action]
            if (action in liste_actions.dic_dim):
                sp.timeout = liste_actions.dic_dim[action]
            sp.write(commande)
        if action == "RAW":
            sp.timeout = 10
        elif action == "set nbr image":
            nbr_image = int(input("nombre d'image à capturer: "))
        elif action == "set liste pixels":
            while True:
                pos = input("pos pixel x,y : ")
                if pos == 'ok':
                    break
                pos = (int(pos[0]), int(pos[2]))
                liste_pixels.append(pos)
            nbr_pixel = len(liste_pixels)
            print(liste_pixels)
        elif action == "test image":
            liste_RGB = actions_image.cree_liste_RGB(nbr_image, nbr_pixel)
            for i in range(nbr_image):
                sp.write(liste_actions.dic_actions["capture"])
                image = ecrit_image(sp)

                actions_image.remplir_listes_RGB(
                    i, liste_RGB, image, liste_pixels)
                print(i)
            actions_image.enregistrer_liste_RGB(
                'liste_RGB_test_image', liste_RGB, liste_pixels, nbr_pixel)
            actions_image.plot_3D(liste_RGB, nbr_pixel, nbr_image)
        elif action == "enregistrer" and image != 0:
            liste_RGB = actions_image.cree_liste_RGB(1, nbr_pixel)
            actions_image.remplir_listes_RGB(0, liste_RGB, image, liste_pixels)
            actions_image.enregistrer_liste_RGB(
                'liste_RGB_capture', liste_RGB, liste_pixels, nbr_pixel)
        elif action == "3D" and image != 0:
            liste_RGB = actions_image.cree_liste_RGB(1, nbr_pixel)
            actions_image.remplir_listes_RGB(0, liste_RGB, image, liste_pixels)
            actions_image.plot_3D(liste_RGB, nbr_pixel, 1)
        elif action == 'moyenne' and image != 0:
            R = actions_image.get_matriceR(image)
            G = actions_image.get_matriceG(image)
            B = actions_image.get_matriceB(image)
            liste_moyenne = actions_image.moyenne_colonne(R, G, B)
            actions_image.enregistrer_moyenne(liste_moyenne)
    sp.close()
