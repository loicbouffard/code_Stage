
import serial
import time
import liste_actions
import actions_image
from PIL import Image


def init_port():
    sp = serial.Serial('COM5', 1000000)
    sp.timeout = 0.3
    return sp


def ecrit_image(sp):
    time.sleep(1)
    size = int(sp.readline().decode('utf-8'))

    img = sp.read(size)

    with open("img_ARDUCAM.jpg", "wb") as f:
        f.write(img)
    sp.reset_input_buffer()
    return Image.open('img_ARDUCAM.jpg')


if __name__ == "__main__":
    sp = init_port()
    action = ""
    while(action != 'exit'):
        if action == 'capture':
            ecrit_image(sp)
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
        elif action == "test image":
            sp.timeout = 0.4
            nbr = 100
            liste_pixels = actions_image.cree_liste_pixel(nbr)
            for i in range(nbr):
                sp.write(liste_actions.dic_actions["capture"])
                image = ecrit_image(sp)
                actions_image.remplir_listes_pixels(i, liste_pixels, image, (153, 29),
                                                    (76, 135), (150, 206), (253, 136))
                print(i)
            actions_image.affiche_liste_pixel(liste_pixels)
    sp.close()
