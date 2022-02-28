
#--------------------------------------------------------------------------------------------------------About Page-------------------------------------------------------------
from PyQt5.QtWidgets import  QDialog
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from pdfViewer import PDFWindow

class BackgroundWindow(QDialog,qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.ctx = args[0]
        uic.loadUi(self.ctx.get_background,self)

        self.buttonClose.clicked.connect(self.close)
        self.buttonWaterQualityParams.mouseReleaseEvent = self.showWaterQuality
        self.buttonAdverseEffects.mouseReleaseEvent = self.showAdverse
        self.buttonMaterialConstruction.mouseReleaseEvent = self.showMaterial
        self.buttonRiskQuantity.mouseReleaseEvent = self.showRisk

    def showWaterQuality(self, event):
        self.infoWindow = PDFWindow(self,"WaterQuality")
        self.infoWindow.show()

    def showAdverse(self, event):
        self.infoWindow = PDFWindow(self,"adverseEffects")
        self.infoWindow.show()

    def showRisk(self, event):
        self.infoWindow = PDFWindow(self,"risk")
        self.infoWindow.show()
    def showMaterial(self, event):
        self.infoWindow = PDFWindow(self,"material")
        self.infoWindow.show()
       