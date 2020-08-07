'''Ce module contient la classe du dialogue pour l'enregistrement de la liste de pixels.'''
from PyQt5 import QtWidgets
from PyQt5 import uic


class Dialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        uic.loadUi("UI/Dialog_liste_pixels.ui", self)

        self.setWindowTitle("Liste pixels")
        self.affiche_liste_pixel()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def affiche_liste_pixel(self):
        liste_pixels = self.parent().liste_pos_pixels
        if len(liste_pixels) > 0:
            self.textEdit_liste_pixels.setText(str(liste_pixels))
