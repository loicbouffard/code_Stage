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
from PIL import Image, ImageQt
import pyqtgraph.opengl as gl
import serial
import classeThreads
import liste_actions


class camera_GUI(QtWidgets.QMainWindow):

    port_ouvert = QtCore.pyqtSignal(serial.Serial)
    port_capture = QtCore.pyqtSignal(serial.Serial, str)
    port_capture_bruit = QtCore.pyqtSignal(serial.Serial, str, Image.Image)
    matRGB = QtCore.pyqtSignal(np.ndarray, np.ndarray, np.ndarray)
    longDonde = QtCore.pyqtSignal(tuple)
    test_bruit_signal = QtCore.pyqtSignal(serial.Serial)
    test_Cap_pixel = QtCore.pyqtSignal(serial.Serial, int, int, list)

    def __init__(self):
        super(camera_GUI, self).__init__()
        uic.loadUi("UI/camera_GUI.ui", self)
        self.etat_port = False
        self.nom_portUSB = ''
        self.sp = 0
        self.image = 0
        self.format_image = '.jpg'
        self.liste_moyenne = []
        self.liste_pos_pixels = []
        self.afficher_port_dispo()
        self.init_graph()
        self.group_Actions()
        self.init_worker()
        self.init_GLwidget()

        self.bouton_vider.clicked.connect(self.action_bouton_vider)
        self.bouton_capture.clicked.connect(self.action_bouton_capture)
        self.actionCapture.triggered.connect(self.action_bouton_capture)
        self.actionQuitter.triggered.connect(self.action_quitter)
        self.actionOuvrir.triggered.connect(self.action_ouvrir)
        self.actionFermer.triggered.connect(self.action_fermer)
        self.actionActualiser.triggered.connect(self.afficher_port_dispo)
        self.actionMoyenne_colonne.triggered.connect(
            self.plot_moyenne_graph)
        self.actionEnr_moyenne_colonnes.triggered.connect(
            self.enregistrer_moyenne_colonnes)
        self.actionListe_pixels.triggered.connect(self.action_dialog)
        self.actionCapture_pixel.triggered.connect(
            self.action_cap_pixel)

        self.bouton_moy_col.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(2))
        self.bouton_moy_colBack.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(0))
        self.bouton_cap_test.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(1))
        self.bouton_cap_testBack.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(2))
        self.bouton_LO.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(0))
        self.bouton_LOBack.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(1))
        self.actionImage.triggered.connect(self.action_import_image)
        self.bouton_graph_moy.clicked.connect(
            lambda: self.stackedWidget_graph.setCurrentIndex(1))
        self.bouton_graph_moyBack.clicked.connect(
            lambda: self.stackedWidget_graph.setCurrentIndex(2))
        self.bouton_graph3D.clicked.connect(
            lambda: self.stackedWidget_graph.setCurrentIndex(0))
        self.bouton_graph3DBack.clicked.connect(
            lambda: self.stackedWidget_graph.setCurrentIndex(1))
        self.bouton_graph_LO.clicked.connect(
            lambda: self.stackedWidget_graph.setCurrentIndex(2))
        self.bouton_graph_LOBack.clicked.connect(
            lambda: self.stackedWidget_graph.setCurrentIndex(0))
        self.bouton_im.clicked.connect(
            lambda: self.stackedWidget_Images.setCurrentIndex(1))
        self.bouton_imBack.clicked.connect(
            lambda: self.stackedWidget_Images.setCurrentIndex(4))
        self.bouton_imR.clicked.connect(
            lambda: self.stackedWidget_Images.setCurrentIndex(2))
        self.bouton_imRBack.clicked.connect(
            lambda: self.stackedWidget_Images.setCurrentIndex(0))
        self.bouton_imG.clicked.connect(
            lambda: self.stackedWidget_Images.setCurrentIndex(3))
        self.bouton_imGBack.clicked.connect(
            lambda: self.stackedWidget_Images.setCurrentIndex(1))
        self.bouton_imB.clicked.connect(
            lambda: self.stackedWidget_Images.setCurrentIndex(4))
        self.bouton_imBBack.clicked.connect(
            lambda: self.stackedWidget_Images.setCurrentIndex(2))
        self.actionLongueur_d_onde.triggered.connect(self.action_LO)
        self.bouton_enr_img.clicked.connect(self.enregistrer_imageSous)
        self.actionImage_sous.triggered.connect(self.enregistrer_imageSous)
        self.bouton_imBruit.clicked.connect(
            lambda: self.stackedWidget_Images.setCurrentIndex(0))
        self.bouton_imBruitBack.clicked.connect(
            lambda: self.stackedWidget_Images.setCurrentIndex(3))
        self.actionImage_bruit.triggered.connect(self.action_import_bruit)
        self.actionTest_Bruit.triggered.connect(self.test_bruit)
        self.actionGraphique_pixels.triggered.connect(self.affiche_plot3D)

    def action_quitter(self):
        self.action_fermer()
        sys.exit()

    def action_bouton_vider(self):
        self.textBrowser.clear()

    def action_bouton_capture(self):
        try:
            if self.checkBox_bruit.isChecked():
                self.port_capture_bruit.emit(
                    self.sp, self.format_image, self.image_bruit)
            else:
                self.port_capture.emit(self.sp, self.format_image)
        except AttributeError:
            self.textBrowser.append(
                "Il n'y a pas d'image de bruit d'enregistrée")
        except TypeError:
            self.textBrowser.append(
                'Ouvrir un port avant de faire une capture')
        except Exception as err:
            print(type(err))
            self.textBrowser.append(str(err))

    @ QtCore.pyqtSlot(Image.Image)
    def recoitCapture(self, img):
        self.image = img
        self.update_image(self.format_image)
        self.sp.reset_input_buffer()
        self.textBrowser.append("Capture faite")

    def afficher_port_dispo(self):
        list = actions_image.list_port()
        group = QtWidgets.QActionGroup(self.menuDisponible)
        length = len(self.menuDisponible.actions())-2
        for i in range(length):
            self.menuDisponible.removeAction(
                self.menuDisponible.actions()[i+2])
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
            nom = self.sender().text()
            self.textBrowser.append(actions_image.envoie_commande(
                self.sp, nom))
            if nom in liste_actions.dic_formats:
                self.format_image = liste_actions.dic_formats[nom]
            self.sp.reset_input_buffer()
        except Exception as err:
            self.textBrowser.append(str(err))

    def action_ouvrir(self):
        if not self.etat_port:
            try:
                self.sp = actions_image.init_port(self.nom_portUSB)
                self.etat_port = True
                self.port_ouvert.emit(self.sp)
            except serial.serialutil.SerialException:
                self.textBrowser.append("Choisir un port")
            except Exception as err:
                print(type(err))
                self.textBrowser.append(str(err))
        else:
            self.textBrowser.append(
                f'Le port {self.nom_portUSB} est déjà ouvert')

    @ QtCore.pyqtSlot(str)
    def recoitPort(self, text):
        self.sp.reset_input_buffer()
        self.textBrowser.append(text)

    def action_fermer(self):
        if self.sp != 0 and self.etat_port:
            self.sp.close()
            self.etat_port = False
            self.textBrowser.append(f'Port {self.nom_portUSB} fermé')

    def plot_moyenne_graph(self):
        if self.image != 0:
            R = actions_image.get_matriceR(self.image)
            G = actions_image.get_matriceG(self.image)
            B = actions_image.get_matriceB(self.image)
            self.matRGB.emit(R, G, B)
        else:
            self.textBrowser.append("Il n'y a pas d'image à traiter")

    @ QtCore.pyqtSlot(tuple, list, list, list)
    def recoitListeMoyenne(self, liste, listeR, listeG, listeB):
        self.liste_moyenne = liste
        x = np.arange(len(self.liste_moyenne[0]))

        self.plot_moyenneR.setData(x, listeR)
        self.plot_moyenneG.setData(x, listeG)
        self.plot_moyenneB.setData(x, listeB)
        actions_image.enregistrer_moyenne(self.liste_moyenne)
        self.update_tab_donnee_moy()
        self.action_LO()

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
                self.liste_pos_pixels = []
                for i in range(0, len(liste), 2):
                    pos = (int(liste[i]), int(liste[i+1]))
                    self.liste_pos_pixels.append(pos)
                self.textBrowser.append(str(self.liste_pos_pixels))

    def action_cap_pixel(self):
        try:
            length = len(self.liste_pos_pixels)
            if length > 0:
                self.test_Cap_pixel.emit(
                    self.sp, length, self.spinBox_nbrCapture.value(), self.liste_pos_pixels)
            else:
                self.textBrowser.append("Remplir la liste de pixels")
        except TypeError:
            self.textBrowser.append("Ouvrir un port série")
        except Exception as err:
            print(type(err))
            self.textBrowser.append(str(err))

    @ QtCore.pyqtSlot(tuple)
    def recoitCapPixel(self, tup):
        self.init_GLwidget()
        x = tup[0]
        y = tup[1]
        zR = tup[2]
        zG = tup[3]
        zB = tup[4]
        print(len(x))
        print(len(y))
        # [(12, 10), (20, 34), (56, 76), (43, 32), (56, 78)]
        try:
            self.plotGL_3DR = gl.GLSurfacePlotItem(
                x=y, y=x, z=zR, colors=[(0.4, 0.5, 1, 1)])
            self.plotGL_3DG = gl.GLSurfacePlotItem(
                x=y, y=x, z=zG, colors=(55, 30, 90, 100))
            self.plotGL_3DB = gl.GLSurfacePlotItem(
                x=y, y=x, z=zB, colors=(55, 100, 100, 1))
            self.gl_Graph.addItem(self.plotGL_3DR)
            self.gl_Graph.addItem(self.plotGL_3DG)
            self.gl_Graph.addItem(self.plotGL_3DB)
            self.gl_Graph.show()
            self.update_tab_donnee_test_cap()
            self.update_image('.jpg')
            self.progressBar_nbrCapture.setValue(0)
        except Exception as err:
            self.textBrowser.append(str(err))

    @ QtCore.pyqtSlot(int)
    def updateProgressBar(self, x):
        self.progressBar_nbrCapture.setValue(
            int(x*100/self.spinBox_nbrCapture.value()))

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

    def update_image(self, format):
        self.image_capteur.setPixmap(
            QtGui.QPixmap('images/img_ARDUCAM'+format))
        self.image_capteurR.setPixmap(
            QtGui.QPixmap('images/img_R'+format))
        self.image_capteurG.setPixmap(
            QtGui.QPixmap('images/img_G'+format))
        self.image_capteurB.setPixmap(
            QtGui.QPixmap('images/img_B'+format))

    def action_import_image(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(
            filter="Image Files (*.png *.jpg)")[0]
        if filePath:
            self.image = Image.open(filePath)
            format = filePath[-4:]
            actions_image.enregistre_image_RGB(self.image, format)

            self.image_capteur.setPixmap(
                QtGui.QPixmap(filePath))
            self.image_capteurR.setPixmap(
                QtGui.QPixmap('images/img_R'+format))
            self.image_capteurG.setPixmap(
                QtGui.QPixmap('images/img_G'+format))
            self.image_capteurB.setPixmap(
                QtGui.QPixmap('images/img_B'+format))

    def action_import_bruit(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(
            filter="Image Files (*.png *.jpg)")[0]
        if filePath:
            self.image_bruit = Image.open(filePath)
            self.image_capteur_Bruit.setPixmap(
                QtGui.QPixmap(filePath))

    def init_GLwidget(self):
        self.gl_Graph = gl.GLViewWidget()
        self.gl_Graph.setGeometry(0, 50, 1000, 800)
        self.gl_Graph.setWindowTitle("Graphique 3D")

        axes = gl.GLAxisItem()
        axes.setSize(10, 10, 10)
        self.gl_Graph.addItem(axes)

    def affiche_plot3D(self):
        self.gl_Graph.show()

    def action_LO(self):
        if self.image != 0:
            if len(self.liste_moyenne) != 0:
                self.longDonde.emit(self.liste_moyenne)
            else:
                self.plot_moyenne_graph()
        else:
            self.textBrowser.append("Il n'y a pas d'image à traiter")

    @ QtCore.pyqtSlot(list, list, list)
    def recoitLongDonde(self, liste, x, y):
        self.plot_LO.setData(x, y)
        actions_image.enregistrer_LO(liste)
        self.update_tab_donne_LO()

    def init_worker(self):
        self.worker = classeThreads.Worker()
        self.worker_thread = QtCore.QThread()

        self.port_ouvert.connect(self.worker.read_port)
        self.worker.read.connect(self.recoitPort)

        self.port_capture.connect(self.worker.capture)
        self.worker.image.connect(self.recoitCapture)

        self.port_capture_bruit.connect(self.worker.capture_bruit)

        self.matRGB.connect(self.worker.liste_moy)
        self.worker.liste_moyenne.connect(self.recoitListeMoyenne)

        self.longDonde.connect(self.worker.longeur_donde)
        self.worker.liste_LO.connect(self.recoitLongDonde)

        self.test_bruit_signal.connect(self.worker.test_bruit)
        self.worker.test_bruitSignal.connect(self.recoitTest_bruit)

        self.test_Cap_pixel.connect(self.worker.test_images)
        self.worker.zvaleur.connect(self.recoitCapPixel)
        self.worker.updateProgressBar.connect(self.updateProgressBar)

        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

    def enregistrer_imageSous(self):
        name = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Enregistrer capture', filter="Image Files (*.jpg)")[0]
        self.image.save(name)

    def test_bruit(self):
        try:
            self.test_bruit_signal.emit(self.sp)
        except Exception:
            self.textBrowser.append("Ouvrir un port série")

    @ QtCore.pyqtSlot(str)
    def recoitTest_bruit(self, text):
        self.textBrowser.append(text)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = camera_GUI()
    window.show()
    app.exec_()
