from PyQt5 import QtCore
import actions_image
import serial
import time
from PIL import Image
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

    @QtCore.pyqtSlot(serial.Serial)
    def capture(self, sp):
        img = actions_image.capture(sp)
        self.image.emit(img)

    liste_moyenne = QtCore.pyqtSignal(tuple, list, list, list)

    @QtCore.pyqtSlot(numpy.ndarray, numpy.ndarray, numpy.ndarray)
    def liste_moy(self, R, G, B):
        liste = actions_image.moyenne_colonne(R, G, B)
        R = liste[0]
        G = liste[1]
        B = liste[2]
        self.liste_moyenne.emit(liste, R, G, B)

    def test_images(self): pass
    '''À implémenter lorsqu'une nouvelle facon de plot 3D sera trouvé. Dont utiliser OpenGL'''

    liste_LO = QtCore.pyqtSignal(list, list, list)

    @QtCore.pyqtSlot(tuple)
    def longeur_donde(self, liste_moyenne):
        liste = actions_image.longueur_Donde(liste_moyenne)
        x = [l[1] for l in liste]
        y = [i[0] for i in liste]
        self.liste_LO.emit(liste, x, y)
