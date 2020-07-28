from PyQt5 import QtCore
import actions_image
import serial
import time
from PIL import Image, ImageChops
import actions_image
import numpy


class Worker(QtCore.QObject):
    '''Classe '''
    read = QtCore.pyqtSignal(str)

    @QtCore.pyqtSlot(serial.Serial)
    def read_port(self, sp):
        text = ''
        time.sleep(2)
        while(sp.in_waiting > 0):
            text += (sp.readline().decode('utf-8'))
        self.read.emit(text)

    image = QtCore.pyqtSignal(Image.Image)

    @QtCore.pyqtSlot(serial.Serial, str)
    def capture(self, sp, format):
        img = actions_image.capture(sp, format)
        self.image.emit(img)

    @QtCore.pyqtSlot(serial.Serial, str, Image.Image)
    def capture_bruit(self, sp, format, img_bruit):
        img = actions_image.capture(sp, format, img_bruit)
        self.image.emit(img)

    liste_moyenne = QtCore.pyqtSignal(tuple, list, list, list)

    @QtCore.pyqtSlot(numpy.ndarray, numpy.ndarray, numpy.ndarray)
    def liste_moy(self, R, G, B):
        liste = actions_image.moyenne_colonne(R, G, B)
        R = liste[0]
        G = liste[1]
        B = liste[2]
        self.liste_moyenne.emit(liste, R, G, B)

    zvaleur = QtCore.pyqtSignal(tuple)
    updateProgressBar = QtCore.pyqtSignal(int)

    @QtCore.pyqtSlot(serial.Serial, int, int, list)
    def test_images(self, sp, nbr_pixel, nbr_image, liste_pixels):
        liste_RGB = actions_image.cree_liste_RGB(nbr_image, nbr_pixel)

        for i in range(nbr_image):
            image = actions_image.capture(sp)
            actions_image.remplir_listes_RGB(
                i, liste_RGB, image, liste_pixels)
            self.updateProgressBar.emit(i+1)
        actions_image.enregistrer_liste_RGB(
            'sauvegarde/liste_RGB_test_image', liste_RGB, liste_pixels, nbr_pixel)
        self.zvaleur.emit(actions_image.plot_3D_GUI(
            liste_RGB, nbr_pixel, nbr_image))

    liste_LO = QtCore.pyqtSignal(list, list, list)

    @QtCore.pyqtSlot(tuple)
    def longeur_donde(self, liste_moyenne):
        liste = actions_image.longueur_Donde(liste_moyenne)
        x = [l[1] for l in liste]
        y = [i[0] for i in liste]
        self.liste_LO.emit(liste, x, y)

    test_bruitSignal = QtCore.pyqtSignal(str)

    @QtCore.pyqtSlot(serial.Serial)
    def test_bruit(self, sp):
        actions_image.capture_test_bruit(sp)
        self.test_bruitSignal.emit("Fin des captures d'image de bruit")
