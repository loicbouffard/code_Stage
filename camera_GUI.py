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
import queue
from PIL import Image
import pyqtgraph.opengl as gl


class camera_GUI(QtWidgets.QMainWindow):

    def __init__(self):
        super(camera_GUI, self).__init__()
        uic.loadUi("UI/camera_GUI.ui", self)
        self.etat_port = False
        self.nom_portUSB = ''
        self.sp = 0
        self.image = 0
        self.liste_pos_pixels = []
        self.liste_moyenne = []
        self.afficher_port_dispo()
        self.init_graph()
        self.group_Actions()
        self.queue = queue.Queue()
        # self.init_GLwidget()

        self.bouton_vider.clicked.connect(self.action_bouton_vider)
        self.bouton_capture.clicked.connect(self.thread_action_bouton_capture)
        self.actionCapture.triggered.connect(self.thread_action_bouton_capture)
        self.actionQuitter.triggered.connect(self.action_quitter)
        self.actionOuvrir.triggered.connect(self.thread_action_ouvrir)
        self.actionFermer.triggered.connect(self.action_fermer)
        self.actionActualiser.triggered.connect(self.afficher_port_dispo)
        self.actionMoyenne_colonne.triggered.connect(
            self.plot_moyenne_graph)
        self.actionEnr_moyenne_colonnes.triggered.connect(
            self.enregistrer_moyenne_colonnes)
        self.actionListe_pixels.triggered.connect(self.action_dialog)
        self.actionTest_images.triggered.connect(
            self.thread_action_test_images)
        self.bouton_moy_col.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(2))
        self.bouton_cap_test.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(1))
        self.bouton_LO.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(0))
        self.actionImage.triggered.connect(self.action_import_image)
        self.bouton_graph_moy.clicked.connect(
            lambda: self.stackedWidget_graph.setCurrentIndex(1))
        self.bouton_graph3D.clicked.connect(
            lambda: self.stackedWidget_graph.setCurrentIndex(0))
        self.bouton_graph_LO.clicked.connect(
            lambda: self.stackedWidget_graph.setCurrentIndex(2))
        self.bouton_im.clicked.connect(
            lambda: self.stackedWidget_Images.setCurrentIndex(1))
        self.bouton_imR.clicked.connect(
            lambda: self.stackedWidget_Images.setCurrentIndex(2))
        self.bouton_imG.clicked.connect(
            lambda: self.stackedWidget_Images.setCurrentIndex(3))
        self.bouton_imB.clicked.connect(
            lambda: self.stackedWidget_Images.setCurrentIndex(0))
        self.actionLongueur_d_onde.triggered.connect(self.action_LO)

    def action_quitter(self):
        self.action_fermer()
        sys.exit()

    def action_bouton_vider(self):
        self.textBrowser.clear()

    def thread_action_bouton_capture(self):
        t = threading.Thread(target=self.action_bouton_capture)
        t.start()

    def action_bouton_capture(self):
        try:
            self.image = actions_image.capture(self.sp)
            self.update_image()
            self.sp.reset_input_buffer()
            self.textBrowser.append("Capture faite")
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

        group_sharpness_auto = QtWidgets.QActionGroup(self.menuSharpness)
        group_sharpness_manual = QtWidgets.QActionGroup(self.menuSharpness)
        for sharp in self.menuSharpness.actions():
            sharp.triggered.connect(self.action_commandes)

        group_sharpness_auto.addAction(self.actionAuto_Sharpness_default)
        group_sharpness_auto.addAction(self.actionAuto_Sharpness_1)
        group_sharpness_auto.addAction(self.actionAuto_Sharpness_2)

        group_sharpness_manual.addAction(self.actionManual_Sharpnessoff)
        group_sharpness_manual.addAction(self.actionManual_Sharpness1)
        group_sharpness_manual.addAction(self.actionManual_Sharpness2)
        group_sharpness_manual.addAction(self.actionManual_Sharpness3)
        group_sharpness_manual.addAction(self.actionManual_Sharpness4)
        group_sharpness_manual.addAction(self.actionManual_Sharpness5)

        group_sharpness_auto.setExclusive(True)
        group_sharpness_manual.setExclusive(True)

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

    def thread_action_ouvrir(self):
        t = threading.Thread(target=self.action_ouvrir)
        t.start()

    def action_ouvrir(self):
        if not self.etat_port:
            try:
                # t = threading.Thread(target=lambda q, arg1: q.put(
                #     actions_image.init_port(arg1)), args=(self.queue, self.nom_portUSB))
                # t.start()
                # t.join()
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

    def thread_plot_moyenne_graph(self):
        t = threading.Thread(target=self.plot_moyenne_graph)
        t.start()

    def plot_moyenne_graph(self):
        R = actions_image.get_matriceR(self.image)
        G = actions_image.get_matriceG(self.image)
        B = actions_image.get_matriceB(self.image)
        # t = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(
        #     actions_image.moyenne_colonne(arg1, arg2, arg3)), args=(self.queue, R, G, B))
        # t.start()
        # t.join()
        self.liste_moyenne = actions_image.moyenne_colonne(R, G, B)
        x = np.arange(len(self.liste_moyenne[0]))
        R = self.liste_moyenne[0]
        G = self.liste_moyenne[1]
        B = self.liste_moyenne[2]

        self.plot_moyenneR.setData(x, R)
        self.plot_moyenneG.setData(x, G)
        self.plot_moyenneB.setData(x, B)
        actions_image.enregistrer_moyenne(self.liste_moyenne)
        self.update_tab_donnee_moy()

    def init_graph(self):
        self.liste_moyenne = []
        self.graphicsView_moyenne.setTitle(
            "Moyenne des intensités R/G/B de chaque colonne")
        self.graphicsView_moyenne.setLabel("left", "Intensité(/255)")
        self.graphicsView_moyenne.setLabel("bottom", "Colonne")
        self.graphicsView_moyenne.addLegend()
        self.graphicsView_moyenne.showGrid(x=True, y=True)

        penR = pyqtgraph.mkPen(color='r')
        penG = pyqtgraph.mkPen(color='g')
        penB = pyqtgraph.mkPen(color='b')

        self.plot_moyenneR = self.graphicsView_moyenne.plot(
            [0], [0], name="Pixels Rouges", pen=penR)
        self.plot_moyenneG = self.graphicsView_moyenne.plot(
            [0], [0], name="Pixels Verts", pen=penG)
        self.plot_moyenneB = self.graphicsView_moyenne.plot(
            [0], [0], name="Pixels bleus", pen=penB)

        # Graphique longueurs d'onde
        self.graphicsView_LO.setTitle(
            "Intensité lumineuse en fonction de la longueur d'onde")
        self.graphicsView_LO.setLabel("left", "Intensité")
        self.graphicsView_LO.setLabel("bottom", "Longueur d'onde (nm)")
        self.graphicsView_LO.showGrid(x=True, y=True)

        self.plot_LO = self.graphicsView_LO.plot([0], [0])

    def enregistrer_moyenne_colonnes(self):
        if self.image != 0:
            if len(self.liste_moyenne) == 0:
                self.plot_moyenne_graph()
            actions_image.enregistrer_moyenne(self.liste_moyenne)
            self.update_tab_donnee_moy()
            self.liste_moyenne = []
        else:
            self.textBrowser.append("Prendre une capture")

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

    def thread_action_test_images(self):
        t = threading.Thread(target=self.action_test_images)
        t.start()

    def action_test_images(self):
        try:
            actions_image.test_images(self.spinBox_nbrCapture.value(),
                                      self.liste_pos_pixels, self.sp, self.progressBar_nbrCapture)
            self.update_image()
            self.update_tab_donnee_test_cap()
        except ZeroDivisionError:
            self.textBrowser.append("Remplir la liste de pixels avant")
        except Exception as err:
            self.textBrowser.append(str(err))

    def update_tab_donnee_test_cap(self):
        with open('sauvegarde/liste_RGB_test_image.txt', 'r') as fich:
            text = fich.read()
        self.textBrowser_testCapture.setText(text)

    def update_tab_donnee_moy(self):
        with open('sauvegarde/moyenne_colonne.txt', 'r') as fich:
            text = fich.read()
        self.textBrowser_moy_colonne.setText(text)

    def update_tab_donne_LO(self):
        with open('sauvegarde/longueur_onde.txt', 'r') as fich:
            text = fich.read()
        self.textBrowser_LO.setText(text)

    def update_image(self):
        self.image_capteur.setPixmap(
            QtGui.QPixmap('images/img_ARDUCAM.jpg'))
        self.image_capteurR.setPixmap(
            QtGui.QPixmap('images/img_R.jpg'))
        self.image_capteurG.setPixmap(
            QtGui.QPixmap('images/img_G.jpg'))
        self.image_capteurB.setPixmap(
            QtGui.QPixmap('images/img_B.jpg'))

    def action_import_image(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(
            filter="Image Files (*.png *.jpg *.bmp)")[0]
        self.image = Image.open(filePath)
        actions_image.enregistre_image_RGB(self.image)

        self.image_capteur.setPixmap(
            QtGui.QPixmap(filePath))
        self.image_capteurR.setPixmap(
            QtGui.QPixmap('images/img_R.jpg'))
        self.image_capteurG.setPixmap(
            QtGui.QPixmap('images/img_G.jpg'))
        self.image_capteurB.setPixmap(
            QtGui.QPixmap('images/img_B.jpg'))

    def init_GLwidget(self):
        self.GL_Graph = gl.GLViewWidget(self.openGLWidget)
        # self.page_4.addAction(self.GL_Graph)
        #self.GL_Graph.resizeGL(500, 500)
        axes = gl.GLAxisItem()
        self.GL_Graph.addItem(axes)

    def thread_action_LO(self):
        t = threading.Thread(target=self.action_LO)
        t.start()

    def action_LO(self):
        if self.image != 0:
            if len(self.liste_moyenne) != 0:
                liste = actions_image.longueur_Donde(self.liste_moyenne)
                x = [l[1] for l in liste]
                y = [i[0] for i in liste]
                self.plot_LO.setData(x, y)
            else:
                self.plot_moyenne_graph()
                liste = actions_image.longueur_Donde(self.liste_moyenne)
                x = [l[1] for l in liste]
                y = [i[0] for i in liste]
                self.plot_LO.setData(x, y)
            actions_image.enregistrer_LO(liste)
            self.update_tab_donne_LO()
        else:
            self.textBrowser.append("Il n'y a pas d'image à traiter")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = camera_GUI()
    window.show()
    app.exec_()
