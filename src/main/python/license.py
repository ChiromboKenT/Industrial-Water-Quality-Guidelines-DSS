#--------------------------------------------------------------------------------------------------------License Window--------------------------------------------------------
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
class LicenseWindow(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.ctx = args[0]
        uic.loadUi(self.ctx.get_license,self)
