from pdfViewer import PDFWindow
from PyQt5.QtWebEngineWidgets import QWebEnginePage

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import uic

from reporting import GeneratePDF
from Proxy import ProxyModel

#-----------------------------------------------------------------------------------------------------Global Variables-----------------------------------------------------------
Field_data = {
            
            "unit" : 0,
            "material": 0,
            "unit" : 0,
            "corrosion": False,
            "scaling": False,
            "fouling": False
        }
class AppWindow(qtw.QMainWindow):

    updateVisual = qtc.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(AppWindow, self).__init__()
        self.ctx = args[0]
        uic.loadUi(self.ctx.get_appWindow, self)
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.center()

        #Frame
        self.frame_fitness.mousePressEvent = self.PressEvent
        self.frame_fitness.mouseMoveEvent = self.MoveEvent
        self.frame_fitness.mouseReleaseEvent = self.PressRelease

        self.sector_data = self.ctx.import_data
        self.sector_keys = self.sector_data.iloc[:,0]
        self.level = "Advanced"
        self.data = self.ctx.import_inputs_data 
        self.exportToPdf.hide()
        #Populate Comboboxes
        self.updateVisual.connect(self.levelDisplay)

        model_place = qtg.QStandardItemModel()
        
        for key in self.sector_keys:
            model_place.appendRow(qtg.QStandardItem(f"{key}"))

        self.sectorComboBox.setModel(ProxyModel(model_place, 'Select Industry...'))
        self.sectorComboBox.setCurrentIndex(0)
        self.sectorComboBox.currentIndexChanged.connect(self.sector_selectionchange)

        
        
        #Combobox for Unit
        model_unit = qtg.QStandardItemModel()
        self.unitComboBox.setModel(ProxyModel(model_unit, 'Select Unit...'))
        self.unitComboBox.setCurrentIndex(0)
        #Combobox for Material
        model_material = qtg.QStandardItemModel()
        self.materialComboBox.setModel(ProxyModel(model_material, 'Select Material...'))
        self.materialComboBox.setCurrentIndex(0)
        self.materialComboBox.currentTextChanged.connect(self.validate_type)
        self.materialComboBox.currentTextChanged.connect(self.material_selectionChange)
        #Radio Buttons
        self.radioButton.hide()
        self.radioButton_2.hide()
        self.liningFrame.hide()
        self.label_14.setText("The processing unit refers to the component or unit to be assessed.")

        #Buttons
        self.buttonProceed.clicked.connect(self.SectorValidate)
        self.buttonHelp.clicked.connect(self.showManual)
        self.pushButton.clicked.connect(self.showBackGround)
    
        self.buttonBack.clicked.connect(self.showBack)
        self.buttonUserInfoEdit.clicked.connect(self.editUserInfo)
        self.buttonAbout.clicked.connect(self.showAbout)
        self.buttonSelectAll.clicked.connect(self.selectAll)
        self.buttonSelectNone.clicked.connect(self.selectNone)
        self.buttonCurrentPage1.clicked.connect(lambda: self.navigateToPage(0))
        self.buttonCurrentPage2.clicked.connect(lambda: self.navigateToPage(1))
        self.pb_minimize_2.clicked.connect(self.maximizeWindow)
        self.buttonSelectNone.hide()
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
        self.buttonAbout.setStyleSheet(
                """ 
                    QPushButton{
                        background:transparent;border-radius:10px;border:2px solid rgb(245, 245, 245);color:#fff;padding:5px 0
                    }                   
                    QPushButton:hover{
                        background:#127281;border-radius:10px;border:2px solid rgb(245, 245, 245);color:#fff;padding:5px 0
                    }
                """
        )
        self.buttonHelp.setStyleSheet(
                """ 
                    QPushButton{
                        background:transparent;border-radius:10px;border:2px solid rgb(245, 245, 245);color:#fff;padding:5px 0
                    }                   
                    QPushButton:hover{
                        background:#127281;border-radius:10px;border:2px solid rgb(245, 245, 245);color:#fff;padding:5px 0
                    }
                """
        )
        self.pushButton.setStyleSheet(
                """     
                    QPushButton{
                        background:transparent;border-radius:10px;border:2px solid rgb(245, 245, 245);color:#fff;padding:5px 0
                    }               
                    QPushButton:hover{
                        background:#127281;border-radius:10px;border:2px solid rgb(245, 245, 245);color:#fff;padding:5px 0
                    }
                """
        )
        self.buttonSelectAll.setStyleSheet(
                """ 
                    QPushButton{
                        padding:4px 10px;border:2px solid rgb(12, 75, 85);color:#fff;background:rgb(12, 75, 85);border-radius:8px;
                    }                   
                    QPushButton:hover{
                        padding:4px 10px;border:2px solid rgb(12, 75, 85);color:#fff;background:#127281;border-radius:8px;
                    }
                """
            )
        self.buttonSelectNone.setStyleSheet(
                """ 
                    QPushButton{
                        padding:4px 10px;border:2px solid rgb(12, 75, 85);color:#fff;background:rgb(12, 75, 85);border-radius:8px;
                    }                   
                    QPushButton:hover{
                        padding:4px 10px;border:2px solid rgb(12, 75, 85);color:#fff;background:#127281;border-radius:8px;
                    }
                """
            )
        self.buttonUserInfoEdit.setStyleSheet(
                """ 
                    QPushButton{
                        padding:7px 10px;border:2px solid rgb(12, 75, 85);color:#fff;background:rgb(12, 75, 85);border-radius:10px
                    }                   
                    QPushButton:hover{
                        padding:7px 10px;border:2px solid rgb(12, 75, 85);color:#fff;background:#127281;border-radius:10px
                    }
                """
            )
        self.materialComboBox.setStyleSheet("selection-background-color:#127281")
        self.unitComboBox.setStyleSheet("selection-background-color:#127281")
        self.sectorComboBox.setStyleSheet("selection-background-color:#127281")
        self.exportToPdf.clicked.connect(self.ExportToPdf)
        self.oldPos = self.pos()

    def showBackGround(self):
        self.background_window = self.ctx.background_window
        self.background_window.show()
        
    def maximizeWindow(self):
        if(self.isMaximized()):
            self.showNormal()
        else:
            self.showMaximized()
    def ExportToPdf(self):
        self.pdfReport = GeneratePDF(self.ui_reports_window.data)
        html = self.pdfReport.generateHTML()
        self.doc = QWebEnginePage()
        self.doc.setHtml(html)
        self.printPDF()
    def showManual(self):
        self.infoWindow = PDFWindow(self,"manual")
        self.infoWindow.show()
           
    def printPDF(self):
            fn, _ = qtw.QFileDialog.getSaveFileName(self, 'Export PDF',"Industrial Water Quality Guidelines Report.pdf", 'PDF files (.pdf);;All Files()')
            if fn != '':
                try:
                    self.doc.printToPdf(fn)
                    self.updateStatusBar_2("green", f"Successfully saved PDF Report in {fn}")
                except Exception as e:
                    self.updateStatusBar_2("red", f"Failed to save PDF Report")
                    print(e)

    def PressEvent(self, event):
        
        if event.button() == qtc.Qt.LeftButton:
            self.oldPos = event.globalPos()
            self.frame_fitness.setCursor(qtg.QCursor(qtc.Qt.ClosedHandCursor))
            super().mousePressEvent(event)
    def PressRelease(self,event):
        if event.button() == qtc.Qt.LeftButton:
            self.frame_fitness.setCursor(qtg.QCursor(qtc.Qt.OpenHandCursor))
            super().mouseReleaseEvent(event)
    def MoveEvent(self, event):
        delta = qtc.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    @qtc.pyqtSlot()
    def levelDisplay(self):
        self.exportToPdf.hide()
        if(self.stackedWidget.currentIndex() == 0):
            
            self.step_1.setStyleSheet("background-color:rgb(12, 75, 85);border:3px solid rgb(223, 223, 223);border-radius:13px")
            self.step_2.setStyleSheet("background-color:rgb(223, 223, 223);border:none;border-radius:7px")
            self.step_3.setStyleSheet("background-color:rgb(223, 223, 223);border:none;border-radius:7px")

            self.step_1.setMinimumWidth(26)
            self.step_1.setMaximumWidth(26)
            self.step_1.setMinimumHeight(26)
            self.step_1.setMaximumHeight(26)

            self.step_2.setMinimumWidth(15)
            self.step_2.setMaximumWidth(15)
            self.step_2.setMinimumHeight(15)
            self.step_2.setMaximumHeight(15)

            self.step_3.setMinimumWidth(15)
            self.step_3.setMaximumWidth(15)
            self.step_3.setMinimumHeight(15)
            self.step_3.setMaximumHeight(15)

            self.buttonCurrentPage1.setStyleSheet("background:#fff;border-top:1px solid rgb(12, 75, 85);border-bottom:1px solid rgb(12, 75, 85);border-right:12px solid rgb(12, 75, 85);padding:5px;color:rgb(12, 75, 85)")
            self.buttonCurrentPage2.setStyleSheet("background:rgb(223, 223, 223);border-top:1px solid rgb(12, 75, 85);border-bottom:1px solid rgb(12, 75, 85);border-right:none;padding:5px;color:rgb(12, 75, 85)")
            self.buttonCurrentPage3.setStyleSheet("background:rgb(223, 223, 223);border-top:1px solid rgb(12, 75, 85);border-bottom:1px solid rgb(12, 75, 85);border-right:none;padding:5px;color:rgb(12, 75, 85)")
            self.buttonCurrentPage1.setEnabled(True)
            self.buttonCurrentPage2.setEnabled(False)
            self.buttonCurrentPage3.setEnabled(False)
        elif(self.stackedWidget.currentIndex() == 1):
            self.step_1.setStyleSheet("background-color:rgb(223, 223, 223);border:none;border-radius:7px")
            self.step_2.setStyleSheet("background-color:rgb(12, 75, 85);border:3px solid rgb(223, 223, 223);border-radius:13px")
            self.step_3.setStyleSheet("background-color:rgb(223, 223, 223);border:none;border-radius:7px")

            self.step_1.setMinimumWidth(15)
            self.step_1.setMaximumWidth(15)
            self.step_1.setMinimumHeight(15)
            self.step_1.setMaximumHeight(15)

            self.step_2.setMinimumWidth(26)
            self.step_2.setMaximumWidth(26)
            self.step_2.setMinimumHeight(26)
            self.step_2.setMaximumHeight(26)

            self.step_3.setMinimumWidth(15)
            self.step_3.setMaximumWidth(15)
            self.step_3.setMinimumHeight(15)
            self.step_3.setMaximumHeight(15)

            self.buttonCurrentPage1.setStyleSheet("background:rgb(223, 223, 223);border-top:1px solid rgb(12, 75, 85);border-bottom:1px solid rgb(12, 75, 85);border-right:none;padding:5px;color:rgb(12, 75, 85)")
            self.buttonCurrentPage2.setStyleSheet("background:#fff;border-top:1px solid rgb(12, 75, 85);border-bottom:1px solid rgb(12, 75, 85);border-right:12px solid rgb(12, 75, 85);padding:5px;color:rgb(12, 75, 85)")
            self.buttonCurrentPage3.setStyleSheet("background:rgb(223, 223, 223);border-top:1px solid rgb(12, 75, 85);border-bottom:1px solid rgb(12, 75, 85);border-right:none;padding:5px;color:rgb(12, 75, 85)")
            self.buttonCurrentPage1.setEnabled(True)
            self.buttonCurrentPage2.setEnabled(True)
            self.buttonCurrentPage3.setEnabled(False)

            
        
        else:
            self.exportToPdf.show()
            self.step_1.setStyleSheet("background-color:rgb(223, 223, 223);border:none;border-radius:7px")
            self.step_2.setStyleSheet("background-color:rgb(223, 223, 223);border:none;border-radius:7px")
            self.step_3.setStyleSheet("background-color:rgb(12, 75, 85);border:3px solid rgb(223, 223, 223);border-radius:13px")

            self.step_1.setMinimumWidth(15)
            self.step_1.setMaximumWidth(15)
            self.step_1.setMinimumHeight(15)
            self.step_1.setMaximumHeight(15)

            self.step_2.setMinimumWidth(15)
            self.step_2.setMaximumWidth(15)
            self.step_2.setMinimumHeight(15)
            self.step_2.setMaximumHeight(15)

            self.step_3.setMinimumWidth(26)
            self.step_3.setMaximumWidth(26)
            self.step_3.setMinimumHeight(26)
            self.step_3.setMaximumHeight(26)

            self.buttonCurrentPage1.setStyleSheet("background:rgb(223, 223, 223);border-top:1px solid rgb(12, 75, 85);border-bottom:1px solid rgb(12, 75, 85);border-right:none;padding:5px;color:rgb(12, 75, 85)")
            self.buttonCurrentPage2.setStyleSheet("background:rgb(223, 223, 223);border-top:1px solid rgb(12, 75, 85);border-bottom:1px solid rgb(12, 75, 85);border-right:none;padding:5px;color:rgb(12, 75, 85)")
            self.buttonCurrentPage3.setStyleSheet("background:#fff;border-top:1px solid rgb(12, 75, 85);border-bottom:1px solid rgb(12, 75, 85);border-right:12px solid rgb(12, 75, 85);padding:5px;color:rgb(12, 75, 85)")

            self.buttonCurrentPage1.setEnabled(True)
            self.buttonCurrentPage2.setEnabled(True)
            self.buttonCurrentPage3.setEnabled(True)

        

    def selectAll(self):
        if(self.checkBoxCorrosion_2.isEnabled() == True):
            self.checkBoxCorrosion_2.setChecked(True)
        if(self.checkBoxFouling_2.isEnabled() == True):
            self.checkBoxFouling_2.setChecked(True)
        if(self.checkBoxScaling_2.isEnabled() == True):
            self.checkBoxScaling_2.setChecked(True)

    def selectNone(self):
        if(self.checkBoxCorrosion_2.isEnabled() == True):
            self.checkBoxCorrosion_2.setChecked(False)
        if(self.checkBoxFouling_2.isEnabled() == True):
            self.checkBoxFouling_2.setChecked(False)
        if(self.checkBoxScaling_2.isEnabled() == True):
            self.checkBoxScaling_2.setChecked(False)

    def editUserInfo(self):
        data = {
            "fullName" : self.fullName.text(),
            "role": self.role.text(),
            "company": self.company.text(),
            "location": self.location.text(),
            "email":self.email.text(),
            "description":self.description.text()
        }
        self.user_info = self.ctx.user_info_setter(data)
        self.user_info.show()
        
        if(self.user_info.exec() == 1):
            updated_data = self.user_info.data
            print(updated_data)
            self.fullName.setText(updated_data["fullName"])
            self.role.setText(updated_data["role"])
            self.company.setText(updated_data["company"])
            self.location.setText(updated_data['location'])
            self.email.setText(updated_data["email"])
            self.description.setText(updated_data["description"])
    def showAbout(self):
        self.about_window = self.ctx.about_window
        self.about_window.show()
    def validate_type(self):
        self.checkBoxCorrosion_2.setEnabled(True)
        self.checkBoxFouling_2.setEnabled(True)
        self.checkBoxScaling_2.setEnabled(True)
        if(self.materialComboBox.currentText() == "Plastic"):

            self.checkBoxCorrosion_2.setChecked(False)
            self.checkBoxCorrosion_2.setEnabled(False)
            
            
        elif(self.materialComboBox.currentText() == "Membranes" ):
            self.checkBoxCorrosion_2.setChecked(False)
            self.checkBoxScaling_2.setChecked(False)
            self.checkBoxCorrosion_2.setEnabled(False)
            self.checkBoxScaling_2.setEnabled(False)
        else:
            self.checkBoxCorrosion_2.setEnabled(True)
            self.checkBoxFouling_2.setEnabled(True)
            self.checkBoxScaling_2.setEnabled(True)
    def center(self):
        multiplier_x = 1
        multiplier_y = 1
        cursor_pos = qtw.QApplication.desktop().cursor().pos()
        screen = qtw.QApplication.desktop().screenNumber(cursor_pos)
        pos_x = qtw.QDesktopWidget().screenGeometry(screen).center().x()
        pos_x -= self.frameGeometry().center().x() * multiplier_x
        pos_y = qtw.QDesktopWidget().screenGeometry(screen).center().y()
        pos_y -= self.frameGeometry().center().y() * multiplier_y
        self.move(pos_x, pos_y)

    def sector_selectionchange(self):
        self.sectorComboBox.setStyleSheet("border-color:#303030; background-color:#f7f7f7;")
        tempSelect = self.sectorComboBox.currentText()
        sector_unitList = self.sector_data.loc[self.sector_keys == tempSelect].iloc[:,1:].dropna(axis='columns')
        sector_materials = ['Carbon Steel','Concrete'
        ,'Monel-Lead/Copper Alloys','Plastic','Stainless steel 304/304L'
        ,'Stainless steel 316/316L','Stainless steel Alloy 20','Stainless steel 904L'
        ,'Duplex Stainless Steel']
        model_unit = qtg.QStandardItemModel()
        model_materials = qtg.QStandardItemModel()
        
        for unit in sector_unitList:
            model_unit.appendRow(qtg.QStandardItem(f"{sector_unitList[unit].values[0]}"))
        for material in sector_materials:
            model_materials.appendRow(qtg.QStandardItem(f"{material}"))

        self.unitComboBox.setModel(ProxyModel(model_unit, 'Select Unit...'))
        self.unitComboBox.setCurrentIndex(0)

        self.materialComboBox.setModel(ProxyModel(model_materials, 'Select Material...'))
        self.materialComboBox.setCurrentIndex(0)

        
        self.unitComboBox.currentTextChanged.connect(self.unit_selectionChange)
        self.materialComboBox.setStyleSheet("selection-background-color:#127281")
        self.unitComboBox.setStyleSheet("selection-background-color:#127281")
        self.sectorComboBox.setStyleSheet("selection-background-color:#127281")
    def unit_selectionChange(self):
        text = self.unitComboBox.currentText()
        print(f"Unit Text: {text}" )
        self.unitComboBox.setStyleSheet("border-color:#303030; background-color:#f7f7f7;selection-background-color:#127281")
        if(text == "Grids/Screens" or text == "Screens" or text == "Sand Filters" or text == "Membranes"):
            self.frame_15.hide()
            self.verticalLayout_13.addStretch(2)
        else:
            self.frame_15.show()
        
        if(text == "Dams" or text == "Reactor" or text == "Tanks"):
            self.radioButton.show()
            self.radioButton_2.show()
            self.liningFrame.show()
            self.label_14.setText("The processing unit refers to the component or unit to be assessed.\nNot Lined - Applies to storage units without lining considerations. \nLined - Applies to storage unit that has any lining considerations.")
            
        else:
            
            self.radioButton.hide()
            self.radioButton_2.hide()
            self.liningFrame.hide()
            self.label_14.setText("The processing unit refers to the component or unit to be assessed.")
        self.materialComboBox.setStyleSheet("selection-background-color:#127281")
        self.sectorComboBox.setStyleSheet("selection-background-color:#127281")

    def material_selectionChange(self):

        self.materialComboBox.setStyleSheet("border-color:#303030; background-color:#f7f7f7;selection-background-color:#127281")
        self.unitComboBox.setStyleSheet("selection-background-color:#127281")
        self.sectorComboBox.setStyleSheet("selection-background-color:#127281")
    def SectorValidate(self):
        if(self.sectorComboBox.currentIndex() == 0):
            msg = qtw.QMessageBox()
            msg.setText("Please specifiy the Sector")
            msg.setWindowTitle("Missing Input Information")
            msg.setStyleSheet("QmessageBox QLabel{min-width: "+str(300)+"px;}")
            msg.exec_()
            if(msg.result() == 1024):
                self.sectorComboBox.setFocus()
                self.sectorComboBox.setStyleSheet("border:1px solid #ff4500;selection-background-color:#127281")
        elif(self.unitComboBox.currentIndex() == 0):
                msg = qtw.QMessageBox()
                msg.setText("Please specifiy the Unit")
                msg.setWindowTitle("Missing Input Information")
                msg.setStyleSheet("QmessageBox QLabel{min-width: "+str(300)+"px;}")
                msg.exec_()
                if(msg.result() == 1024):
                    self.unitComboBox.setFocus()
                    self.unitComboBox.setStyleSheet("border:1px solid #ff4500;")
        elif(self.materialComboBox.currentIndex() == 0 and self.frame_15.isHidden() == False):
                msg = qtw.QMessageBox()
                msg.setText("Please specifiy the material of construction")
                msg.setWindowTitle("Missing Input Information")
                msg.setStyleSheet("QmessageBox QLabel{min-width: "+str(300)+"px;}")
                msg.exec_()
                if(msg.result() == 1024):
                    self.materialComboBox.setFocus()
                    self.materialComboBox.setStyleSheet("border:1px solid #ffcccb;selection-background-color:#127281")
        elif(self.radioButton.isHidden() == False and (self.radioButton.isChecked() == False and self.radioButton_2.isChecked() == False)):
                msg = qtw.QMessageBox()
                msg.setText("Please specifiy if the storage unit is lined or not lined ")
                msg.setWindowTitle("Missing Input Information")
                msg.setStyleSheet("QmessageBox QLabel{min-width: "+str(300)+"px;}")
                msg.exec_()
                if(msg.result() == 1024):
                    self.radioButton.setFocus()
        elif(self.radioButton_2.isChecked() == True and self.radioButton_2.isHidden() == False ):
            msg = qtw.QMessageBox()
            msg.setText("Confirm with the supplier about liner specifications and limitations. Unfortunately this assessment is limited to non lined units.")
            msg.setWindowTitle("Lined Units")
            msg.setStyleSheet("QmessageBox QLabel{min-width: "+str(300)+"px;}")
            msg.exec_()
        elif(self.checkBoxCorrosion_2.isChecked() == True or self.checkBoxScaling_2.isChecked() == True or self.checkBoxFouling_2.isChecked() == True):
            if(self.radioButton.isHidden() == True or self.radioButton.isChecked() == True):
                self.showNext()
        
        else:
            msg = qtw.QMessageBox()
            msg.setText("Please select at least one assessment type!")
            msg.setWindowTitle("Missing Input Information")
            msg.setStyleSheet("QmessageBox QLabel{min-width: "+str(300)+"px;}")
            msg.exec_()
        self.updateVisual.emit()
    @qtc.pyqtSlot(str,str)
    def updateStatusBar(self,color,message):
        self.statusBarText.setStyleSheet(f'color:{color};background-color:#fff')
        self.statusBarText.setText(message)

        qtc.QTimer.singleShot(3000, self.statusBarReset)
    @qtc.pyqtSlot()
    def statusBarReset(self):
        self.statusBarText.setStyleSheet(f'color:;background-color:#fff')
        self.statusBarText.setText(" ")
    def updateStatusBar_2(self,color,message):
        self.statusBarText.setStyleSheet(f'color:{color};background-color:#fff')
        self.statusBarText.setText(message)

        qtc.QTimer.singleShot(10000, self.statusBarReset_2)
    def statusBarReset_2(self):
        self.statusBarText.setStyleSheet(f'color:;background-color:#fff')
        self.statusBarText.setText(" ")
    def showNext(self):
        data = {
            "fullName" : self.fullName.text(),
            "role": self.role.text(),
            "company": self.company.text(),
            "location": self.location.text(),
            "email":self.email.text(),
            "description":self.description.text()
        }
        assesmentDetails = {
            "level" : "Advanced",
            "sector": self.sectorComboBox.currentText(),
            "unit": self.unitComboBox.currentText(),
            "material" : self.materialComboBox.currentText(),
            "user": data
        }
        if(self.frame_15.isHidden() == True):
            assesmentDetails['material'] = "Membranes"       
            
        #Store Selections
        Field_data['sector'] = self.sectorComboBox.currentIndex()
        Field_data['unit'] = self.unitComboBox.currentIndex()
        Field_data['material'] = self.materialComboBox.currentIndex()
        Field_data['corrosion'] = self.checkBoxCorrosion_2.isChecked()
        Field_data['scaling'] = self.checkBoxScaling_2.isChecked()
        Field_data['fouling'] = self.checkBoxFouling_2.isChecked()
        #Validate

         
        

        typeLabels = []
        if(self.checkBoxCorrosion_2.isChecked() == True):
            typeLabels.append("Corrosion")
        if(self.checkBoxScaling_2.isChecked() == True):
            typeLabels.append("Scaling")
        if(self.checkBoxFouling_2.isChecked() == True):
            typeLabels.append("Fouling") 
        
        
        typeList = []
        for label in typeLabels:
            for x in self.data[assesmentDetails['material']][label]:
                typeList.append(x)

        assesmentDetails['type'] = typeLabels
        assesmentDetails['inputs'] = list(set(typeList))
                  
        if(self.stackedWidget.currentIndex() == 0):
            self.ui_inputs = self.ctx.input_window_setter(assesmentDetails)
            self.ui_inputs.statusBarSignal.connect(self.updateStatusBar)
            self.ui_inputs.reportsSignal.connect(self.showReports)
            self.stackedWidget.insertWidget(1,self.ui_inputs)
            self.stackedWidget.setCurrentIndex(1)
        elif(self.stackedWidget.currentIndex() == 1):
            self.ui_inputs.reportsSignal.connect(self.showReports)
            self.ui_inputs.Validate()
            

            print("Report")

        # Closing file
    @qtc.pyqtSlot(dict,str,list,dict,dict,dict)
    def showReports(self,analysis,material,assesments,inputs,user,info):
        self.ui_reports_window = self.ctx.report_window_setter(analysis,material,assesments,inputs,user,info)
        self.stackedWidget.insertWidget(2,self.ui_reports_window)
        self.stackedWidget.setCurrentIndex(2)
        self.buttonProceed.hide()
        self.setMinimumWidth(1024)
        self.showMaximized()
    def navigateToPage(self, indx):
        self.showNormal()
        self.stackedWidget.setCurrentIndex(indx)
        self.buttonProceed.show()
        self.updateVisual.emit()

    def showBack(self):
        if(self.stackedWidget.currentIndex() > 0):
            self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() - 1)
        else:
            self.ui_main = self.ctx.main_window
            self.ui_main.show()
            self.close()
        self.buttonProceed.show()
        if(self.stackedWidget.currentIndex() > 0):
            self.showNormal()
        self.updateVisual.emit()
      
