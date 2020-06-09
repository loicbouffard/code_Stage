
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
    time.sleep(1)
    size = int(sp.readline().decode('utf-8'))

    img = sp.read(size)

    with open("img_ARDUCAM.jpg", "wb") as f:
        f.write(img)
    sp.reset_input_buffer()
    return Image.open('img_ARDUCAM.jpg')


def ecrit_image_RAW(sp):
    time.sleep(1)
    size = 640*480
    img = sp.read(size)
    with open("img_ARDUCAM.raw", "wb") as f:
        f.write(img)
    sp.reset_input_buffer()


nbr_image = 10  # nombre de captures à prendre
nbr_pixel = 6   # nombre de pixels à comptabiliser les valeurs RGB
liste_pixels = [(153, 29), (76, 135), (150, 206),
                (253, 136), (100, 100), (132, 45)]
if __name__ == "__main__":
    sp = init_port()
    action = ""
    while(action != 'exit'):
        if action == 'capture':
            ecrit_image(sp)
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
        elif action == "test image":
            liste_RGB = actions_image.cree_liste_RGB(nbr_image, nbr_pixel)
            for i in range(nbr_image):
                sp.write(liste_actions.dic_actions["capture"])
                image = ecrit_image(sp)

                actions_image.remplir_listes_RGB(
                    i, liste_RGB, image, liste_pixels)
                print(i)
            actions_image.affiche_liste_RGB(liste_RGB, nbr_pixel)
    sp.close()
