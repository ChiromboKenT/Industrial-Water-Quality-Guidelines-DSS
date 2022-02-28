from typing import cast
from PyQt5.QtWidgets import QApplication, QDialog,  QLabel, QWidget


from PyQt5 import QtCore, QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import uic
import math
import webbrowser
#--------------------------------------------------------------------------------------------------------Reports Window-----------------------------------------------------------

class AlignDelegate(qtw.QStyledItemDelegate):
    def createEditor(self,parent,option,index):
        print('createEditor event fired')
        return
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = qtc.Qt.AlignCenter
        option.font = qtg.QFont("Times",10)

class AlignLeftDelegate(qtw.QStyledItemDelegate):
    def createEditor(self,parent,option,index):
        print('createEditor event fired')
        return
    def initStyleOption(self, option, index):
        super(AlignLeftDelegate, self).initStyleOption(option, index)
        option.displayAlignment = qtc.Qt.AlignLeft
        option.font = qtg.QFont("Times",10)
        

class ReportsWindow(QDialog, qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.ctx = args[0]
        uic.loadUi(self.ctx.get_report,self)
        
        self.analysis = args[1]
        self.material = args[2]
        self.assessments = args[3]
        self.inputs = list(args[4].items())
        self.user = args[5]
        self.info = args[6]
        self.units = self.ctx.import_units_data
        self.assessment_alloy = self.ctx.import_assessment_alloy
        self.assessment_carbon = self.ctx.import_assessment_carbon
        self.assessment_concrete = self.ctx.import_assessment_concrete
        self.assessment_plastic = self.ctx.import_assessment_plastic
        self.assessment_membrane = self.ctx.import_assessment_membrane
        self.assessment_ss = self.ctx.import_assessment_ss
     
        
        self.setWindowTitle("Fitness-of-use Report")
       
        self.report_data = self.parseTable()
        
        if(self.material == "Membranes"):
            self.label_20.setText("")
            self.labelMaterial.setText("")
            self.material = "-"

        self.data = {
            "report_data" :self.report_data,
            "material" : self.material,
            "assessments" : self.assessments,
            "units" : self.units,
            "info" : self.info,
            "user" : self.user,
            "inputs" : self.inputs
        }
        #Report User Info
        self.reportFullName.setText(self.user['fullName'])
        self.reportJobTitle.setText(self.user['role'])
        self.reportCompany.setText(self.user['company'])
        self.reportLocation.setText(self.user['location'])
        self.reportEmail.setText(self.user['email'])
        self.reportDescription.setPlainText(self.user['description'])

        #Basic Info Tab
        typeText = ", ".join(self.assessments)
        self.labelTypeAssess.setText(typeText)
        self.labelSector.setText(self.info['sector'])
        self.labelUnit.setText(self.info['unit'])
        self.labelMaterial.setText(self.material)

       
            
        

        #Specific Inputs Tab
        inputsSize = len(self.inputs)
        if(inputsSize %2 == 0):
            inputListLeft  =  self.inputs[0:int(inputsSize/2)]
            inputListRight = self.inputs[int(inputsSize/2):]
        else:
            inputListLeft = self.inputs[0:int((inputsSize+1)/2)]
            inputListRight = self.inputs[int((inputsSize+1)/2):]

        
        for i, item in enumerate(inputListLeft):
            paramLabel = QLabel()
            paramValue = QLabel()
            paramUnits = QLabel()

            paramLabel.setText(item[0])
            try:
                if(type(item[1]) == bool):
                    strVal = "YES" if item[1] == True else "NO"
                    paramValue.setText(strVal)
                else:
                    paramValue.setText(f'{round(item[1],2)}')
            except Exception as e:
                print(f"Error setting TRUE FALSE VALUE left: {e}")
                paramValue.setText(f'{item[1]}')
            try:
                paramUnits.setText(self.units[item[0]]['unit'])
            except Exception as e:
                paramUnits.setText(self.units[item[0]]['unit'][0])
                print(f"Report Grid units: {e}")

            
            self.gridReportLeft.addWidget(paramLabel,i+1,0,alignment=qtc.Qt.AlignTop)
            self.gridReportLeft.addWidget(paramValue,i+1,1,alignment=qtc.Qt.AlignTop)
            self.gridReportLeft.addWidget(paramUnits,i+1,2,alignment=qtc.Qt.AlignTop)
        self.gridReportLeft.addItem(qtw.QSpacerItem(20, 10, qtw.QSizePolicy.Fixed,qtw.QSizePolicy.Expanding))
        


        for i, item in enumerate(inputListRight):
            paramLabel = QLabel()
            paramValue = QLabel()
            paramUnits = QLabel()

            paramLabel.setText(item[0])
            try:
                if(type(item[1]) == bool):
                    strVal = "YES" if item[1] == True else "NO"
                    paramValue.setText(strVal)
                else:
                    paramValue.setText(f'{round(item[1],2)}')
            except Exception as e:
                print(f"Error setting TRUE FALSE VALUE right: {e}")
                paramValue.setText(f'{item[1]}')
            try:
                paramUnits.setText(self.units[item[0]]['unit'])
            except Exception as e:
                paramUnits.setText(self.units[item[0]]['unit'][0])
                print(f"Report Grid units {i}: {e}")

            self.gridReportRight.addWidget(paramLabel,i+1,0,alignment=qtc.Qt.AlignTop)
            self.gridReportRight.addWidget(paramValue,i+1,1,alignment=qtc.Qt.AlignTop)
            self.gridReportRight.addWidget(paramUnits,i+1,2,alignment=qtc.Qt.AlignTop)
        try:
            
            self.gridReportRight.addItem(qtw.QSpacerItem(20, 10, qtw.QSizePolicy.Fixed,qtw.QSizePolicy.Expanding))
        except Exception as e:
            print("Error adding Spacer: {e}") 

        assesment_keys = list(self.report_data.keys())
        tabNumber = 0
        for key in assesment_keys:
            self.tab1 = QWidget()
            self.resultTab.addTab(self.tab1, f'{key}')
            self.tab1UI(key,self.report_data,tabNumber)
            tabNumber = tabNumber + 1

        self.resultTab.currentChanged.connect(self.TabChanger)
        myText = self.resultTab.tabText(self.resultTab.currentIndex())
        if(myText != "Scaling"):
            self.linkToToolFrame.hide()

        self.linkToTool.clicked.connect(self.open_webbrowser)
   

    def open_webbrowser(self): 
        webbrowser.open('http://wrcwebsite.azurewebsites.net/mdocs-posts/stasoft-install/stasoft-install-2/')

    def TabChanger(self):
        myText = self.resultTab.tabText(self.resultTab.currentIndex())
        if(myText != "Scaling"):
            self.linkToToolFrame.hide()
        else :
            self.linkToToolFrame.show()

    def tab1UI(self,key,data,tabNumber):
        styleSheet = "QHeaderView::section{Background-color:#404040;color:#fff;text-align:center;font-weight:900}"

        layout = qtw.QVBoxLayout()
        
        table = qtw.QTableWidget()

        #Colum Count
        table.setColumnCount(5)
        #RowCount
        table.setRowCount(len(data[key]))
        table.setHorizontalHeaderLabels(["  Parameter ","Value"," Risk Category ","Description","Options for Consideration"])
        table.horizontalHeader().setStyleSheet("border: 1px solid #000;background-color:rgb(17, 111, 125);font-weight:700;color:#fff")
        table.horizontalHeader().setSectionResizeMode(0, qtw.QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(1, qtw.QHeaderView.Fixed)
        table.horizontalHeader().setSectionResizeMode(2, qtw.QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(3, qtw.QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(4, qtw.QHeaderView.Stretch)
        table.setWordWrap(True)

        #table.horizontalHeader().resizeSection(1, 90)
        #table.horizontalHeader().resizeSection(1, 120)

        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().hide()
        
        
        table.setStyleSheet(styleSheet)
        #table.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        rowCount = 0

        
        
        

        
        
        for item_key,item_value in data[key].items():
            item1 = qtw.QTableWidgetItem(item_value['Risk'])

            if(item_value["Risk"] == "Unacceptable"):
                item1.setBackground(qtg.QColor(255,0,0))
                item1.setForeground(qtg.QColor(255,255,255))
            elif(item_value["Risk"] == "Tolerable"):
                item1.setBackground(qtg.QColor(255,255,0))
            elif(item_value["Risk"] == "Acceptable"):
                item1.setBackground(qtg.QColor(146,208,80)) 
            elif(item_value["Risk"] == "Ideal"):
                item1.setBackground(qtg.QColor(0,176,240))
            else:
                 item1.setBackground(qtg.QColor(40,40,40))

            if item_key == "Corrosion Rate due to the Pisigan and Shingley Correlation (mmpy)":
                table.setItem(rowCount, 0, qtw.QTableWidgetItem("""Corrosion Rate due to the Pisigan\nand Shingley Correlation (mmpy)"""))
            else:
                table.setItem(rowCount, 0, qtw.QTableWidgetItem(f'{item_key}'))
            try:
                table.setItem(rowCount, 1, qtw.QTableWidgetItem(f"{round(item_value['Index'],2)}"))
                
            except TypeError as e:
                table.setItem(rowCount, 1, qtw.QTableWidgetItem(f"{item_value['Index']}"))

            descriptionCell =  qtw.QTableWidgetItem(f"{item_value['Description']}")
            descriptionCell.setFont(qtg.QFont("Times",10))

            treatmentCell =  qtw.QTableWidgetItem(f"{item_value['Treatment']}")
            treatmentCell.setFont(qtg.QFont("Times",10))

            table.setItem(rowCount, 2, item1)
            table.setItem(rowCount, 3, descriptionCell)
            table.setItem(rowCount, 4,treatmentCell)
            delegateAlign = AlignDelegate(table)
            leftDelegateAlign = AlignLeftDelegate(table)

            table.setItemDelegateForColumn(0, delegateAlign)
            table.setItemDelegateForColumn(1, delegateAlign)
            table.setItemDelegateForColumn(2, delegateAlign)
            table.setItemDelegateForColumn(3, leftDelegateAlign)
            table.setItemDelegateForColumn(4, leftDelegateAlign)
            rowCount = rowCount + 1
            
           
            
        table.setStyleSheet("font-size:13px;border:none")
        table.resizeRowsToContents()
        
        table.setMaximumHeight(self.getQTableHeight(table))
        table.setMinimumSize(self.getQTableWidgetSize(table))
        
       
        table.resizeRowsToContents()
        
        
        
        

        layout.addWidget(table,0)
        layout.setAlignment(table, qtc.Qt.AlignTop)
        layout.addSpacerItem(qtw.QSpacerItem(20, 10, qtw.QSizePolicy.Fixed,qtw.QSizePolicy.Expanding))
        layout.addStretch()
        self.resultTab.setTabText(tabNumber,f"{key}")
        self.tab1.setLayout(layout)  

    def showBack(self):
        self.inputs_window = self.ctx.input_window()
        self.inputs_window.show()
        self.close()    
    def getQTableWidgetSize(self,table):
        w = table.verticalHeader().width() + 4  # +4 seems to be needed
        for i in range(table.columnCount()):
            w += table.columnWidth(i)  # seems to include gridline (on my machine)
        h = table.horizontalHeader().height() + 4
        for i in range(table.rowCount()):
            h += math.floor(table.rowHeight(i) * 0.5)
        return QtCore.QSize(h, w)

    def getQTableHeight(self,table):
        
        h = table.horizontalHeader().height() + 5
        for i in range(table.rowCount()):
            h += table.rowHeight(i)
        return h

    def parseTable(self):
        analysis = self.analysis
        results = {

        }
        if(self.material == "Stainless steel 304/304L" or self.material == "Stainless steel 316/316L" or 
        self.material == "Stainless steel Alloy 20" or self.material == "Stainless steel 904L" or self.material == "Duplex Stainless Steel" ):
            for assessment in self.assessments:
                if(assessment == "Corrosion"):
                    _data = self.assessment_ss["corrosion"] 
                    Corrosion = {}
                    RyznerRes = {}
                    FlourideRes = {}
                    prenRes = {}
                    PittingRes = {}
                    chlorideRes = {}

                    #------------------------------------------------------Corrosion Ryzner-------------------------------------
                    if(analysis['ryznar'] >= 8.5):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Severe Corrosion due to lack of CaCO\u2083 formation"
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["unacceptable"]
                    elif(analysis['ryznar'] < 8.5 and analysis['ryznar'] >= 7.8):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Mild Corrosion due to lack of CaCO\u2083 formation"
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["tolerable"]
                    elif(analysis['ryznar'] < 7.8 and analysis['ryznar'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Mild Corrosion due to lack of CaCO\u2083 formation"
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["acceptable"]
                    else:
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Minimal to no corrosion "
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["ideal"]
                    Corrosion["Ryznar Index"] = RyznerRes
                    #--------------------------------------------------Corrosion Flouride-------------------------------------------
                    try:
                        if(analysis["Flouride"] > 10):
                            FlourideRes["Index"] = round(analysis['Flouride'], 2)
                            FlourideRes["Description"] = "Severe pitting corrosion due to Flouride"
                            FlourideRes["Risk"] = "Unacceptable"
                            FlourideRes["Treatment"] = _data["Flouride"]["unacceptable"]
                        elif(analysis["Flouride"] <= 10 and analysis["Flouride"] > 5):
                            FlourideRes["Index"] = round(analysis['Flouride'], 2)
                            FlourideRes["Description"] = "Moderate pitting corrosion due to Flouride"
                            FlourideRes["Risk"] = "Tolerable"
                            FlourideRes["Treatment"] = _data["Flouride"]["tolerable"]
                        elif(analysis["Flouride"] <= 5 and analysis["Flouride"] >= 1):
                            FlourideRes["Index"] = round(analysis['Flouride'], 2)
                            FlourideRes["Description"] = "Mild pitting corrosion due to Flouride"
                            FlourideRes["Risk"] = "Acceptable"
                            FlourideRes["Treatment"] = _data["Flouride"]["acceptable"]
                        else:
                            FlourideRes["Index"] = round(analysis['Flouride'], 2)
                            FlourideRes["Description"] = "No pitting corrosion due to Flouride"
                            FlourideRes["Risk"] = "Ideal"
                            FlourideRes["Treatment"] = _data["Flouride"]["ideal"]
                        Corrosion["Pitting Corrosion due to Flouride (mg/l) "] = FlourideRes
                    except Exception as e:
                        print(f"Flouride Concentration Error- Report: {e}")
                        
                    #-------------------------------------------Langlier------------------------------------------------------------
                    langlierRes = {}
                    try:
                        if(analysis["Langlier"] >= 5):
                            langlierRes["Description"] = "Severe Corrosion due to CaCO\u2083"
                            langlierRes["Risk"] = "Unacceptable"
                            langlierRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                        elif(analysis["Langlier"] < 5 and analysis["Langlier"] >= 2):
                            langlierRes["Description"] = "Mild Corrosion due to CaCO\u2083"
                            langlierRes["Risk"] = "Tolerable"
                            langlierRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""

                        elif(analysis["Langlier"] < 2 and analysis["Langlier"] >= 0.5):
                            langlierRes["Description"] = "Mild Corrosion due to CaCO\u2083"
                            langlierRes["Risk"] = "Acceptable"
                            langlierRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                        else:
                            langlierRes["Description"] = "Minimal to no risk of corrosion"
                            langlierRes["Risk"] = "Ideal"
                            langlierRes["Treatment"] = "No Treatment"
                        langlierRes["Index"] = round(analysis["Langlier"],2)
                        Corrosion["Langelier Saturation Index"] = langlierRes
                    except Exception as e :
                        print(f"Error Lanlier: {e}")
                    #-------------------------------------------Pitting Corrosion----------------------------------------------------
                    try:
                        if(self.material == "Stainless steel 304/304L"):
                            prenRes["Index"] = 20
                            prenRes["Description"] = "Low sea water resistance"
                            prenRes["Risk"] = "Unacceptable"
                            prenRes["Treatment"] = _data["Pitting Corrosion"]["unacceptable"]
                            #Chloride Concentration
                            try:
                                limit = 50 if(analysis['pH'] < 7 and analysis['Temperature'] > 35) else 200
                                if(analysis["Chloride"] < limit):
                                    chlorideRes["Risk"] = "Acceptable"
                                    chlorideRes["Treatment"] = _data["Pitting Corrosion"]["acceptable"]
                                else:
                                    
                                    chlorideRes["Risk"] = "Unacceptable"
                                    chlorideRes["Treatment"] = """1. Prevent corrosion through adjusting the index by reducing the concentration of Cl\n2. Change construction material.\nCl can be reduced through Ion Exchange or Reverse Osmosis - partial stream of full stream."""
                                chlorideRes['Index'] = round(analysis["Chloride"], 2)
                                chlorideRes["Description"] = "-"
                                
                                Corrosion["Chloride Concentration (mg/l)"] = chlorideRes
                            except Exception as e:
                                print(f"Error Chloride Corrosion 304 {e}")
                                
                            
                            #Critical Pitting Temperature
                            try:
                                if(analysis["Temperature"] < 18):
                                    PittingRes["Index"] = analysis["Temperature"]
                                    PittingRes["Description"] = "No risk of pitting corrosion"
                                    PittingRes["Risk"] = "Acceptable"
                                    PittingRes["Treatment"] = "No Treatment"
                                else:
                                    PittingRes["Index"] = analysis["Temperature"]
                                    PittingRes["Description"] = "Risk of pitting corrosion"
                                    PittingRes["Risk"] = "Tolerable"  
                                    PittingRes["Treatment"] = """Reduce the temperature of the water\nOR\nConsider an alternative Material of Construction"""
                                Corrosion["Critical Pitting Temperature"] = PittingRes  
                            except Exception as e:
                                print(f'Error Critical Pitting Temperature 304 {e}')
                                
                        elif(self.material == "Stainless steel 316/316L" ):
                            prenRes["Index"] = 25
                            prenRes["Description"] = "Low sea water resistance"
                            prenRes["Risk"] = "Unacceptable"
                            prenRes["Treatment"] = _data["Pitting Corrosion"]["unacceptable"]
                            #Chloride Concentration
                            try:
                                limit = 100 if(analysis['pH'] < 7 and analysis['Temperature'] > 35) else 300
                                if(analysis["Chloride"] < limit):
                                    chlorideRes["Risk"] = "Acceptable"
                                    chlorideRes["Treatment"] = "No Treatment"
                                else:
                                    
                                    chlorideRes["Risk"] = "Unacceptable"
                                    chlorideRes["Treatment"] = """1. Prevent corrosion through adjusting the index by reducing the concentration of Cl\n2. Change construction material.\nCl can be reduced through Ion Exchange or Reverse Osmosis - partial stream of full stream."""
                                chlorideRes['Index'] = round(analysis["Chloride"], 2)
                                chlorideRes["Description"] = "-"
                                Corrosion["Chloride Concentration (mg/l)"] = chlorideRes
                            except Exception as e:
                                print(f"Error Chloride Corrosion 316 {e}")
                                
                            #Critical Pitting Temperature
                            try:
                                if(analysis["Temperature"] < 20):
                                    PittingRes["Index"] = analysis["Temperature"]
                                    PittingRes["Description"] = "No risk of pitting corrosion"
                                    PittingRes["Risk"] = "Acceptable"
                                    PittingRes["Treatment"] = "No Treatment"
                                else:
                                    PittingRes["Index"] = analysis["Temperature"]
                                    PittingRes["Description"] = "Risk of pitting corrosion"
                                    PittingRes["Risk"] = "Tolerable"  
                                    PittingRes["Treatment"] = """Reduce the temperature of the water\nOR\nConsider an alternative Material of Construction"""
                                Corrosion["Critical Pitting Temperature"] = PittingRes  
                            except Exception as e:
                                print(f'Error Critical Pitting Temperature 304 {e}')
                                
                        elif(self.material == "Stainless steel Alloy 20"):
                            prenRes["Index"] = 30
                            prenRes["Description"] = "Low sea water resistance"
                            prenRes["Risk"] = "Unacceptable"
                            prenRes["Treatment"] = _data["Pitting Corrosion"]["unacceptable"]
                            #Chloride Concentration
                            try:
                                limit = 150 if(analysis['pH'] < 7 and analysis['Temperature'] > 35) else 400
                                if(analysis["Chloride"] < limit):
                                    chlorideRes["Risk"] = "Acceptable"
                                    chlorideRes["Treatment"] = "No Treatment"
                                else:
                                    
                                    chlorideRes["Risk"] = "Unacceptable"
                                    chlorideRes["Treatment"] = """1. Prevent corrosion through adjusting the index by reducing the concentration of Cl\n2. Change construction material.\nCl can be reduced through Ion Exchange or Reverse Osmosis - partial stream of full stream."""
                                chlorideRes['Index'] = round(analysis["Chloride"], 2)
                                chlorideRes["Description"] = "-"
                                
                                Corrosion["Chloride Concentration (mg/l)"] = chlorideRes
                            except Exception as e:
                                print(f"Error Chloride Corrosion Aloy 20 {e}")
                                
                            #Critical Pitting Temperature
                            try:
                                if(analysis["Temperature"] < 90):
                                    PittingRes["Index"] = analysis["Temperature"]
                                    PittingRes["Description"] = "No risk of pitting corrosion"
                                    PittingRes["Risk"] = "Acceptable"
                                    PittingRes["Treatment"] = "No Treatment"
                                else:
                                    PittingRes["Index"] = analysis["Temperature"]
                                    PittingRes["Description"] = "Risk of pitting corrosion"
                                    PittingRes["Risk"] = "Tolerable"  
                                    PittingRes["Treatment"] = """Reduce the temperature of the water\nOR\nConsider an alternative Material of Construction"""
                                Corrosion["Critical Pitting Temperature"] = PittingRes  
                            except Exception as e:
                                print(f'Error Critical Pitting Temperature 304 {e}')
                                
                        elif(self.material == "Stainless steel 904L"):
                            prenRes["Index"] = 36
                            prenRes["Description"] = "Sea water resistance"
                            prenRes["Risk"] = "Acceptable"
                            prenRes["Treatment"] = _data["Pitting Corrosion"]["acceptable"]

                            #Chloride Concentration
                            try:
                                limit = 2000 if(analysis['pH'] < 7 and analysis['Temperature'] > 35) else 3000
                                if(analysis["Chloride"] < limit):
                                    chlorideRes["Risk"] = "Acceptable"
                                    chlorideRes["Treatment"] = "No Treatment"
                                else:
                                    
                                    chlorideRes["Risk"] = "Unacceptable"
                                    chlorideRes["Treatment"] = """1. Prevent corrosion through adjusting the index by reducing the concentration of Cl\n2. Change construction material.\nCl can be reduced through Ion Exchange or Reverse Osmosis - partial stream of full stream."""
                                chlorideRes['Index'] = round(analysis["Chloride"], 2)
                                chlorideRes["Description"] = "-"
                                
                                Corrosion["Chloride Concentration (mg/l)"] = chlorideRes
                            except Exception as e:
                                print(f"Error Chloride Corrosion 904 {e}")
                                
                            #Critical Pitting Temperature
                            try:
                                if(analysis["Temperature"] < 40):
                                    PittingRes["Index"] = analysis["Temperature"]
                                    PittingRes["Description"] = "No risk of pitting corrosion"
                                    PittingRes["Risk"] = "Acceptable"
                                    PittingRes["Treatment"] = "No Treatment"
                                else:
                                    PittingRes["Index"] = analysis["Temperature"]
                                    PittingRes["Description"] = "Risk of pitting corrosion"
                                    PittingRes["Risk"] = "Tolerable" 
                                    PittingRes["Treatment"] = """Reduce the temperature of the water\nOR\nConsider an alternative Material of Construction"""
                                Corrosion["Critical Pitting Temperature"] = PittingRes  
                            except Exception as e:
                                print(f'Error Critical Pitting Temperature 304 {e}')
                                
                        elif(self.material == "Duplex Stainless Steel"):
                            prenRes["Index"] = 46
                            prenRes["Description"] = "Sea water resistance with temp > 30°C"
                            prenRes["Risk"] = "Acceptable"
                            prenRes["Treatment"] = _data["Pitting Corrosion"]["acceptable"]

                            #Chloride Concentration
                            try:
                                limit = 3000 if(analysis['pH'] < 7 and analysis['Temperature'] > 35) else 3600
                                if(analysis["Chloride"] < limit):
                                    chlorideRes["Risk"] = "Acceptable"
                                    chlorideRes["Treatment"] = "No Treatment"
                                else:
                                    
                                    chlorideRes["Risk"] = "Unacceptable"
                                    chlorideRes["Treatment"] = """1. Prevent corrosion through adjusting the index by reducing the concentration of Cl\n2. Change construction material.\nCl can be reduced through Ion Exchange or Reverse Osmosis - partial stream of full stream."""
                                chlorideRes['Index'] = round(analysis["Chloride"], 2)
                                chlorideRes["Description"] = "-"
                                Corrosion["Chloride Concentration (mg/l)"] = chlorideRes
                            except Exception as e:
                                print(f"Error Chloride Corrosion duplex {e}")
                                
                            #Critical Pitting Temperature
                            try:
                                if(analysis["Temperature"] < 65):
                                    PittingRes["Index"] = analysis["Temperature"]
                                    PittingRes["Description"] = "No risk of pitting corrosion"
                                    PittingRes["Risk"] = "Acceptable"
                                    PittingRes["Treatment"] = "No Treatment"
                                else:
                                    PittingRes["Index"] = analysis["Temperature"]
                                    PittingRes["Description"] = "Risk of pitting corrosion"
                                    PittingRes["Risk"] = "Tolerable" 
                                    PittingRes["Treatment"] = """Reduce the temperature of the water\nOR\nConsider an alternative Material of Construction"""
                                Corrosion["Critical Pitting Temperature (°C)"] = PittingRes  
                            except Exception as e:
                                print(f'Error Critical Pitting Temperature 304 {e}')
                                 
                    except Exception as e:
                        print("Error Pitting Corrosion: {e}")
                        
                    Corrosion["PREN of Alloy"] = prenRes
                    #-------------------------------End of Corrosion-------------------------------------------------------------------------------------------------------------------
                    results["Corrosion"] = Corrosion
                elif(assessment == "Scaling"):
                    _data = self.assessment_ss["scaling"] 
                    Scaling = {}
                    RyznerRes = {}
                    silicaSteamRes = {}
                    magnesiumSilicaRes = {}
                    calciumSulphateRes = {}
                   
                    #------------------------------------------------------Ryzner for Scaling---------------------------
                    if(analysis['ryznar'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "No scale formation due to CaCO\u2083"
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["ideal"]
                    elif(analysis['ryznar'] < 6.8 and analysis['ryznar'] >= 6.2):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Moderate Scale Formation due to CaCO\u2083"
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["acceptable"]
                    elif(analysis['ryznar'] < 6.2 and analysis['ryznar'] >= 5.5):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Mild Scale Formation due to CaCO\u2083"
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["tolerable"]
                    else:
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Severe Scale Formation due to CaCO\u2083"
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["unacceptable"]
                    Scaling["Ryznar Index"] = RyznerRes

                    #Langlier-------------------------------------------------------------------------------------------------
                    langlierResScaling = {}
                    try:
                        if(analysis["Langlier"] > 3.5):
                            langlierResScaling["Description"] = "Severe Scale Formation due to CaCO\u2083"
                            langlierResScaling["Risk"] = "Unacceptable"
                            langlierResScaling["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""

                        elif(analysis["Langlier"] <= 3.5 and analysis["Langlier"] > 2):
                            langlierResScaling["Description"] = "Mild Scale Formation due to CaCO\u2083"
                            langlierResScaling["Risk"] = "Tolerable"
                            langlierResScaling["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""

                        elif(analysis["Langlier"] <= 2 and analysis["Langlier"] > 0):
                            langlierResScaling["Description"] = "Moderate Scale Formation due to CaCO\u2083"
                            langlierResScaling["Risk"] = "Acceptable"
                            langlierResScaling["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""
                        else:
                            langlierResScaling["Description"] = "No scale formation due to CaCO\u2083"
                            langlierResScaling["Risk"] = "Ideal"
                            langlierResScaling["Treatment"] = "No Treatment"
                        langlierResScaling["Index"] = round(analysis["Langlier"],2)
                        Scaling["Langelier Saturation Index"] = langlierResScaling
                    except Exception as e:
                        print("Error Langlier: {e}")
                
                    #-----------------------------------------------------Silica Concentration in Steam-----------------------
                    try:
                        if(analysis["Silica Concentration in steam"] <= 0.02):
                            silicaSteamRes["Index"] = round(analysis["Silica Concentration in steam"],2)
                            silicaSteamRes["Description"] = "Minimal silica film formation"
                            silicaSteamRes["Risk"] = "Ideal"
                            silicaSteamRes["Treatment"] = _data["Silica Concentration in steam"]["ideal"]
                        else:
                            silicaSteamRes["Index"] = round(analysis["Silica Concentration in steam"],2)
                            silicaSteamRes["Description"] = "High silica film formation"
                            silicaSteamRes["Risk"] = "Tolerable"
                            silicaSteamRes["Treatment"] = _data["Silica Concentration in steam"]["tolerable"]
                        Scaling["Scaling due to Silica in Steam (mg/l)"] = silicaSteamRes
                   
                    except Exception as e:
                        print(f"Error Silica in Steam SS")
                     #---------------------------------------------------Silica and Magnesium -------------------------------------------
                    try:
                        mgLimit = 0
                        if(analysis['pH'] >= 8.5):
                            mgLimit = 6000
                        elif(analysis['pH'] < 8.5 and analysis['pH'] > 7.5):
                            mgLimit = 12000
                        elif(analysis['pH'] <= 7.5):
                            mgLimit = 17000
                        
                        if(analysis['SilicaMagnesium'] < mgLimit):
                            magnesiumSilicaRes['Description'] = "Acceptable Magnesium Silicate Scaling"
                            magnesiumSilicaRes['Risk'] = "Acceptable"
                            magnesiumSilicaRes['Treatment'] = "No Treatment"
                        else:
                            magnesiumSilicaRes['Description'] = "Unacceptable Magnesium Silicate Scaling"
                            magnesiumSilicaRes['Risk'] = "Unacceptable"
                            magnesiumSilicaRes['Treatment'] = f"""If this value decreases to below {mgLimit}, then it will be acceptable"""
                        magnesiumSilicaRes["Index"] = analysis['SilicaMagnesium']
                        Scaling["Magnesium Silicate Scale Formation"] = magnesiumSilicaRes
                    except Exception as e:
                        print(f'Error magnesium * silica SS : {e}')
                    #-------------------------------------------------------Calcium Sulphate------------------------------------------------
                    try:
                        calSulLimit = 10000000 if(analysis['WaterTreatment'] == True) else 50000
                        if(analysis["SilicaMagnesium"] < calSulLimit):
                            calciumSulphateRes["Description"] = "Acceptable Calcium Sulphate Scaling"
                            calciumSulphateRes["Risk"] = "Acceptable"
                            calciumSulphateRes["Treatment"] = "-"
                        else:
                            calciumSulphateRes["Description"] = "Unacceptable Calcium Sulphate Scaling"
                            calciumSulphateRes["Risk"] = "Unacceptable"
                            calciumSulphateRes["Treatment"] = f"""If this value decreases to below {calSulLimit},\nthen it will be acceptable"""
                        calciumSulphateRes["Index"] = analysis["SilicaMagnesium"]
                        Scaling["Calcium Sulphate Scale Formation"] = calciumSulphateRes
                    except Exception as e:
                        print(f"Error Calcium Sulphate SS: {e}") 
                    #-----------------------------------------------------Phosphate Scaling------------------------------------------   
                    calciumPhosphateRes = {}
                    try:
                        if(analysis["CalciumPhosphate"] <= 0):
                            calciumPhosphateRes["Index"] = round(analysis["CalciumPhosphate"],2)
                            calciumPhosphateRes["Description"] = "Balance – Low potential for scale formation"
                            calciumPhosphateRes["Risk"] = "Ideal"
                            calciumPhosphateRes["Treatment"] = "No Treatment"
                        else:
                            calciumPhosphateRes["Index"] = round(analysis["CalciumPhosphate"],2)
                            calciumPhosphateRes["Description"] = "Potential of Scale Formation"
                            calciumPhosphateRes["Risk"] = "Tolerable"
                            calciumPhosphateRes["Treatment"] = "Treatment Recommended"
                        Scaling["Calcium phosphate scaling"] = calciumPhosphateRes
                   
                    except Exception as e:
                        print(f"Error Phosphate Assemnent Parse Table: {e}")
                    results["Scaling"] = Scaling
                elif(assessment == "Fouling"):
                    _data = self.assessment_ss["fouling"] 
                    Fouling = {}
                    ssFoulRes = {}
                    if(analysis['Suspended Solids'] >= 30):
                        ssFoulRes["Description"] = "High Chance of Fouling"
                        ssFoulRes["Risk"] = "Unacceptable"
                        ssFoulRes["Treatment"] = _data["suspended solids"]['unacceptable']
                    elif(analysis['Suspended Solids'] < 30 and analysis['Suspended Solids'] >= 15):
                        ssFoulRes["Description"] = "Moderate Fouling"
                        ssFoulRes["Risk"] = "Tolerable"
                        ssFoulRes["Treatment"] = """Treatment May Be Needed - Upfront filtration pre-treatment\nOR\nChemical treatment by addition of dispersants"""
                    elif(analysis['Suspended Solids'] < 15 and analysis['Suspended Solids'] >= 5):
                        ssFoulRes["Description"] = "Mild of Fouling"
                        ssFoulRes["Risk"] = "Acceptable"
                        ssFoulRes["Treatment"] = _data["suspended solids"]['acceptable']
                    else:
                        ssFoulRes["Description"] = "No Fouling predicted"
                        ssFoulRes["Risk"] = "Ideal"
                        ssFoulRes["Treatment"] = "No treatment"
                    
                    ssFoulRes['Index'] = analysis["Suspended Solids"]
                    Fouling["Suspended Solids Fouling (mg/l)"] = ssFoulRes
                    results["Fouling"] = Fouling
        elif(self.material == "Carbon Steel"):
            for assessment in self.assessments:
                if(assessment == "Corrosion"):
                    _data = self.assessment_carbon["corrosion"] 
                    Corrosion = {}
                    RyznerRes = {}
                    LarsonRes = {}
                    PisiganRes = {}
                    #------------------------------------------------------Corrosion Ryzner-------------------------------------
                    if(analysis['ryznar'] >= 8.5):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Severe Corrosion due to lack of CaCO\u2083 formation"
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["unacceptable"]
                    elif(analysis['ryznar'] < 8.5 and analysis['ryznar'] >= 7.8):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Mild Corrosion due to lack of CaCO\u2083 formation "
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["tolerable"]
                    elif(analysis['ryznar'] < 7.8 and analysis['ryznar'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Mild Corrosion due to lack of CaCO\u2083 formation "
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["acceptable"]
                    else:
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Minimal to no corrosion "
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["ideal"]
                    Corrosion["Ryznar Index"] = RyznerRes

                    #-------------------------------------------Langlier------------------------------------------------------------
                    langlierRes = {}
                    try:
                        if(analysis["Langlier"] >= 5):
                            langlierRes["Description"] = "Severe Corrosion due to CaCO\u2083"
                            langlierRes["Risk"] = "Unacceptable"
                            langlierRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                        elif(analysis["Langlier"] < 5 and analysis["Langlier"] >= 2):
                            langlierRes["Description"] = "Mild Corrosion due to CaCO\u2083"
                            langlierRes["Risk"] = "Tolerable"
                            langlierRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""

                        elif(analysis["Langlier"] < 2 and analysis["Langlier"] >= 0.5):
                            langlierRes["Description"] = "Mild Corrosion due to CaCO\u2083"
                            langlierRes["Risk"] = "Acceptable"
                            langlierRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                        else:
                            langlierRes["Description"] = "Minimal to no risk of corrosion"
                            langlierRes["Risk"] = "Ideal"
                            langlierRes["Treatment"] = "No Treatment"
                        langlierRes["Index"] = round(analysis["Langlier"],2)
                        Corrosion["Langelier Saturation Index"] = langlierRes
                    except Exception as e :
                        print(f"Error Lanlier: {e}")
                    #------------------------------------------------------Corrosion Larson--------------------------------------
                    
                    if(analysis['larson'] >= 1.2):
                        LarsonRes["Description"] = "Severe pitting corrosion"
                        LarsonRes["Risk"] = "Unacceptable"
                        LarsonRes["Treatment"] = _data["Pitting Corrosion"]["unacceptable"]
                    elif(analysis['larson'] < 1.2 and analysis['larson'] >= 1):
                        LarsonRes["Description"] = "Significant pitting corrosion"
                        LarsonRes["Risk"] = "Tolerable"
                        LarsonRes["Treatment"] = _data["Pitting Corrosion"]["tolerable"]
                    elif(analysis['larson'] < 1 and analysis['larson'] >= 0.8):
                        LarsonRes["Description"] = "Mild pitting corrosion"
                        LarsonRes["Risk"] = "Acceptable"
                        LarsonRes["Treatment"] = _data["Pitting Corrosion"]["acceptable"]
                    else:
                        LarsonRes["Description"] = "Minimal risk of pitting corrosion"
                        LarsonRes["Risk"] = "Ideal"
                        LarsonRes["Treatment"] = _data["Pitting Corrosion"]["ideal"]
                    LarsonRes["Index"] = round(analysis["larson"],2)
                    Corrosion[' Larson-Skold Index'] = LarsonRes

                    #---------------------------------------------------------Corrosion Pisigan----------------------------------------
                    try:
                        if(analysis['reticulation']):
                            if(analysis['pisigan corrosion'] > 10):
                                PisiganRes["Description"] = "High corrosion rate - Severe corrosion will be experienced"
                                PisiganRes["Risk"] = "Unacceptable"
                                PisiganRes["Treatment"] = _data["Pisigan Corrosion"]["unacceptable"]
                            elif(analysis['pisigan corrosion'] <= 10 and analysis['pisigan corrosion'] > 5):
                                PisiganRes["Description"] = "Intermediate corrosion rate - Moderate corrosion may be experienced"
                                PisiganRes["Risk"] = "Tolerable"
                                PisiganRes["Treatment"] = _data["Pisigan Corrosion"]["tolerable"]
                            elif(analysis['pisigan corrosion'] <= 5 and analysis['pisigan corrosion'] >= 1):
                                PisiganRes["Description"] = "Intermediate corrosion rate - Mild corrosion may be experienced"
                                PisiganRes["Risk"] = "Acceptable"
                                PisiganRes["Treatment"] = _data["Pisigan Corrosion"]["acceptable"]
                            else:
                                PisiganRes["Description"] = "Low corrosion rate - Minimal corrosion experienced"
                                PisiganRes["Risk"] = "Ideal"
                                PisiganRes["Treatment"] = _data["Pisigan Corrosion"]["ideal"]
                        else:
                            if(analysis['pisigan corrosion'] > 1):
                                PisiganRes["Description"] = "High corrosion rate - Severe corrosion will be experienced"
                                PisiganRes["Risk"] = "Unacceptable"
                                PisiganRes["Treatment"] = _data["Pisigan Corrosion"]["unacceptable"]
                            elif(analysis['pisigan corrosion'] <= 1 and analysis['pisigan corrosion'] >= 0.5):
                                PisiganRes["Description"] = "Intermediate corrosion rate - Moderate corrosion may be experienced"
                                PisiganRes["Risk"] = "Tolerable"
                                PisiganRes["Treatment"] = _data["Pisigan Corrosion"]["tolerable"]
                            elif(analysis['pisigan corrosion'] < 0.5 and analysis['pisigan corrosion'] >= 0.2):
                                PisiganRes["Description"] = "Intermediate corrosion rate - Mild corrosion may be experienced"
                                PisiganRes["Risk"] = "Acceptable"
                                PisiganRes["Treatment"] = _data["Pisigan Corrosion"]["acceptable"]
                            else:
                                PisiganRes["Description"] = "Low corrosion rate - Minimal corrosion experienced"
                                PisiganRes["Risk"] = "Ideal"
                                PisiganRes["Treatment"] = _data["Pisigan Corrosion"]["ideal"]
                        PisiganRes["Index"] = round(analysis['pisigan corrosion'], 2)
                        Corrosion["Corrosion Rate due to the Pisigan and Shingley Correlation (mmpy)"] = PisiganRes
                    except KeyError as e:
                        print("Error For corrosion Rate :{e}")
                    
                    #-------------------------------End of Corrosion-------------------------------------------------------------------------------------------------------------------
                    results["Corrosion"] = Corrosion
                elif(assessment == "Scaling"):
                    _data = self.assessment_carbon["scaling"] 
                    Scaling = {}
                    RyznerRes = {}
                    silicaSteamRes = {}
                    magnesiumSilicaRes = {}
                    calciumSulphateRes = {}


                    #------------------------------------------------------Ryzner for Scaling---------------------------
                    if(analysis['ryznar'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "No scale formation due to CaCO\u2083"
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["ideal"]
                    elif(analysis['ryznar'] < 6.8 and analysis['ryznar'] >= 6.2):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Moderate Scale Formation due to CaCO\u2083"
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["acceptable"]
                    elif(analysis['ryznar'] < 6.2 and analysis['ryznar'] >= 5.5):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Mild Scale Formation due to CaCO\u2083"
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["tolerable"]
                    else:
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Severe Scale Formation due to CaCO\u2083"
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["unacceptable"]
                    Scaling["Ryznar Index"] = RyznerRes
                    
                    #Langlier-------------------------------------------------------------------------------------------------
                    langlierResScaling = {}
                    try:
                        if(analysis["Langlier"] > 3.5):
                            langlierResScaling["Description"] = "Severe Scale Formation due to CaCO\u2083"
                            langlierResScaling["Risk"] = "Unacceptable"
                            langlierResScaling["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""

                        elif(analysis["Langlier"] <= 3.5 and analysis["Langlier"] > 2):
                            langlierResScaling["Description"] = "Mild Scale Formation due to CaCO\u2083"
                            langlierResScaling["Risk"] = "Tolerable"
                            langlierResScaling["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""

                        elif(analysis["Langlier"] <= 2 and analysis["Langlier"] > 0):
                            langlierResScaling["Description"] = "Moderate Scale Formation due to CaCO\u2083"
                            langlierResScaling["Risk"] = "Acceptable"
                            langlierResScaling["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""
                        else:
                            langlierResScaling["Description"] = "No scale formation due to CaCO\u2083"
                            langlierResScaling["Risk"] = "Ideal"
                            langlierResScaling["Treatment"] = "No Treatment"
                        langlierResScaling["Index"] = round(analysis["Langlier"],2)
                        Scaling["Langelier Saturation Index"] = langlierResScaling
                    except Exception as e:
                        print("Error Langlier: {e}")
                    
                    #-----------------------------------------------------Silica Concentration in Steam-----------------------
                    try:
                        if(analysis["Silica Concentration in steam"] <= 0.02):
                            silicaSteamRes["Index"] = analysis["Silica Concentration in steam"]
                            silicaSteamRes["Description"] = "Minimal silica film formation"
                            silicaSteamRes["Risk"] = "Ideal"
                            silicaSteamRes["Treatment"] = _data["Silica Concentration in steam"]["ideal"]
                        else:
                            silicaSteamRes["Index"] = analysis["Silica Concentration in steam"]
                            silicaSteamRes["Description"] = "High silica film formation"
                            silicaSteamRes["Risk"] = "Tolerable"
                            silicaSteamRes["Treatment"] = _data["Silica Concentration in steam"]["tolerable"]
                        Scaling["Scaling due to Silica in Steam"] = silicaSteamRes
                   
                    except Exception as e:
                        print(f"Error Silica in Steam SS")
                     #---------------------------------------------------Silica and Magnesium -------------------------------------------
                    try:
                        mgLimit = 0
                        if(analysis['pH'] >= 8.5):
                            mgLimit = 6000
                        elif(analysis['pH'] < 8.5 and analysis['pH'] > 7.5):
                            mgLimit = 12000
                        elif(analysis['pH'] <= 7.5):
                            mgLimit = 17000
                        
                        if(analysis['SilicaMagnesium'] < mgLimit):
                            magnesiumSilicaRes['Description'] = "Acceptable Magnesium Silicate Scaling"
                            magnesiumSilicaRes['Risk'] = "Acceptable"
                            magnesiumSilicaRes['Treatment'] = _data["Silica and Magnesium"]["acceptable"]
                        else:
                            magnesiumSilicaRes['Description'] = "Unacceptable Magnesium Silicate Scaling"
                            magnesiumSilicaRes['Risk'] = "Unacceptable"
                            magnesiumSilicaRes['Treatment'] = _data["Silica and Magnesium"]["unacceptable"]
                        magnesiumSilicaRes["Index"] = analysis['SilicaMagnesium']
                        Scaling["Magnesium Silicate Scale Formation"] = magnesiumSilicaRes
                    except Exception as e:
                        print(f'Error magnesium * silica SS : {e}')
                    #-------------------------------------------------------Calcium Sulphate------------------------------------------------
                    try:
                        calSulLimit = 10000000 if(analysis['WaterTreatment'] == True) else 50000
                        if(analysis["CalciumSulphate"] < calSulLimit):
                            calciumSulphateRes["Description"] = "Acceptable Calcium Sulphate Scaling"
                            calciumSulphateRes["Risk"] = "Acceptable"
                            calciumSulphateRes["Treatment"] = _data["Calcium Sulphate"]["acceptable"]
                        else:
                            calciumSulphateRes["Description"] = "Unacceptable Calcium Sulphate Scaling"
                            calciumSulphateRes["Risk"] = "Unacceptable"
                            calciumSulphateRes["Treatment"] = _data["Calcium Sulphate"]["unacceptable"]
                        calciumSulphateRes["Index"] = analysis["SilicaMagnesium"]
                        Scaling["Calcium Sulphate Scale Formation"] = calciumSulphateRes
                    except Exception as e:
                        print(f"Error Calcium Sulphate SS: {e}")   
                    #-----------------------------------------------------Phosphate Scaling------------------------------------------   
                    calciumPhosphateRes = {}
                    try:
                        if(analysis["CalciumPhosphate"] <= 0):
                            calciumPhosphateRes["Index"] = round(analysis["CalciumPhosphate"],2)
                            calciumPhosphateRes["Description"] = "Balance – Low potential for scale formation"
                            calciumPhosphateRes["Risk"] = "Ideal"
                            calciumPhosphateRes["Treatment"] = "No Treatment"
                        else:
                            calciumPhosphateRes["Index"] = round(analysis["CalciumPhosphate"],2)
                            calciumPhosphateRes["Description"] = "Potential of Scale Formation"
                            calciumPhosphateRes["Risk"] = "Tolerable"
                            calciumPhosphateRes["Treatment"] = "Treatment Recommended"
                        Scaling["Calcium phosphate scaling"] = calciumPhosphateRes
                   
                    except Exception as e:
                        print(f"Error Phosphate Assemnent Parse Table carbon: {e}") 
                    results["Scaling"] = Scaling
                elif(assessment == "Fouling"):
                    _data = self.assessment_carbon["fouling"] 
                    Fouling = {}
                    ssFoulRes = {}
                    if(analysis['Suspended Solids'] >= 30):
                        ssFoulRes["Description"] = "High Chance of Fouling"
                        ssFoulRes["Risk"] = "Unacceptable"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["unacceptable"]
                    elif(analysis['Suspended Solids'] < 30 and analysis['Suspended Solids'] >= 15):
                        ssFoulRes["Description"] = "Moderate Fouling"
                        ssFoulRes["Risk"] = "Tolerable"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["tolerable"]
                    elif(analysis['Suspended Solids'] < 15 and analysis['Suspended Solids'] >= 5):
                        ssFoulRes["Description"] = "Mild of Fouling"
                        ssFoulRes["Risk"] = "Acceptable"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["acceptable"]
                    else:
                        ssFoulRes["Description"] = "No Fouling predicted"
                        ssFoulRes["Risk"] = "Ideal"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["ideal"]
                    
                    ssFoulRes['Index'] = analysis["Suspended Solids"]
                    Fouling["Suspended Solids Fouling (mg/l)"] = ssFoulRes
                    results["Fouling"] = Fouling   
        elif(self.material == "Concrete"):
            for assessment in self.assessments:
                if(assessment == "Corrosion"):
                    _data = self.assessment_concrete["corrosion"] 
                    Corrosion = {}
                    RyznerRes = {}
                    AggressiveRes = {}
                    #------------------------------------------------------Corrosion Ryzner-------------------------------------
                    if(analysis['ryznar'] >= 8.5):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Severe Corrosion"
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["unacceptable"]
                    elif(analysis['ryznar'] < 8.5 and analysis['ryznar'] >= 7.8):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Mild Corrosion"
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["tolerable"]
                    elif(analysis['ryznar'] < 7.8 and analysis['ryznar'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Mild Corrosion"
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["acceptable"]
                    else:
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Balanced No Corrosion"
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["ideal"]
                    Corrosion["Ryznar Index"] = RyznerRes
                    #-------------------------------------------Langlier------------------------------------------------------------
                    langlierRes = {}
                    try:
                        if(analysis["Langlier"] >= 5):
                            langlierRes["Description"] = "Severe Corrosion due to CaCO\u2083"
                            langlierRes["Risk"] = "Unacceptable"
                            langlierRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                        elif(analysis["Langlier"] < 5 and analysis["Langlier"] >= 2):
                            langlierRes["Description"] = "Mild Corrosion due to CaCO\u2083"
                            langlierRes["Risk"] = "Tolerable"
                            langlierRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""

                        elif(analysis["Langlier"] < 2 and analysis["Langlier"] >= 0.5):
                            langlierRes["Description"] = "Mild Corrosion due to CaCO\u2083"
                            langlierRes["Risk"] = "Acceptable"
                            langlierRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                        else:
                            langlierRes["Description"] = "Minimal to no risk of corrosion"
                            langlierRes["Risk"] = "Ideal"
                            langlierRes["Treatment"] = "No Treatment"
                        langlierRes["Index"] = round(analysis["Langlier"],2)
                        Corrosion["Langelier Saturation Index"] = langlierRes
                    except Exception as e :
                        print(f"Error Lanlier: {e}")
                    #----------------------------------------------------------Corrosion Aggressive-------------------------------------
                    try:
                        if(analysis["Concrete Reinforced"]):
                            if(analysis["Aggressive"] >= 12):
                                AggressiveRes["Description"] = "Non aggressive, Lack of pitting corrosion of the concrete reinforced bars"
                                AggressiveRes["Risk"] = "Ideal"
                                AggressiveRes["Treatment"] = _data["Aggressive Index"]["ideal"]
                            elif(analysis["Aggressive"] < 12 and analysis["Aggressive"] >= 11):
                                AggressiveRes["Description"] = "Moderately aggressive, Moderate pitting corrosion of the concrete reinforced bars"
                                AggressiveRes["Risk"] = "Acceptable"
                                AggressiveRes["Treatment"] = _data["Aggressive Index"]["acceptable"]
                            elif(analysis["Aggressive"] < 11 and analysis["Aggressive"] >= 10):
                                AggressiveRes["Description"] = "Mildly aggressive, Mild pitting corrosion of the concrete reinforced bars"
                                AggressiveRes["Risk"] = "Ideal"
                                AggressiveRes["Treatment"] = _data["Aggressive Index"]["ideal"]
                            else:
                                AggressiveRes["Description"] = "Very aggressive, Severe pitting corrosion of the concrete reinforced bars"
                                AggressiveRes["Risk"] = "Unacceptable"
                                AggressiveRes["Treatment"] = _data["Aggressive Index"]["unacceptable"]
                            AggressiveRes["Index"] = round(analysis["Aggressive"],2)
                            Corrosion["Aggressive Index"] = AggressiveRes
                    except Exception as e:
                        print(f"Error Aggressive in Concrete: {e}")
                    
                    #-------------------------------End of Corrosion-------------------------------------------------------------------------------------------------------------------
                    results["Corrosion"] = Corrosion
                elif(assessment == "Scaling"):
                    _data = self.assessment_concrete["scaling"] 
                    Scaling = {}
                    RyznerRes = {}
                    sulphateAttackRez = {}

                    #--------------------------------------------------------------------Ryzner for scaling------------------------------------------
                    if(analysis['ryznar'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "No scale formation due to CaCO\u2083"
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["ideal"]
                    elif(analysis['ryznar'] < 6.8 and analysis['ryznar'] >= 6.2):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Moderate Scale Formation due to CaCO\u2083"
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["acceptable"]
                    elif(analysis['ryznar'] < 6.2 and analysis['ryznar'] >= 5.5):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Mild Scale Formation due to CaCO\u2083"
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["tolerable"]
                    else:
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Severe Scale Formation due to CaCO\u2083"
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["unacceptable"]
                    Scaling["Ryznar Index"] = RyznerRes
                    #Langlier-------------------------------------------------------------------------------------------------
                    langlierResScaling = {}
                    try:
                        if(analysis["Langlier"] > 3.5):
                            langlierResScaling["Description"] = "Severe Scale Formation due to CaCO\u2083"
                            langlierResScaling["Risk"] = "Unacceptable"
                            langlierResScaling["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""

                        elif(analysis["Langlier"] <= 3.5 and analysis["Langlier"] > 2):
                            langlierResScaling["Description"] = "Mild Scale Formation due to CaCO\u2083"
                            langlierResScaling["Risk"] = "Tolerable"
                            langlierResScaling["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""

                        elif(analysis["Langlier"] <= 2 and analysis["Langlier"] > 0):
                            langlierResScaling["Description"] = "Moderate Scale Formation due to CaCO\u2083"
                            langlierResScaling["Risk"] = "Acceptable"
                            langlierResScaling["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""
                        else:
                            langlierResScaling["Description"] = "No scale formation due to CaCO\u2083"
                            langlierResScaling["Risk"] = "Ideal"
                            langlierResScaling["Treatment"] = "No Treatment"
                        langlierResScaling["Index"] = round(analysis["Langlier"],2)
                        Scaling["Langelier Saturation Index"] = langlierResScaling
                    except Exception as e:
                        print("Error Langlier: {e}")
                    #-------------------------------------------------------------------Sulpahate attack Scaling--------------------------------------------
                    if(analysis['Sulphate'] >= 10000):
                        sulphateAttackRez["Description"] = "Very severe risk of sulphate attack"
                        sulphateAttackRez["Risk"] = "Unacceptable"
                        sulphateAttackRez["Treatment"] = _data['Sulphate Concentration']['unacceptable']
                    elif(analysis["Sulphate"] < 10000 and analysis["Sulphate"] >= 1500 ):
                        sulphateAttackRez["Description"] = "Severe risk of sulphate attack"
                        sulphateAttackRez["Risk"] = "Tolerable"
                        sulphateAttackRez["Treatment"] = _data['Sulphate Concentration']['tolerable']
                    elif(analysis["Sulphate"] < 1500 and analysis["Sulphate"] >= 150):
                        sulphateAttackRez["Description"] = "Moderate risk of sulphate attack"
                        sulphateAttackRez["Risk"] = "Acceptable"
                        sulphateAttackRez["Treatment"] = _data['Sulphate Concentration']['acceptable']
                    else:
                        sulphateAttackRez["Description"] = "Low risk of sulphate attack"
                        sulphateAttackRez["Risk"] = "Ideal"
                        sulphateAttackRez["Treatment"] = _data['Sulphate Concentration']['ideal'] 
                    sulphateAttackRez["Index"] = analysis["Sulphate"]
                    Scaling["Sulphate attack"] = sulphateAttackRez
                    #-----------------------------------------------------Phosphate Scaling------------------------------------------   
                    calciumPhosphateRes = {}
                    try:
                        if(analysis["CalciumPhosphate"] <= 0):
                            calciumPhosphateRes["Index"] = round(analysis["CalciumPhosphate"],2)
                            calciumPhosphateRes["Description"] = "Balance – Low potential for scale formation"
                            calciumPhosphateRes["Risk"] = "Ideal"
                            calciumPhosphateRes["Treatment"] = "No Treatment"
                        else:
                            calciumPhosphateRes["Index"] = round(analysis["CalciumPhosphate"],2)
                            calciumPhosphateRes["Description"] = "Potential of Scale Formation"
                            calciumPhosphateRes["Risk"] = "Tolerable"
                            calciumPhosphateRes["Treatment"] = "Treatment Recommended"
                        Scaling["Calcium phosphate scaling"] = calciumPhosphateRes
                   
                    except Exception as e:
                        print(f"Error Phosphate Assemnent Parse Table concrete: {e}")


                    results["Scaling"] = Scaling
                elif(assessment == "Fouling"):
                    _data = self.assessment_concrete["fouling"]
                    Fouling = {}
                    ssFoulRes = {}
                    if(analysis['Suspended Solids'] >= 30):
                        ssFoulRes["Description"] = "High Chance of Fouling"
                        ssFoulRes["Risk"] = "Unacceptable"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["unacceptable"]
                    elif(analysis['Suspended Solids'] < 30 and analysis['Suspended Solids'] >= 15):
                        ssFoulRes["Description"] = "Moderate Fouling"
                        ssFoulRes["Risk"] = "Tolerable"
                        ssFoulRes["Treatment"] =_data["suspended solids"]["tolerable"]
                    elif(analysis['Suspended Solids'] < 15 and analysis['Suspended Solids'] >= 5):
                        ssFoulRes["Description"] = "Mild of Fouling"
                        ssFoulRes["Risk"] = "Acceptable"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["acceptable"]
                    else:
                        ssFoulRes["Description"] = "No Fouling predicted"
                        ssFoulRes["Risk"] = "Ideal"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["ideal"]
                    
                    ssFoulRes['Index'] = analysis["Suspended Solids"]
                    Fouling["Suspended Solids Fouling (mg/l)"] = ssFoulRes
                    results["Fouling"] = Fouling
        elif(self.material == "Monel-Lead/Copper Alloys"):
            for assessment in self.assessments:
                if(assessment == "Corrosion"):
                    _data = self.assessment_alloy["corrosion"]
                    Corrosion = {}
                    RyznerRes = {}
                    LarsonRes = {}
                    AggressiveRes = {}
                    csmr = {}
                    prenRes = {}
                    #------------------------------------------------------Corrosion Ryzner-------------------------------------
                    if(analysis['ryznar'] >= 8.5):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Severe Corrosion due to lack of CaCO\u2083 formation "
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] =  _data["General Corrosion"]["unacceptable"]
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Mild Corrosion due to lack of CaCO\u2083 formation "
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] =_data["General Corrosion"]["tolerable"]
                    elif(analysis['ryznar'] < 7.8 and analysis['ryznar'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Mild Corrosion due to lack of CaCO\u2083 formation "
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["acceptable"]
                    else:
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Minimal to no corrosion"
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["ideal"]
                    Corrosion["Ryznar Index"] = RyznerRes
                    #-------------------------------------------Langlier------------------------------------------------------------
                    langlierRes = {}
                    try:
                        if(analysis["Langlier"] >= 5):
                            langlierRes["Description"] = "Severe Corrosion due to CaCO\u2083"
                            langlierRes["Risk"] = "Unacceptable"
                            langlierRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                        elif(analysis["Langlier"] < 5 and analysis["Langlier"] >= 2):
                            langlierRes["Description"] = "Mild Corrosion due to CaCO\u2083"
                            langlierRes["Risk"] = "Tolerable"
                            langlierRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""

                        elif(analysis["Langlier"] < 2 and analysis["Langlier"] >= 0.5):
                            langlierRes["Description"] = "Mild Corrosion due to CaCO\u2083"
                            langlierRes["Risk"] = "Acceptable"
                            langlierRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                        else:
                            langlierRes["Description"] = "Minimal to no risk of corrosion"
                            langlierRes["Risk"] = "Ideal"
                            langlierRes["Treatment"] = "No Treatment"
                        langlierRes["Index"] = round(analysis["Langlier"],2)
                        Corrosion["Langelier Saturation Index"] = langlierRes
                    except Exception as e :
                        print(f"Error Lanlier: {e}")
                    #--------------------------------------------------------Chloride to Sulphate MAss Ratio-----------------------------
                    try:
                        if(analysis["Lead or Copper"]):
                            if(analysis["csmr"] > 0.5):
                                csmr["Index"] = round(analysis["csmr"],2)
                                csmr["Description"] = "Significant corrosion risk and lead exposure"
                                csmr["Risk"] = "Unacceptable"
                                csmr['Treatment'] = _data["Chloride to sulphate"]["unacceptable"]
                            else:
                                csmr["Index"] = round(analysis["csmr"],2)
                                csmr["Description"] = "Minimal corrosion risk"
                                csmr["Risk"] = "Ideal"
                                csmr['Treatment'] = _data["Chloride to sulphate"]["ideal"]
                            Corrosion["Chloride to Sulphate Mass Ratio "] = csmr
                    except Exception as e:
                        print(f"Error CSMR :{e}")

                    #-----------------------------------------------------------Larson Alloys------------------------------------------------
                    if(analysis['larson'] >= 1.2):
                        LarsonRes["Description"] = "Severe corrosion"
                        LarsonRes["Risk"] = "Unacceptable"
                        LarsonRes["Treatment"] = _data["Pitting Corrosion"]["unacceptable"]
                    elif(analysis['larson'] < 1.2 and analysis['larson'] >= 1):
                        LarsonRes["Description"] = "Significant corrosion"
                        LarsonRes["Risk"] = "Tolerable"
                        LarsonRes["Treatment"] = _data["Pitting Corrosion"]["tolerable"]
                    elif(analysis['larson'] < 1 and analysis['larson'] >= 0.8):
                        LarsonRes["Description"] = "Mild corrosion"
                        LarsonRes["Risk"] = "Acceptable"
                        LarsonRes["Treatment"] = _data["Pitting Corrosion"]["acceptable"]
                    else:
                        LarsonRes["Description"] = "Non corrosive water"
                        LarsonRes["Risk"] = "Ideal"
                        LarsonRes["Treatment"] = _data["Pitting Corrosion"]["ideal"]
                    LarsonRes["Index"] = round(analysis["larson"],2)
                    Corrosion[' Larson-Skold Index'] = LarsonRes

                    #--------------------------------------------------------------Add PREN ALLOYS---------------------------------
                    try:
                        if(analysis['PREN'] <= 35):
                            prenRes["Description"] = "-"
                            prenRes["Risk"] = "Unacceptable"
                            prenRes["Treatment"] = _data["PREN"]["unacceptable"]
                        elif(analysis['PREN'] > 35 and analysis["PREN"] <= 40):
                            prenRes["Description"] = "Sea water resistance"
                            prenRes["Risk"] = "Acceptable"
                            prenRes["Treatment"] = _data["PREN"]["acceptable"]
                        elif(analysis["PREN"] > 40 and analysis["PREN"] <= 45):
                            prenRes["Description"] = "Sea water resistance with temperature >30°C"
                            prenRes["Risk"] = "Acceptable"
                            prenRes["Treatment"] = _data["PREN"]["acceptable"]
                        else:
                            prenRes["Description"] = "Crevice corrosion resistance"
                            prenRes["Risk"] = "Acceptable"
                            prenRes["Treatment"] = _data["PREN"]["acceptable"]
                        
                        prenRes["Index"] = round(analysis['PREN'],2)
                        Corrosion["PREN of Alloy"] = prenRes
                    except Exception as e:
                        print(f"Error PREN for Alloys: {e}")
                    #End Corosion-------------------------------------------------------------------------
                    results["Corrosion"] = Corrosion
                elif(assessment == "Scaling"):
                    _data = self.assessment_alloy["scaling"]
                    Scaling = {}
                    RyznerRes = {}
                    silicaSteamRes = {}
                    magnesiumSilicaRes = {}
                    calciumSulphateRes = {}


                    #------------------------------------------------------Ryzner for Scaling---------------------------
                    if(analysis['ryznar'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "No scale formation due to CaCO\u2083"
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = _data['General Corrosion']["ideal"]
                    elif(analysis['ryznar'] < 6.8 and analysis['ryznar'] >= 6.2):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Moderate Scale Formation due to CaCO\u2083"
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = _data['General Corrosion']["acceptable"]
                    elif(analysis['ryznar'] < 6.2 and analysis['ryznar'] >= 5.5):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Mild Scale Formation due to CaCO\u2083"
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] = _data['General Corrosion']["tolerable"]
                    else:
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Severe Scale Formation due to CaCO\u2083"
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] = _data['General Corrosion']["unacceptable"]
                    Scaling["Ryznar Index"] = RyznerRes
                    #Langlier-------------------------------------------------------------------------------------------------
                    langlierResScaling = {}
                    try:
                        if(analysis["Langlier"] > 3.5):
                            langlierResScaling["Description"] = "Severe Scale Formation due to CaCO\u2083"
                            langlierResScaling["Risk"] = "Unacceptable"
                            langlierResScaling["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""

                        elif(analysis["Langlier"] <= 3.5 and analysis["Langlier"] > 2):
                            langlierResScaling["Description"] = "Mild Scale Formation due to CaCO\u2083"
                            langlierResScaling["Risk"] = "Tolerable"
                            langlierResScaling["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""

                        elif(analysis["Langlier"] <= 2 and analysis["Langlier"] > 0):
                            langlierResScaling["Description"] = "Moderate Scale Formation due to CaCO\u2083"
                            langlierResScaling["Risk"] = "Acceptable"
                            langlierResScaling["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""
                        else:
                            langlierResScaling["Description"] = "No scale formation due to CaCO\u2083"
                            langlierResScaling["Risk"] = "Ideal"
                            langlierResScaling["Treatment"] = "No Treatment"
                        langlierResScaling["Index"] = round(analysis["Langlier"],2)
                        Scaling["Langelier Saturation Index"] = langlierResScaling
                    except Exception as e:
                        print("Error Langlier: {e}")
                    #-----------------------------------------------------Silica Concentration in Steam-----------------------
                    try:
                        if(analysis["Silica Concentration in steam"] <= 0.02):
                            silicaSteamRes["Index"] = round(analysis["Silica Concentration in steam"],2)
                            silicaSteamRes["Description"] = "Minimal silica film formation"
                            silicaSteamRes["Risk"] = "Ideal"
                            silicaSteamRes["Treatment"] = _data["Silica Concentration in steam"]["ideal"]
                        else:
                            silicaSteamRes["Index"] = round(analysis["Silica Concentration in steam"],2)
                            silicaSteamRes["Description"] = "High silica film formation"
                            silicaSteamRes["Risk"] = "Tolerable"
                            silicaSteamRes["Treatment"] =  _data["Silica Concentration in steam"]["tolerable"]
                        Scaling["Scaling due to Silica in Steam"] = silicaSteamRes
                   
                    except Exception as e:
                        print(f"Error Silica in Steam SS")
                     #---------------------------------------------------Silica and Magnesium -------------------------------------------
                    try:
                        mgLimit = 0
                        if(analysis['pH'] >= 8.5):
                            mgLimit = 6000
                        elif(analysis['pH'] < 8.5 and analysis['pH'] > 7.5):
                            mgLimit = 12000
                        elif(analysis['pH'] <= 7.5):
                            mgLimit = 17000
                        
                        if(analysis['SilicaMagnesium'] < mgLimit):
                            magnesiumSilicaRes['Description'] = "Acceptable Magnesium Silicate Scaling"
                            magnesiumSilicaRes['Risk'] = "Acceptable"
                            magnesiumSilicaRes['Treatment'] = _data["Silica and Magnesium"]["acceptable"]
                        else:
                            magnesiumSilicaRes['Description'] = "Unacceptable Magnesium Silicate Scaling"
                            magnesiumSilicaRes['Risk'] = "Unacceptable"
                            magnesiumSilicaRes['Treatment'] = _data["Silica and Magnesium"]["unacceptable"]
                        magnesiumSilicaRes["Index"] = analysis['SilicaMagnesium']
                        Scaling["Magnesium Silicate Scale Formation"] = magnesiumSilicaRes
                    except Exception as e:
                        print(f'Error magnesium * silica SS : {e}')
                    #-------------------------------------------------------Calcium Sulphate------------------------------------------------
                    try:
                        calSulLimit = 10000000 if(analysis['WaterTreatment'] == True) else 50000
                        
                        if(analysis["CalciumSulphate"] < calSulLimit):
                            calciumSulphateRes["Description"] = "Acceptable Calcium Sulphate Scaling"
                            calciumSulphateRes["Risk"] = "Acceptable"
                            calciumSulphateRes["Treatment"] = _data["Calcium Sulphate"]["acceptable"]
                        else:
                            calciumSulphateRes["Description"] = "Unacceptable Calcium Sulphate Scaling"
                            calciumSulphateRes["Risk"] = "Unacceptable"
                            calciumSulphateRes["Treatment"] = _data["Calcium Sulphate"]["unacceptable"]
                        calciumSulphateRes["Index"] = analysis["SilicaMagnesium"]
                        Scaling["Calcium Sulphate Scale Formation"] = calciumSulphateRes
                    except Exception as e:
                        print(f"Error Calcium Sulphate SS: {e}") 
                    #-----------------------------------------------------Phosphate Scaling------------------------------------------   
                    calciumPhosphateRes = {}
                    try:
                        if(analysis["CalciumPhosphate"] <= 0):
                            calciumPhosphateRes["Index"] = round(analysis["CalciumPhosphate"],2)
                            calciumPhosphateRes["Description"] = "Balance – Low potential for scale formation"
                            calciumPhosphateRes["Risk"] = "Ideal"
                            calciumPhosphateRes["Treatment"] = "No Treatment"
                        else:
                            calciumPhosphateRes["Index"] = round(analysis["CalciumPhosphate"],2)
                            calciumPhosphateRes["Description"] = "Potential of Scale Formation"
                            calciumPhosphateRes["Risk"] = "Tolerable"
                            calciumPhosphateRes["Treatment"] = "Treatment Recommended"
                        Scaling["Calcium phosphate scaling"] = calciumPhosphateRes
                   
                    except Exception as e:
                        print(f"Error Phosphate Assemnent Parse Table monel: {e}")
                       
                    results["Scaling"] = Scaling
                elif(assessment == "Fouling"):
                    _data = self.assessment_alloy["fouling"]
                    Fouling = {}
                    ssFoulRes = {}
                    if(analysis['Suspended Solids'] >= 30):
                        ssFoulRes["Description"] = "High Chance of Fouling"
                        ssFoulRes["Risk"] = "Unacceptable"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["unacceptable"]
                    elif(analysis['Suspended Solids'] < 30 and analysis['Suspended Solids'] >= 15):
                        ssFoulRes["Description"] = "Moderate Fouling"
                        ssFoulRes["Risk"] = "Tolerable"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["tolerable"]
                    elif(analysis['Suspended Solids'] < 15 and analysis['Suspended Solids'] >= 5):
                        ssFoulRes["Description"] = "Mild of Fouling"
                        ssFoulRes["Risk"] = "Acceptable"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["acceptable"]
                    else:
                        ssFoulRes["Description"] = "No Fouling predicted"
                        ssFoulRes["Risk"] = "Ideal"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["ideal"]
                    
                    ssFoulRes['Index'] = analysis["Suspended Solids"]
                    Fouling["Suspended Solids Fouling (mg/l)"] = ssFoulRes
                    results["Fouling"] = Fouling   
        elif(self.material == "Plastic"):
            for assessment in self.assessments:
                if(assessment == "Scaling"):
                    _data = self.assessment_plastic["scaling"]
                    Scaling = {}
                    RyznerRes = {}
                    #------------------------------------------------------Ryzner for Scaling---------------------------
                    if(analysis['ryznar'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Minimal to no corrosion"
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["ideal"]
                    elif(analysis['ryznar'] < 6.8 and analysis['ryznar'] >= 6.2):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Mild Corrosion due to lack of CaCO\u2083 formation "
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = _data["General Corrosion"]["acceptable"]
                    elif(analysis['ryznar'] < 6.2 and analysis['ryznar'] >= 5.5):
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Mild Corrosion due to lack of CaCO\u2083 formation "
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] =_data["General Corrosion"]["tolerable"]
                    else:
                        RyznerRes["Index"] = round(analysis['ryznar'], 2)
                        RyznerRes["Description"] = "Severe Corrosion due to lack of CaCO\u2083 formation "
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] =_data["General Corrosion"]["unacceptable"]
                    Scaling["Ryznar Index"] = RyznerRes
                    
                    #-----------------------------------------------------Phosphate Scaling------------------------------------------   
                    calciumPhosphateRes = {}
                    try:
                        if(analysis["CalciumPhosphate"] <= 0):
                            calciumPhosphateRes["Index"] = round(analysis["CalciumPhosphate"],2)
                            calciumPhosphateRes["Description"] = "Balance – Low potential for scale formation"
                            calciumPhosphateRes["Risk"] = "Ideal"
                            calciumPhosphateRes["Treatment"] = "No Treatment"
                        else:
                            calciumPhosphateRes["Index"] = round(analysis["CalciumPhosphate"],2)
                            calciumPhosphateRes["Description"] = "Potential of Scale Formation"
                            calciumPhosphateRes["Risk"] = "Tolerable"
                            calciumPhosphateRes["Treatment"] = "Treatment Recommended"
                        Scaling["Calcium phosphate scaling"] = calciumPhosphateRes
                   
                    except Exception as e:
                        print(f"Error Phosphate Assemnent Parse Table Plastic: {e}")
                    results["Scaling"] = Scaling
                elif(assessment == "Fouling"):
                    _data = self.assessment_plastic["fouling"]
                    Fouling = {}
                    ssFoulRes = {}
                    if(analysis['Suspended Solids'] >= 30):
                        ssFoulRes["Description"] = "High Chance of Fouling"
                        ssFoulRes["Risk"] = "Unacceptable"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["unacceptable"]
                    elif(analysis['Suspended Solids'] < 30 and analysis['Suspended Solids'] >= 15):
                        ssFoulRes["Description"] = "Moderate Fouling"
                        ssFoulRes["Risk"] = "Tolerable"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["tolerable"]
                    elif(analysis['Suspended Solids'] < 15 and analysis['Suspended Solids'] >= 5):
                        ssFoulRes["Description"] = "Mild of Fouling"
                        ssFoulRes["Risk"] = "Acceptable"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["acceptable"]
                    else:
                        ssFoulRes["Description"] = "No Fouling predicted"
                        ssFoulRes["Risk"] = "Ideal"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["ideal"]
                    
                    ssFoulRes['Index'] = analysis["Suspended Solids"]
                    Fouling["Suspended Solids Fouling (mg/l)"] = ssFoulRes
                    results["Fouling"] = Fouling 
        elif(self.material == "Membranes"):
            for assessment in self.assessments:
                if(assessment == "Corrosion"):
                    _data = self.assessment_membrane["corrosion"]
                    Corrosion = {}
                    langlierRes = {}
                    if(analysis["Langlier"] >= 5):
                        langlierRes["Description"] = "Severe Corrosion due to CaCO\u2083"
                        langlierRes["Risk"] = "Unacceptable"
                        langlierRes["Treatment"] = _data["Langlier"]["unacceptable"]
                    elif(analysis["Langlier"] < 5 and analysis["Langlier"] >= 2):
                        langlierRes["Description"] = "Mild Corrosion due to CaCO\u2083"
                        langlierRes["Risk"] = "Tolerable"
                        langlierRes["Treatment"] = _data["Langlier"]["tolerable"]

                    elif(analysis["Langlier"] < 2 and analysis["Langlier"] >= 0.5):
                        langlierRes["Description"] = "Mild Corrosion due to CaCO\u2083"
                        langlierRes["Risk"] = "Acceptable"
                        langlierRes["Treatment"] = _data["Langlier"]["acceptable"]
                    else:
                        langlierRes["Description"] = "Minimal to no risk of corrosion"
                        langlierRes["Risk"] = "Ideal"
                        langlierRes["Treatment"] = _data["Langlier"]["ideal"]
                    langlierRes["Index"] = round(analysis["Langlier"],2)
                    Corrosion["Langelier Saturation Index"] = langlierRes
                    results["Corrosion"] = Corrosion
                elif(assessment == "Scaling"):
                    _data = self.assessment_membrane["scaling"]
                    Scaling = {}
                    langlierResScaling = {}
                    if(analysis["Langlier"] > 3.5):
                        langlierResScaling["Description"] = "Severe Scale Formation due to CaCO\u2083"
                        langlierResScaling["Risk"] = "Unacceptable"
                        langlierResScaling["Treatment"] = _data["Langlier"]["unacceptable"]

                    elif(analysis["Langlier"] <= 3.5 and analysis["Langlier"] > 2):
                        langlierResScaling["Description"] = "Mild Scale Formation due to CaCO\u2083"
                        langlierResScaling["Risk"] = "Tolerable"
                        langlierResScaling["Treatment"] = _data["Langlier"]["tolerable"]

                    elif(analysis["Langlier"] <= 2 and analysis["Langlier"] > 0):
                        langlierResScaling["Description"] = "Moderate Scale Formation due to CaCO\u2083"
                        langlierResScaling["Risk"] = "Acceptable"
                        langlierResScaling["Treatment"] = _data["Langlier"]["acceptable"]
                    else:
                        langlierResScaling["Description"] = "No scale formation due to CaCO\u2083"
                        langlierResScaling["Risk"] = "Ideal"
                        langlierResScaling["Treatment"] = _data["Langlier"]["ideal"]
                    langlierResScaling["Index"] = round(analysis["Langlier"],2)
                    Scaling["Langelier Saturation Index"] = langlierResScaling
                    
                    #-----------------------------------------------------Phosphate Scaling------------------------------------------   
                    calciumPhosphateRes = {}
                    try:
                        if(analysis["CalciumPhosphate"] <= 0):
                            calciumPhosphateRes["Index"] = round(analysis["CalciumPhosphate"],2)
                            calciumPhosphateRes["Description"] = "Balance – Low potential for scale formation"
                            calciumPhosphateRes["Risk"] = "Ideal"
                            calciumPhosphateRes["Treatment"] = "No Treatment"
                        else:
                            calciumPhosphateRes["Index"] = round(analysis["CalciumPhosphate"],2)
                            calciumPhosphateRes["Description"] = "Potential of Scale Formation"
                            calciumPhosphateRes["Risk"] = "Tolerable"
                            calciumPhosphateRes["Treatment"] = "Treatment Recommended"
                        Scaling["Calcium phosphate scaling"] = calciumPhosphateRes
                   
                    except Exception as e:
                        print(f"Error Phosphate Assemnent Parse Table membrane: {e}")
                    results["Scaling"] = Scaling
                elif(assessment == "Fouling"):
                    _data = self.assessment_membrane["fouling"]
                    Fouling = {}
                    ssFoulRes = {}
                    psRes = {}
                    sdensityRes = {}
                    if(analysis['Suspended Solids'] >= 30):
                        ssFoulRes["Description"] = "High Chance of Fouling"
                        ssFoulRes["Risk"] = "Unacceptable"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["unacceptable"]
                    elif(analysis['Suspended Solids'] < 30 and analysis['Suspended Solids'] >= 15):
                        ssFoulRes["Description"] = "Moderate Fouling"
                        ssFoulRes["Risk"] = "Tolerable"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["tolerable"]
                    elif(analysis['Suspended Solids'] < 15 and analysis['Suspended Solids'] >= 5):
                        ssFoulRes["Description"] = "Mild of Fouling"
                        ssFoulRes["Risk"] = "Acceptable"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["acceptable"]
                    else:
                        ssFoulRes["Description"] = "No Fouling predicted"
                        ssFoulRes["Risk"] = "Ideal"
                        ssFoulRes["Treatment"] = _data["suspended solids"]["ideal"]
                    ssFoulRes['Index'] = analysis["Suspended Solids"]

                    #--------------------------------------------------------------------------Fouling Silt Density----------------------
                    try:
                        if(analysis["Silt Density Index"] >= 5):
                            psRes["Description"] = "Several years without collodial fouling"
                            psRes['Risk'] = "Ideal"
                            psRes["Treatment"] = _data["silt index"]["ideal"]
                        if(analysis["Silt Density Index"] < 5 and analysis["Silt Density Index"] >= 3):
                            psRes["Description"] = "Several months between cleaning"
                            psRes['Risk'] = "Acceptable"
                            psRes["Treatment"] = _data["silt index"]["acceptable"]
                        elif(analysis["Silt Density Index"] > 3 and analysis["Silt Density Index"] <= 1):
                            psRes["Description"] = "Particular fouling likely a problem, frequent cleaning"
                            psRes['Risk'] = "Tolerable"
                            psRes["Treatment"] = _data["silt index"]["tolerable"]
                        else:
                            psRes["Description"] = "Unacceptable, additional pre-treatment is needed"
                            psRes['Risk'] = "Unacceptable"
                            psRes["Treatment"] = _data["silt index"]["unacceptable"]
                        psRes["Index"] = round(analysis["Silt Density Index"],2)
                        Fouling["Silt Density Index"] = psRes
                    except Exception as e:
                        print(f"Error Fouling Silt Density :{e}")
                    #-----------------------------------------------------------------------------Particle Size-----------------------------
                    try:
                        analysisLimit = 0
                        if(analysis['Technology Type'] == 0): #Grit Removal
                            analysisLimit = 1000
                            description = "Treatment Recommended - Consider use of microfiltration"

                        elif(analysis["Technology Type"] == 1): #Microfiltration
                            analysisLimit = 0.1
                            description = "Treatment Recommended, This technology is recommended for suspended solids and large colloids"
                        elif(analysis["Technology Type"] == 2): #Ultrafiltration
                            analysisLimit = 0.1                            
                            description = "Treatment Recommended, This technology is recommened for Proteins and large organics"
                        elif(analysis["Technology Type"] == 3): #Nanofiltration
                            analysisLimit = 0.001
                            description = "Treatment Recommended, This technology is recommended for Organics and dissolved solids"
                        elif(analysis["Technology Type"] == 4): #Reverse Osmosis
                            analysisLimit = 0.001
                            description = "Treatment Recommended, This technology is recommended for Dissolved salts and organics"

                        if(analysis["Particle Size"] > analysisLimit): 
                            sdensityRes["Treatment"] = description
                            sdensityRes["Risk"] = "Unacceptable"
                        else:
                            sdensityRes["Treatment"] = "No Treatment"
                            sdensityRes["Risk"] = "Acceptable"
                        
                        Fouling["Particle Size (µm)"] = sdensityRes
                        sdensityRes["Description"] = "-"
                        sdensityRes['Index'] = analysis["Particle Size"]
                        
                    except Exception as e:
                        print(f"Error Paricle Size ;{e}")
                    Fouling["Suspended Solids Fouling (mg/l)"] = ssFoulRes
                    results["Fouling"] = Fouling      
        
        return results  
