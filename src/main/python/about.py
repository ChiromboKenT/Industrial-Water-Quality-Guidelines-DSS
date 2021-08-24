#--------------------------------------------------------------------------------------------------------About Page-------------------------------------------------------------
from PyQt5.QtWidgets import  QDialog
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic

class AboutWindow(QDialog,qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.ctx = args[0]
        uic.loadUi(self.ctx.get_about,self)

        #buttons
        self.buttonViewLicense.clicked.connect(self.view_license)
    
    def view_license(self):
        self.license_window = self.ctx.license_window
        self.license_window.show()
