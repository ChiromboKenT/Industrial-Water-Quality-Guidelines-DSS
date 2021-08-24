from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import  QMainWindow,QFileDialog

from PyQt5 import  QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import uic


from Proxy import ProxyModel
class WaterQualityWindow(QMainWindow, qtw.QWidget):
    updateVisual = qtc.pyqtSignal()
    def __init__(self, *args, **kwargs):
        super(WaterQualityWindow, self).__init__()
        self.ctx = args[0]
        uic.loadUi(self.ctx.get_waterQuality, self)
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.center()

        water_materials = ['Carbon Steel','Concrete'
        ,'Monel-Lead/Copper Alloys','Plastic','Stainless steel 304/304L'
        ,'Stainless steel 316/316L','Stainless steel Alloy 20','Stainless steel 904L'
        ,'Duplex Stainless Steel','Membranes']

        #Comboboxes
        model_material = qtg.QStandardItemModel()
        for material in water_materials:
            model_material.appendRow(qtg.QStandardItem(f"{material}"))
        self.materialComboBox.setModel(ProxyModel(model_material, 'Select Material...'))
        self.materialComboBox.setCurrentIndex(0)
        self.materialComboBox.currentTextChanged.connect(self.materialSelectionChanged)

        self.materialComboBox.setStyleSheet("selection-background-color:#127281")

        #buttons
        self.exportToPdf.hide()
        self.exportToPdf.clicked.connect(self.printPDF)
        self.buttonAbout_2.clicked.connect(self.showAbout)
        self.buttonProceed.clicked.connect(self.materialValidate)
        self.pb_minimize_2.clicked.connect(self.maximizeWindow)
        self.buttonProceed.setStyleSheet(
                """ 
                    QPushButton{
                        padding:7px 0;border:2px solid rgb(12, 75, 85);color:#fff;background:rgb(12, 75, 85);border-radius:8px
                    }                    
                    QPushButton:hover{
                        padding:7px 0;border:2px solid rgb(12, 75, 85);color:#fff;background:#127281;border-radius:8px
                    }
                """
            )
        self.buttonBack.setStyleSheet(
                """ 
                    QPushButton{
                        padding:7px 0;border:2px solid rgb(12, 75, 85);background:#fff;color:rgb(12, 75, 85);border-radius:8px
                    }                    
                    QPushButton:hover{
                        padding:7px 0;border:2px solid rgb(12, 75, 85);background:#dadada;color:rgb(12, 75, 85);border-radius:8px
                    }
                """
        )
        self.buttonAbout_2.setStyleSheet(
                """ 
                    QPushButton{
                        background:transparent;border-radius:10px;border:2px solid rgb(245, 245, 245);color:#fff;padding:5px 0
                    }                   
                    QPushButton:hover{
                        background:#127281;border-radius:10px;border:2px solid rgb(245, 245, 245);color:#fff;padding:5px 0
                    }
                """
        )
        self.buttonHelp_2.setStyleSheet(
                """ 
                    QPushButton{
                        background:transparent;border-radius:10px;border:2px solid rgb(245, 245, 245);color:#fff;padding:5px 0
                    }                   
                    QPushButton:hover{
                        background:#127281;border-radius:10px;border:2px solid rgb(245, 245, 245);color:#fff;padding:5px 0
                    }
                """
        )
        self.pushButton_2.setStyleSheet(
                """ 
                    QPushButton{
                        background:transparent;border-radius:10px;border:2px solid rgb(245, 245, 245);color:#fff;padding:5px 0
                    }                   
                    QPushButton:hover{
                        background:#127281;border-radius:10px;border:2px solid rgb(245, 245, 245);color:#fff;padding:5px 0
                    }
                """
        )

        self.buttonBack.clicked.connect(self.showBack)

        #Signals
        self.updateVisual.connect(self.levelDisplay)
        self.oldPos = self.pos()
    def maximizeWindow(self):
        if(self.isMaximized()):
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = qtc.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def materialValidate(self):
        if(self.materialComboBox.currentIndex()== 0):
            msg = qtw.QMessageBox()
            msg.setText("Please specifiy the material of construction")
            msg.setWindowTitle("Missing Input Information")
            msg.setStyleSheet("QmessageBox QLabel{min-width: "+str(300)+"px;}")
            msg.exec_()
            if(msg.result() == 1024):
                self.materialComboBox.setFocus()
                self.materialComboBox.setStyleSheet("border:1px solid #ffcccb;")
        else:
            self.showNext()
    def materialSelectionChanged(self):
        self.materialComboBox.setStyleSheet("border-color:#303030; background-color:#f7f7f7")

    def showNext(self):
        material = self.materialComboBox.currentText()
        #Calculate the next Report
        
        fileNames = {
            'Carbon Steel' : "CarbonSteel",
            'Concrete' : "Concrete",
            'Monel-Lead/Copper Alloys' : "Alloy",
            'Plastic' : "Plastic",
            'Stainless steel 304/304L' : "304",
            'Stainless steel 316/316L' : "316L",
            'Stainless steel Alloy 20' : "SteelAlloy20",
            'Stainless steel 904L' : "904L",
            'Duplex Stainless Steel' : "DuplexSS",
            "Membranes" : "Membranes"
        }
        self.label_25.setText(f'Results: {material}')

        self.webEnginePage = QWebEnginePage()
        self.webEnginePage.setHtml(self.ctx.retrieve_html(fileNames[material]))
        self.webEngineView.setPage(self.webEnginePage)
        self.webEngineView.setContextMenuPolicy(qtc.Qt.NoContextMenu)

        
        self.stackedWidget.setCurrentIndex(1)
        self.buttonProceed.hide()
        self.showMaximized()
        self.updateVisual.emit()

    def showBack(self):
        if(self.stackedWidget.currentIndex() > 0):
            self.showNormal()
            self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() - 1)
        else:
            self.ui_main = self.ctx.main_window
            self.ui_main.show()
            self.close()
        self.buttonProceed.show()
        
            
        self.updateVisual.emit()
          
        
    def printPDF(self):
            fn, _ = QFileDialog.getSaveFileName(self, 'Export PDF', None, 'PDF files (.pdf);;All Files()')
            if fn != '':
                if qtc.QFileInfo(fn).suffix() == "" : fn += '.pdf'
                try:
                    self.webEnginePage.printToPdf(fn)
                    self.updateStatusBar_2("green", f"Successfully saved PDF Report in {fn}")
                except Exception as e:
                    self.updateStatusBar_2("red", f"Failed to save PDF Report")

    def showAbout(self):
        self.about_window = self.ctx.about_window
        self.about_window.show()
    def center(self):
        multiplier_x = 1
        multiplier_y = 1.1
        cursor_pos = qtw.QApplication.desktop().cursor().pos()
        screen = qtw.QApplication.desktop().screenNumber(cursor_pos)
        pos_x = qtw.QDesktopWidget().screenGeometry(screen).center().x()
        pos_x -= self.frameGeometry().center().x() * multiplier_x
        pos_y = qtw.QDesktopWidget().screenGeometry(screen).center().y()
        pos_y -= self.frameGeometry().center().y() * multiplier_y
        self.move(pos_x, pos_y)

    def updateStatusBar_2(self,color,message):
        self.statusBarText.setStyleSheet(f'color:{color};background-color:#fff')
        self.statusBarText.setText(message)

        qtc.QTimer.singleShot(10000, self.statusBarReset_2)
    def statusBarReset_2(self):
        self.statusBarText.setStyleSheet(f'color:;background-color:#fff')
        self.statusBarText.setText(" ")
    @qtc.pyqtSlot()
    def levelDisplay(self):
        if(self.stackedWidget.currentIndex() == 0):
            self.exportToPdf.hide()
            self.step_4.setStyleSheet("background-color:rgb(12, 75, 85);border:3px solid rgb(223, 223, 223);border-radius:13px")
            self.step_5.setStyleSheet("background-color:rgb(223, 223, 223);border:none;border-radius:7px")
    
            self.step_4.setMinimumWidth(26)
            self.step_4.setMaximumWidth(26)
            self.step_4.setMinimumHeight(26)
            self.step_4.setMaximumHeight(26)

            self.step_5.setMinimumWidth(15)
            self.step_5.setMaximumWidth(15)
            self.step_5.setMinimumHeight(15)
            self.step_5.setMaximumHeight(15)

            self.buttonCurrentPage1_2.setStyleSheet("background:#fff;border-top:1px solid rgb(12, 75, 85);border-bottom:1px solid rgb(12, 75, 85);border-right:12px solid rgb(12, 75, 85);padding:5px;color:rgb(12, 75, 85)")
            self.buttonCurrentPage2_2.setStyleSheet("background:rgb(223, 223, 223);border-top:1px solid rgb(12, 75, 85);border-bottom:1px solid rgb(12, 75, 85);border-right:none;padding:5px;color:rgb(12, 75, 85)")

            self.buttonCurrentPage1_2.setEnabled(True)
            self.buttonCurrentPage2_2.setEnabled(False)

        elif(self.stackedWidget.currentIndex() == 1):
            self.exportToPdf.show()
            self.step_4.setStyleSheet("background-color:rgb(223, 223, 223);border:none;border-radius:7px")
            self.step_5.setStyleSheet("background-color:rgb(12, 75, 85);border:3px solid rgb(223, 223, 223);border-radius:13px")

            self.step_4.setMinimumWidth(15)
            self.step_4.setMaximumWidth(15)
            self.step_4.setMinimumHeight(15)
            self.step_4.setMaximumHeight(15)

            self.step_5.setMinimumWidth(26)
            self.step_5.setMaximumWidth(26)
            self.step_5.setMinimumHeight(26)
            self.step_5.setMaximumHeight(26)

            self.buttonCurrentPage1_2.setStyleSheet("background:rgb(223, 223, 223);border-top:1px solid rgb(12, 75, 85);border-bottom:1px solid rgb(12, 75, 85);border-right:none;padding:5px;color:rgb(12, 75, 85)")
            self.buttonCurrentPage2_2.setStyleSheet("background:#fff;border-top:1px solid rgb(12, 75, 85);border-bottom:1px solid rgb(12, 75, 85);border-right:12px solid rgb(12, 75, 85);padding:5px;color:rgb(12, 75, 85)")

            self.buttonCurrentPage1_2.setEnabled(False)
            self.buttonCurrentPage2_2.setEnabled(True)
        else:
            
            self.step_4.setStyleSheet("background-color:rgb(223, 223, 223);border:none;border-radius:7px")
            self.step_5.setStyleSheet("background-color:rgb(223, 223, 223);border:none;border-radius:7px")
            
            self.step_4.setMinimumWidth(15)
            self.step_4.setMaximumWidth(15)
            self.step_4.setMinimumHeight(15)
            self.step_4.setMaximumHeight(15)

            self.step_5.setMinimumWidth(15)
            self.step_5.setMaximumWidth(15)
            self.step_5.setMinimumHeight(15)
            self.step_5.setMaximumHeight(15)

            self.buttonCurrentPage1_2.setEnabled(True)
            self.buttonCurrentPage2_2.setEnabled(False)
            
            self.buttonCurrentPage1_2.setStyleSheet("background:rgb(223, 223, 223);border-top:1px solid rgb(12, 75, 85);border-bottom:1px solid rgb(12, 75, 85);border-right:none;padding:5px;color:rgb(12, 75, 85)")
            self.buttonCurrentPage2_2.setStyleSheet("background:rgb(223, 223, 223);border-top:1px solid rgb(12, 75, 85);border-bottom:1px solid rgb(12, 75, 85);border-right:none;padding:5px;color:rgb(12, 75, 85)")
