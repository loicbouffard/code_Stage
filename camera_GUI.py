import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import actions_image
import time
from pyqtgraph import PlotWidget, plot
import pyqtgraph
import numpy as np
import Dialog_liste_pixels
import re
import threading


class camera_GUI(QtWidgets.QMainWindow):

    def __init__(self):
        super(camera_GUI, self).__init__()
        uic.loadUi("UI/camera_GUI.ui", self)
        self.etat_port = False
        self.nom_portUSB = ''
        self.sp = 0
        self.image = 0
        self.liste_pos_pixels = []
        self.afficher_port_dispo()
        self.init_graph()
        self.group_Actions()

        self.bouton_vider.clicked.connect(self.action_bouton_vider)
        self.bouton_capture.clicked.connect(self.action_bouton_capture)
        self.actionCapture.triggered.connect(self.action_bouton_capture)
        self.actionQuitter.triggered.connect(self.action_quitter)
        self.actionOuvrir.triggered.connect(self.action_ouvrir)
        self.actionFermer.triggered.connect(self.action_fermer)
        self.actionActualiser.triggered.connect(self.afficher_port_dispo)
        self.actionMoyenne_colonne.triggered.connect(self.plot_moyenne_graph)
        self.actionEnr_moyenne_colonnes.triggered.connect(
            self.enregistrer_moyenne_colonnes)
        self.actionListe_pixels.triggered.connect(self.action_dialog)
        self.actionTest_images.triggered.connect(self.action_test_images)

    def action_quitter(self):
        self.action_fermer()
        sys.exit()

    def action_bouton_vider(self):
        self.textBrowser.clear()

    def action_bouton_capture(self):
        try:
            self.image = actions_image.capture(self.sp)
            self.image_capteur.setPixmap(
                QtGui.QPixmap('images/img_ARDUCAM.jpg'))
            self.sp.reset_input_buffer()
        except Exception as err:
            self.textBrowser.append(str(err))

    def afficher_port_dispo(self):
        list = actions_image.list_port()
        # list = ['COM1', 'COM2', 'COM3']
        group = QtWidgets.QActionGroup(self.menuDisponible)
        for port in list:
            action = QtWidgets.QAction(
                port, self.menuDisponible, checkable=True)
            action.triggered.connect(self.setNom_portUSB)
            self.menuDisponible.addAction(action)
            group.addAction(action)
        group.setExclusive(True)

    def setNom_portUSB(self):
        if not self.etat_port:
            self.nom_portUSB = self.sender().text()
        elif (self.etat_port):
            self.textBrowser.append(
                f'Fermez le port {self.nom_portUSB} avant de changer de port')

    def group_Actions(self):
        group_dimensions = QtWidgets.QActionGroup(self.menuDimensions)
        for dim in self.menuDimensions.actions():
            dim.triggered.connect(self.action_commandes)
            group_dimensions.addAction(dim)
        group_dimensions.setExclusive(True)

        group_formats = QtWidgets.QActionGroup(self.menuFormat)
        for format in self.menuFormat.actions():
            format.triggered.connect(self.action_commandes)
            group_formats.addAction(format)
        group_formats.setExclusive(True)

        group_saturations = QtWidgets.QActionGroup(self.menuSaturation)
        for sat in self.menuSaturation.actions():
            sat.triggered.connect(self.action_commandes)
            group_saturations.addAction(sat)
        group_saturations.setExclusive(True)

        group_brightness = QtWidgets.QActionGroup(self.menuBrightness)
        for bright in self.menuBrightness.actions():
            bright.triggered.connect(self.action_commandes)
            group_brightness.addAction(bright)
        group_brightness.setExclusive(True)

        group_contrast = QtWidgets.QActionGroup(self.menuContrast)
        for cont in self.menuContrast.actions():
            cont.triggered.connect(self.action_commandes)
            group_contrast.addAction(cont)
        group_contrast.setExclusive(True)

        group_sharpness = QtWidgets.QActionGroup(self.menuSharpness)
        for sharp in self.menuSharpness.actions():
            sharp.triggered.connect(self.action_commandes)
            group_sharpness.addAction(sharp)
        group_sharpness.setExclusive(True)

        group_exposure = QtWidgets.QActionGroup(self.menuExposure)
        for expo in self.menuExposure.actions():
            expo.triggered.connect(self.action_commandes)
            group_exposure.addAction(expo)
        group_exposure.setExclusive(True)

        group_mirror = QtWidgets.QActionGroup(self.menuMirror)
        for mirr in self.menuMirror.actions():
            mirr.triggered.connect(self.action_commandes)
            group_mirror.addAction(mirr)
        group_mirror.setExclusive(True)

        group_hue = QtWidgets.QActionGroup(self.menuHue)
        for hue in self.menuHue.actions():
            hue.triggered.connect(self.action_commandes)
            group_hue.addAction(hue)
        group_hue.setExclusive(True)

        group_LM = QtWidgets.QActionGroup(self.menuLight_mode)
        for l_m in self.menuLight_mode.actions():
            l_m.triggered.connect(self.action_commandes)
            group_LM.addAction(l_m)
        group_LM.setExclusive(True)

        group_SE = QtWidgets.QActionGroup(self.menuSpecial_Effect)
        for s_e in self.menuSpecial_Effect.actions():
            s_e.triggered.connect(self.action_commandes)
            group_SE.addAction(s_e)
        group_SE.setExclusive(True)

        group_tests = QtWidgets.QActionGroup(self.menuTests)
        for test in self.menuTests.actions():
            test.triggered.connect(self.action_commandes)
            group_tests.addAction(test)
        group_tests.setExclusive(True)

    def action_commandes(self):
        try:
            self.textBrowser.append(actions_image.envoie_commande(
                self.sp, self.sender().text()))
        except Exception as err:
            self.textBrowser.append(str(err))

    def action_ouvrir(self):
        if not self.etat_port:
            try:
                self.sp = actions_image.init_port(self.nom_portUSB)
                self.etat_port = True
                time.sleep(2)
                self.read_sp()
            except Exception as err:
                self.textBrowser.append(str(err))
        else:
            self.textBrowser.append(
                f'Le port {self.nom_portUSB} est déjà ouvert')

    def action_fermer(self):
        if self.sp != 0 and self.etat_port:
            self.sp.close()
            self.etat_port = False
            self.textBrowser.append(f'Port {self.nom_portUSB} fermé')

    def read_sp(self):
        while(self.sp.in_waiting > 0):
            self.textBrowser.append(self.sp.readline().decode('utf-8'))
        self.sp.reset_input_buffer()

    def plot_moyenne_graph(self):
        R = actions_image.get_matriceR(self.image)
        G = actions_image.get_matriceG(self.image)
        B = actions_image.get_matriceB(self.image)
        self.liste_moyenne = actions_image.moyenne_colonne(R, G, B)
        x = np.arange(len(self.liste_moyenne[0]))
        R = self.liste_moyenne[0]
        G = self.liste_moyenne[1]
        B = self.liste_moyenne[2]
        penR = pyqtgraph.mkPen(color='r')
        penG = pyqtgraph.mkPen(color='g')
        penB = pyqtgraph.mkPen(color='b')
        self.graphicsView_moyenne.plot(x, R, name="Pixels Rouges", pen=penR)
        self.graphicsView_moyenne.plot(x, G, name="Pixels Verts", pen=penG)
        self.graphicsView_moyenne.plot(x, B, name="Pixels bleus", pen=penB)

    def init_graph(self):
        self.liste_moyenne = []
        self.graphicsView_moyenne.setTitle(
            "Moyenne des intensités R/G/B de chaque colonne")
        self.graphicsView_moyenne.setLabel("left", "Intensité(/255)")
        self.graphicsView_moyenne.setLabel("bottom", "Colonne")
        self.graphicsView_moyenne.addLegend()
        self.graphicsView_moyenne.showGrid(x=True, y=True)

    def enregistrer_moyenne_colonnes(self):
        actions_image.enregistrer_moyenne(self.liste_moyenne)

    def action_dialog(self):
        dlg = Dialog_liste_pixels.Dialog(self)
        if dlg.exec_():
            liste = re.findall(
                r'\d+', dlg.textEdit_liste_pixels.toPlainText())
            if len(liste) == 0:
                self.textBrowser.append("La liste de pixels est vide")
            else:
                self.liste_pos_pixels.clear()
                for i in range(0, len(liste), 2):
                    pos = (int(liste[i]), int(liste[i+1]))
                    self.liste_pos_pixels.append(pos)
                self.textBrowser.append(str(self.liste_pos_pixels))

    def action_test_images(self):
        try:
            threading._start_new_thread(actions_image.test_images,
                                        (self.spinBox_nbrCapture.value(), self.liste_pos_pixels, self.sp, self.progressBar_nbrCapture))
            self.progressBar_nbrCapture.reset()
        except Exception as err:
            self.textBrowser.append(str(err))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = camera_GUI()
    window.show()
    app.exec_()
