import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import actions_image


class camera_GUI(QtWidgets.QMainWindow):

    def __init__(self):
        super(camera_GUI, self).__init__()
        uic.loadUi("camera_GUI.ui", self)
        self.setWindowTitle('OV5642 GUI')
        self.nom_portUSB = ''
        self.sp = 0
        self.image = 0
        self.afficher_port_dispo()

        self.bouton_vider.clicked.connect(self.action_bouton_vider)
        self.bouton_capture.clicked.connect(self.action_bouton_capture)
        self.actionQuitter.triggered.connect(
            QtWidgets.QApplication.instance().quit)
        self.actionOuvrir.triggered.connect(self.action_ouvrir)

    def action_bouton_vider(self):
        self.textBrowser.clear()

    def action_bouton_capture(self):
        try:
            self.image = actions_image.capture(self.sp)
            self.image_capteur.setPixmap(QtGui.QPixmap('img_ARDUCAM.jpg'))
        except Exception as err:
            print(err)

    def afficher_port_dispo(self):
        #list = actions_image.list_port()
        list = ['COM1', 'COM2', 'COM3']
        group = QtWidgets.QActionGroup(self.menuNom)
        for port in list:
            action = QtWidgets.QAction(port, self.menuNom, checkable=True)
            action.triggered.connect(self.setNom_portUSB)
            self.menuNom.addAction(action)
            group.addAction(action)
        group.setExclusive(True)

    def setNom_portUSB(self):
        for port in self.menuNom.actions():
            if port.isChecked():
                self.nom_portUSB = port.text()

    def action_ouvrir(self):
        try:
            actions_image.init_port(self.nom_portUSB)
        except Exception as err:
            self.textBrowser.append(str(err))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = camera_GUI()
    window.show()
    app.exec_()
