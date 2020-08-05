from PyQt5 import QtWidgets
from PyQt5 import uic


class DialogAide(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(DialogAide, self).__init__(*args, **kwargs)
        uic.loadUi("UI/Dialog_Aide.ui", self)
