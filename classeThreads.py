'''Ce module contient les classes «Worker» qui permette l'utilisation des threads de l'application.'''
from PyQt5 import QtCore
import actions_image
import serial
import time
from PIL import Image, ImageChops
import actions_image
import numpy


class Worker(QtCore.QObject):
    '''Classe Worker qui permet de lancé des threads pour l'application'''
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
        if format == '.jpg':
            img = actions_image.captureJPEG(sp)
        elif format == '.bmp':
            img = actions_image.captureBMP(sp)
        elif format == '.raw':
            img = actions_image.captureRAW(sp)
        self.image.emit(img)

    @QtCore.pyqtSlot(serial.Serial)
    def debutStreaming(self, sp):
        actions_image.beginStreaming(sp)

    endStream = QtCore.pyqtSignal(str)

    @QtCore.pyqtSlot(serial.Serial)
    def finStream(self, sp):
        actions_image.endStreaming(sp)
        self.endStream.emit("Fin du stream")

    @QtCore.pyqtSlot(serial.Serial, str, Image.Image)
    def capture_bruit(self, sp, format, img_bruit):
        img = actions_image.captureJPEG(sp, img_bruit=img_bruit)
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
            image = actions_image.captureJPEG(sp)
            actions_image.remplir_listes_RGB(
                i, liste_RGB, image, liste_pixels)
            self.updateProgressBar.emit(i+1)
        actions_image.enregistrer_liste_RGB(
            'sauvegarde/liste_RGB_test_image', liste_RGB, liste_pixels, nbr_pixel)
        self.zvaleur.emit(actions_image.plot_3D_GUI(
            liste_RGB, nbr_pixel, nbr_image))

    liste_LO = QtCore.pyqtSignal(list, list, list)
    list_histo = QtCore.pyqtSignal(list, list, dict)

    @QtCore.pyqtSlot(tuple, int, int)
    def longeur_donde(self, liste_moyenne, lMax, lMin):
        liste, histo = actions_image.longueur_Donde(
            liste_moyenne, lMax, lMin, nbr_param=4)
        x = [l[3] for l in liste]
        y = [i[2] for i in liste]
        self.liste_LO.emit(liste, x, y)
        self.list_histo.emit([l for l in histo], [
                             nbr for nbr in histo.values()], histo)

    test_bruitSignal = QtCore.pyqtSignal(str)

    @QtCore.pyqtSlot(serial.Serial)
    def test_bruit(self, sp):
        actions_image.capture_test_bruit(sp)
        self.test_bruitSignal.emit("Fin des captures d'image de bruit")


class WorkerStream(QtCore.QObject):
    '''Classe worker pour le streaming.'''
    image = QtCore.pyqtSignal(Image.Image)

    @QtCore.pyqtSlot(serial.Serial)
    def stream(self, sp):
        time.sleep(0.4)
        while self.bStream:
            self.image.emit(actions_image.stream(sp))
            # 0.2 pour image couleur, 0.15 pour image noire // dim 320x240
            time.sleep(0.2)

    bStream = False

    @QtCore.pyqtSlot(bool)
    def setBStream(self, b):
        self.bStream = b
