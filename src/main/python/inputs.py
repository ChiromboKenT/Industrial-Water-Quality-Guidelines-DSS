
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import uic
from calculations import Analyze

class InputsWindow(QDialog, qtw.QWidget):
    statusBarSignal = qtc.pyqtSignal(str,str)
    reportsSignal = qtc.pyqtSignal(dict,str,list,dict,dict,dict)
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.ctx = args[0]
        uic.loadUi(self.ctx.get_inputs,self)
        
        
        
        #print(args[0])
        # Opening JSON file
        self.units_data = self.ctx.import_units_data
        self.parameters_list = self.ctx.import_param_data()

        
        #Buttons
        self.buttonLoadDefaults.clicked.connect(self.loadDefaults)
        #self.buttonBack.clicked.connect(self.showBack)
        self.buttonSaveDefaults.clicked.connect(self.saveDefaults)
        #self.buttonNext.clicked.connect(self.Validate)
        self.buttonDeleteDefaults.clicked.connect(self.deleteParams)
        self.buttonDeleteDefaults.setEnabled(False)
        #self.buttonAbout.clicked.connect(self.showAbout)

        self.buttonSaveDefaults.setStyleSheet(
            """
                QPushButton{
                    background-color: rgb(12, 75, 85);color: rgb(255, 255, 255);border: 1px solid rgb(12, 75, 85); padding: 5px 20px; border-radius:8px
                }                   
                QPushButton:hover{
                    background-color: #127281;color: rgb(255, 255, 255);border: 1px solid rgb(12, 75, 85); padding: 5px 20px; border-radius:8px
                }
            """
        )
        #List Widget
        for item in self.parameters_list.keys():
            self.listDefaults.addItem(f'{item}')
        self.listDefaults.currentRowChanged.connect(self.rowChange)

        #Labels
        typeText = ", ".join(args[1]['type'])
        self.inputType.setText(typeText)
        self.inputSector.setText(args[1]['sector'])
        self.inputUnit.setText(args[1]['unit'])
        self.inputMaterial.setText(args[1]['material'])

        if(args[1]['material'] == "Membranes"):
            self.inputMaterial.hide()
            self.materialOfConstructionLabel.setText("")

        #Inputs
        self.parameter_inputs = args[1]['inputs']
        self.material = args[1]["material"]
        self.assesments = args[1]['type']
        self.user = args[1]['user']
        self.sector = args[1]['sector']
        self.unit = args[1]['unit']
        
        #Load Error
        self.errors = {}
        for item_key in self.parameter_inputs:
            self.errors[item_key] = "Not Entered"
        
        inputsSize = len(self.parameter_inputs)
        if(inputsSize %2 == 0):
            inputListLeft  =  self.parameter_inputs[0:int(inputsSize/2)]
            inputListRight = self.parameter_inputs[int(inputsSize/2):]
        else:
            inputListLeft = self.parameter_inputs[0:int((inputsSize+1)/2)]
            inputListRight = self.parameter_inputs[int((inputsSize+1)/2):]
        try:
            #Left Column Inputs-----------------------------------------------------------------------------
            for i,input in enumerate(inputListLeft):
                label = qtw.QLabel(str(input)+":")
                label.setStyleSheet("color:rgb(48,48,48);font-size:12px")
                unit_box = qtw.QComboBox()
                
                if(self.units_data[input]['input_type'] == "number"):
                    if(self.units_data[input]['decimals'] == 0):
                        spin_input = qtw.QSpinBox()
                        spin_input.setRange(self.units_data[input]['rangeLow'],self.units_data[input]['rangeHigh'])
                        spin_input.setSingleStep(1)
                        
                    else:
                        spin_input = qtw.QDoubleSpinBox()
                        spin_input.setRange(self.units_data[input]['rangeLow'],self.units_data[input]['rangeHigh'])
                        spin_input.setSingleStep(0.1)
                        try:
                            spin_input.setDecimals(self.units_data[input]['decimals'])
                        except Exception as e:
                            spin_input.setDecimals(1)
                            print(f'Decimal error: {e}')
                    spin_input.clear()
                    spin_input.setButtonSymbols(qtw.QAbstractSpinBox.NoButtons)
                    spin_input.setLocale(qtc.QLocale())
                    spin_input.valueChanged.connect(self.valueChanged)
                    
                    spin_input.setMaximumWidth(80)
                    spin_input.setMinimumWidth(70)
                elif(self.units_data[input]['input_type'] == "list"):
                    spin_input = qtw.QComboBox()
                    spin_input.addItems(self.units_data[input]['options'])
                else:
                    spin_input = qtw.QCheckBox()
                    spin_input.setText("Tick,if yes")
                    spin_input.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))
                                   

                
                spin_input.setObjectName(f'{self.units_data[input]["label"]}')
                spin_input.setStyleSheet("color:rgb(48,48,48);")
                
                if(self.units_data[input]['unit'] == "n/a"):
                    unit_box = qtw.QLabel()
                    unit_box.setEnabled(False)
                    unit_box.setText(self.units_data[input]['unit'])
                    unit_box.setMinimumWidth(60)
                    unit_box.setStyleSheet("font-size:11px;border:none;color:rgb(48,48,48);")
                elif(len(self.units_data[input]['unit']) <= 1):
                    unit_box = qtw.QLabel()
                    unit_box.setEnabled(False)
                    unit_box.setText(self.units_data[input]['unit'][0])
                    unit_box.setMinimumWidth(70)
                    unit_box.setStyleSheet("font-size:11px;border:none;color:rgb(48,48,48);")
                else:
                    unit_box = qtw.QComboBox()
                    unit_box.setEnabled(False)
                    unit_box.addItems(self.units_data[input]['unit'])
                    unit_box.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))

                verticalSpacer = qtw.QSpacerItem(5, 5, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)
                self.gridInputsLeft.setSpacing(8)
                self.gridInputsLeft.addWidget(label,i +1,0,alignment=qtc.Qt.AlignTop)
                if(self.units_data[input]['input_type'] == "number"):
                    self.gridInputsLeft.addWidget(spin_input,i +1,1,alignment=qtc.Qt.AlignTop)
                    self.gridInputsLeft.addWidget(unit_box, i+1,2,alignment=qtc.Qt.AlignTop)
                elif(self.units_data[input]['input_type'] == "list"):
                    self.gridInputsLeft.addWidget(spin_input,i +1,1,1,2,alignment=qtc.Qt.AlignTop)
                else:
                    self.gridInputsLeft.addWidget(spin_input,i +1,1,alignment=qtc.Qt.AlignTop)
                self.gridInputsLeft.addItem(verticalSpacer)

            #Right Hand Inputs----------------------------------------------------------------------------
            for i,input in enumerate(inputListRight):
                label = qtw.QLabel(str(input)+":")
                label.setStyleSheet("color:rgb(48,48,48);font-size:12px")
                unit_box = qtw.QComboBox()
                
                if(self.units_data[input]['input_type'] == "number"):
                    if(self.units_data[input]['decimals'] == 0):
                        spin_input = qtw.QSpinBox()
                        spin_input.setRange(self.units_data[input]['rangeLow'],self.units_data[input]['rangeHigh'])
                        spin_input.setSingleStep(1)
                        
                    else:
                        spin_input = qtw.QDoubleSpinBox()
                        spin_input.setRange(self.units_data[input]['rangeLow'],self.units_data[input]['rangeHigh'])
                        spin_input.setSingleStep(0.1)
                        try:
                            spin_input.setDecimals(self.units_data[input]['decimals'])
                        except Exception as e:
                            spin_input.setDecimals(1)
                            print(f'Decimal error: {e}')
                    spin_input.clear()
                    spin_input.setButtonSymbols(qtw.QAbstractSpinBox.NoButtons)
                    spin_input.setLocale(qtc.QLocale())
                    spin_input.valueChanged.connect(self.valueChanged)
                    spin_input.setMaximumWidth(80)
                    spin_input.setMinimumWidth(70)
                elif(self.units_data[input]['input_type'] == "list"):
                    spin_input = qtw.QComboBox()
                    spin_input.addItems(self.units_data[input]['options'])
                    spin_input.setMaximumWidth(180)
                else:
                    spin_input = qtw.QCheckBox()
                    spin_input.setText("Tick,if yes")
                    spin_input.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))

                spin_input.setObjectName(f'{self.units_data[input]["label"]}')
                spin_input.setStyleSheet("color:rgb(48,48,48);")
                if(self.units_data[input]['unit'] == "n/a"):
                    unit_box = qtw.QLabel()
                    unit_box.setText(self.units_data[input]['unit'])
                    unit_box.setStyleSheet("font-size:11px;border:none;color:rgb(48,48,48);")
                elif(len(self.units_data[input]['unit']) <= 1):
                    unit_box = qtw.QLabel()
                    unit_box.setText(self.units_data[input]['unit'][0])
                    unit_box.setMinimumWidth(70)
                    unit_box.setStyleSheet("font-size:11px;border:none;color:rgb(48,48,48);")
                else:
                    unit_box = qtw.QComboBox()
                    #unit_box.setEnabled(False)
                    unit_box.addItems(self.units_data[input]['unit'])
                    unit_box.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))
                
                verticalSpacer = qtw.QSpacerItem(10, 10, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
                self.gridInputsRight.setSpacing(8)
                self.gridInputsRight.addWidget(label,i +1,0,alignment=qtc.Qt.AlignTop)
                if(self.units_data[input]["input_type"] == "number"): 
                    self.gridInputsRight.addWidget(spin_input,i +1,1,alignment=qtc.Qt.AlignTop)
                    self.gridInputsRight.addWidget(unit_box, i+1,2,alignment=qtc.Qt.AlignTop)
                elif(self.units_data[input]['input_type'] == "list"):
                    self.gridInputsRight.addWidget(spin_input,i +1,1,1,2,alignment=qtc.Qt.AlignTop)
                else:
                    self.gridInputsRight.addWidget(spin_input,i +1,1,alignment=qtc.Qt.AlignTop)
                self.gridInputsRight.addItem(verticalSpacer)
        except Exception as e:
            print(f'Error inputting into grid: {e}')    
   
    def showNext(self,analysis,material,assesments,inputs):
        info = {
            "sector" : self.sector,
            "unit": self.unit
        }
        user = self.user
        self.reportsSignal.emit(analysis,material,assesments,inputs,user,info)
        

        self.close()
    def emitStatusBar(self,color, message):
        self.statusBarSignal.emit(
            color,
            message
        )
        
    def showBack(self):
        self.ui_sector = self.ctx.sector_window
        self.ui_sector.show()
        self.close()
    def loadDefaults(self):
        try:
            loadText = self.listDefaults.currentItem().text()
        except Exception as e:
            self.emitStatusBar("red",str(f'Please select a water type from the list to load values.'))
        increment = 0
        if(len(loadText) >= 1):
            listItem = self.listDefaults.findItems(loadText, qtc.Qt.MatchExactly)
            if(len(listItem) == 1):
                for param_key, param_value in self.parameters_list[loadText].items():
                    inputToChange = self.findChild(qtw.QSpinBox, param_key) or self.findChild(qtw.QDoubleSpinBox, param_key)
                    if(inputToChange):
                        increment = increment + 1
                        inputToChange.setValue(param_value)
                        self.emitStatusBar("green",str(f'Loaded default values for {loadText} successfully!'))
                        
            if(increment == 0):
                self.emitStatusBar("red",str(f'No defaults for these parameters found'))
    def showAbout(self):
        self.about_window = self.ctx.about_window
        self.about_window.show()
    def saveDefaults(self):
        saveText = self.defaultsSaveInput.text()
        
        if (len(saveText) >= 1):
            if(len(self.listDefaults.findItems(saveText, qtc.Qt.MatchExactly)) == 1 ):
                if(self.parameters_list[saveText]['isEditable']):
                    self.storeParams(saveText)
                else:
                    self.emitStatusBar("red",str(f'The values for {saveText} are not editable. Please specify a different save name and try again'))
            else:
                try:
                    self.storeParams(saveText)
                    self.listDefaults.addItem(saveText)
                except Exception as e:
                    print(f'Error Add item to Defaults List: {e}')
                    self.emitStatusBar("red",str(f'Error! Could not save the parameters'))
        else :
            self.emitStatusBar("red",str(f'No save filename specified'))

    def storeParams(self,text):
        params = {
            "input_calcium" :0 ,
            "input_magnesium" :0 ,
            "input_sulphate" : 0,
            "input_chloride" :0,
            "input_flouride" :0,
            "input_alkalinity": 0,
            "input_temperature": 0,
            "input_ph": 0,
            "input_tds": 0,
            "input_ec": 0,
            "input_palkalinity":0,
            "input_silica_concentration":0,
            "input_silica":0,
            "input_suspended":0,
            "input_oxygen":0,
            "input_days":0,
            "input_silt":0,
            "input_particle":0,
            "isEditable" : True
        }
        store_data = {}
        for row in range(1, self.gridInputsRight.rowCount()):
            itemInRow = self.gridInputsRight.itemAtPosition(row,1)
            if(itemInRow != None):
                objName = itemInRow.widget().objectName()
                if params.get(objName)!= None:
                    params[objName] = itemInRow.widget().value()
        for row in range(1, self.gridInputsLeft.rowCount()):
            itemInRow = self.gridInputsLeft.itemAtPosition(row,1)
            if(itemInRow != None):
                objName = itemInRow.widget().objectName()
                if params.get(objName)!= None:
                    params[objName] = itemInRow.widget().value()
        store_data[text] = params
        self.ctx.write_json(store_data)
        self.emitStatusBar("green",str(f'Successfully Saved default parameters for {text}'))
        self.parameters_list = self.ctx.import_param_data()       
    def deleteParams(self):

        deleteValue = self.listDefaults.currentRow()
        deleteKey  = self.listDefaults.currentItem().text()

        try:
            deletedItem = self.listDefaults.takeItem(deleteValue)
            self.listDefaults.setCurrentRow(0)
            data = self.parameters_list
            del data[deleteKey]

            print(data)
            self.ctx.delete_json(data)
            self.emitStatusBar("green",str(f'Successfully removed {deletedItem.text()} defaults'))
            self.parameters_list = self.ctx.import_param_data()
        except Exception as e:
            print(f"Delete Error: {e}")
    def rowChange(self):
        rowText = self.listDefaults.currentItem().text()
        self.defaultsSaveInput.setText(rowText)
        self.buttonDeleteDefaults.setEnabled(False)

        try:
            if(self.parameters_list[rowText]["isEditable"] == True):
                self.buttonDeleteDefaults.setEnabled(True)
        except Exception as e:
            print(f"Delete Param Error: {e}")
    def calculate(self):
        inputs = {}
        for input_key,input_item in self.units_data.items():
           
            inputWidget = (self.findChild(qtw.QSpinBox, input_item["label"]) or self.findChild(qtw.QDoubleSpinBox, input_item["label"]) 
                    or self.findChild(qtw.QCheckBox, input_item["label"]) or self.findChild(qtw.QComboBox, input_item["label"])
                    )
            if(inputWidget):
                try:
                    value = inputWidget.value() 
                    
                except AttributeError as e:
                    try:
                        value = inputWidget.isChecked()
                    except AttributeError as e:
                        value = inputWidget.currentIndex()
                inputs[input_key] = value
                #print("{}:{}".format(input_key,value))
        
        analysis = (Analyze(self.material,self.assesments,inputs))
        self.showNext(analysis,self.material,self.assesments,inputs)
    def valueChanged(self):
        sender = self.sender()
        for field_key, field_item in self.units_data.items():
            if(field_item['label'] == sender.objectName()):
                if(sender.value() == 0):
                    self.errors[field_key] = "Not Entered"
                else:
                    self.errors[field_key] = ""    
    def Validate(self):
        errorSheet = {
            "Required" : [],
            "Optional" : []
        }
        requiredListRyzner = ["pH", "Alkalinity","Calcium",
                              "Electrical Conductivity","Total Dissolved Solids",
                              "Temperature"]
        if(self.material == "Stainless steel 304/304L" or self.material == "Stainless steel 316/316L" or 
        self.material == "Stainless steel Alloy 20" or self.material == "Stainless steel 904L" or self.material == "Duplex Stainless Steel" ):
            for assement in self.assesments:
                if(assement == "Corrosion" or assement == "Scaling"):
                    ryzner = []
                    for r_input in requiredListRyzner:
                        try:
                            if(self.errors[r_input] == "Not Entered"):
                                ryzner.append(r_input)
                        except Exception as e:
                            print(f'Error validation ryzner: {e}')
                            continue
                    if(len(ryzner) > 0) : errorSheet["Required"].append({"Ryzner":ryzner})
                if(assement == "Corrosion"):
                    try:
                        if(self.errors["Flouride"] == "Not Entered"):
                            errorSheet["Optional"].append({"Pitting Corrosion":["Flouride"]})
                    except Exception as e:
                        print(f'Error validation pitting corrosion: {e}')        
                elif(assement == "Scaling"):
                    optional_sil = ["Silica", "Magnesium"]
                    optional_cal =["Calcium", "Sulphate"]
                    casu =[]
                    smagn = []
                    try:
                        if(self.errors["Silica in steam"] == "Not Entered"):
                            errorSheet["Optional"].append({"Silica Film Formation":["Silica in steam"]})
                    except Exception as e: 
                        print(f'Error validation silica in steam: {e}')
                    #--------------------------------Silica & Magnesium
                    for s_input in optional_sil:
                        try:
                            if(self.errors[s_input] == "Not Entered"):
                                smagn.append(s_input)
                        except Exception as e:
                            print(f'Error validation Silica magnesium: {e}')
                            continue
                    if(len(smagn)> 0) : errorSheet["Optional"].append({"Magnesium Silica Scaling":smagn})
                    
                    #-------------------------------Calcium and sulphate
                    for c_input in optional_cal:
                        try:
                            if(self.errors[c_input] == "Not Entered"):
                                casu.append(c_input)
                        except Exception as e:
                            print(f'Error validation calcium: {e}')
                            continue
                    if(len(casu) > 0): errorSheet["Optional"].append({"Calcium Sulphate Scaling":casu})
                elif(assement == "Fouling"):
                    try:
                        if(self.errors["Suspended Solids"] == "Not Entered"):
                            errorSheet["Optional"].append({"Fouling":["Suspended Solids"]})
                    except Exception as e:
                        print(f'Error validation Suspended solids: {e}')
        elif(self.material == "Carbon Steel"):
            for assement in self.assesments:
                if(assement == "Corrosion" or assement == "Scaling"):
                    ryzner = []
                    for r_input in requiredListRyzner:
                        try:
                            if(self.errors[r_input] == "Not Entered"):
                                ryzner.append(r_input)
                        except Exception as e:
                            print(f'Error validation ryzner: {e}')
                            continue
                    if(len(ryzner) > 0) : errorSheet["Required"].append({"Ryzner":ryzner})
                if(assement == "Corrosion"):
                    corrRateReq = ["pH", "Alkalinity","Calcium","Chloride",
                              "Electrical Conductivity","Sulphate","Dissolved Oxygen","Total Dissolved Solids",
                              "Temperature","Days of Exposure","Magnesium"]
                    corrRate = []
                    for corr_input in corrRateReq:
                        try:
                            if(self.errors[corr_input] == "Not Entered"):
                                corrRate.append(corr_input)
                        except Exception as e:
                            print(f'Error validation Coorsion rate: {e}')
                            continue
                    if(len(corrRate)>0):errorSheet["Optional"].append({"Corrosion Rate":corrRate})
                elif(assement == "Scaling"):
                    optional_sil = ["Silica", "Magnesium"]
                    optional_cal =["Calcium", "Sulphate"]
                    casu =[]
                    smagn = []
                    try:
                        if(self.errors["Silica in steam"] == "Not Entered"):
                            errorSheet["Optional"].append({"Silica Film Formation":["Silica in steam"]})
                    except Exception as e: 
                        print(f'Error validation Silica in: {e}')
                    #--------------------------------Silica & Magnesium
                    for s_input in optional_sil:
                        try:
                            if(self.errors[s_input] == "Not Entered"):
                                smagn.append(s_input)
                        except Exception as e:
                            print(f'Error validation silica magnesium: {e}')
                            continue
                    if(len(smagn)> 0) : errorSheet["Optional"].append({"Magnesium Silica Scaling":smagn})
                    
                    #-------------------------------Calcium and sulphate
                    for c_input in optional_cal:
                        try:
                            if(self.errors[c_input] == "Not Entered"):
                                casu.append(c_input)
                        except Exception as e:
                            print(f'Error validation calcium and sulphate: {e}')
                            continue
                    if(len(casu) > 0): errorSheet["Optional"].append({"Calcium Sulphate Scaling":casu})

                elif(assement == "Fouling"):
                    try:
                        if(self.errors["Suspended Solids"] == "Not Entered"):
                            errorSheet["Optional"].append({"Fouling":["Suspended Solids"]})
                    except Exception as e:
                        print(f'Error validation suspended solids: {e}')
        elif(self.material == "Concrete"):
            for assement in self.assesments:
                if(assement == "Corrosion" or assement == "Scaling"):
                    ryzner = []
                    for r_input in requiredListRyzner:
                        try:
                            if(self.errors[r_input] == "Not Entered"):
                                ryzner.append(r_input)
                        except Exception as e:
                            print(f'Error validation concrete: {e}')
                            continue
                    if(len(ryzner) > 0) : errorSheet["Required"].append({"Ryzner":ryzner})
                if(assement == "Corrosion"):
                    aggReq = ["pH","Magnesium","Alkalinity", "P Alkalinity","Calcium"]
                    agg = []
                    for a_input in aggReq:
                        try:
                            if(self.errors[a_input] == "Not Entered"):
                                agg.append(a_input)
                        except Exception as e:
                            print(f'Error validation aggressive: {e}')
                            continue
                    if(len(agg)>0):errorSheet["Optional"].append({"Corrosion Rate":agg})
                elif(assement == "Scaling"):
                    try:
                        if(self.errors["Sulphate"] == "Not Entered"):
                            errorSheet["Optional"].append({"Sulphate Attack":["Sulphate"]})
                    except Exception as e:
                        print(f'Error validation suspended solids: {e}')
                elif(assement == "Fouling"):
                    try:
                        if(self.errors["Suspended Solids"] == "Not Entered"):
                            errorSheet["Optional"].append({"Fouling":["Suspended Solids"]})
                    except Exception as e:
                        print(f'Error validation suspended solids: {e}')
        elif(self.material == "Monel-Lead/Copper Alloys"):
            for assement in self.assesments:
                if(assement == "Corrosion" or assement == "Scaling"):
                    ryzner = []
                    for r_input in requiredListRyzner:
                        try:
                            if(self.errors[r_input] == "Not Entered"):
                                ryzner.append(r_input)
                        except Exception as e:
                            print(f'Error validation required ryzner: {e}')
                            continue
                    if(len(ryzner) > 0) : errorSheet["Required"].append({"Ryzner":ryzner})
                if(assement == "Corrosion"):
                    csmrReq = ["Chloride", "Sulphate"]
                    larsReq = ["Chloride", "Sulphate","P Alkalinity","Alkalinity"]
                    csmr = []
                    lars = []
                    for csm_input in csmrReq:
                        try:
                            if(self.errors[csm_input] == "Not Entered"):
                                csmr.append(csm_input)
                        except Exception as e:
                            print(f'Error csmr validation: {e}')
                            
                    if(len(csmr)>0): errorSheet["Optional"].append({"Chloride to Sulphate Mass Ration":csmr})
                    for lars_input in larsReq:
                        try:
                            if(self.errors[lars_input] == "Not Entered"):
                                lars.append(lars_input)
                        except Exception as e:
                            print(f'Erro validation larson:  {e}')
                            
                    if(len(lars)>0) : errorSheet["Optional"].append({"Larson Index":lars})

                elif(assement == "Scaling"):
                    optional_sil = ["Silica", "Magnesium"]
                    optional_cal =["Calcium", "Sulphate"]
                    casu =[]
                    smagn = []
                    try:
                        if(self.errors["Silica in steam"] == "Not Entered"):
                            errorSheet["Optional"].append({"Silica Film Formation":["Silica in steam"]})
                    except Exception as e: 
                        print(f'Error Silica Validation Scaling: {e}')
                    #--------------------------------Silica & Magnesium
                    for s_input in optional_sil:
                        try:
                            if(self.errors[s_input] == "Not Entered"):
                                smagn.append(s_input)
                        except Exception as e:
                            print(f'Error Silic magnesium validation: {e}')
                            continue
                    if(len(smagn)> 0) : errorSheet["Optional"].append({"Magnesium Silica Scaling":smagn})
                    
                    #-------------------------------Calcium and sulphate
                    for c_input in optional_cal:
                        try:
                            if(self.errors[c_input] == "Not Entered"):
                                casu.append(c_input)
                        except Exception as e:
                            print(f'Error Calcium Validation: {e}')
                            continue
                    if(len(casu) > 0): errorSheet["Optional"].append({"Calcium Sulphate Scaling":casu})

                elif(assement == "Fouling"):
                    try:
                        if(self.errors["Suspended Solids"] == "Not Entered"):
                            errorSheet["Optional"].append({"Fouling":["Suspended Solids"]})
                    except Exception as e:
                        print(f'Error Validation Suspended solids: {e}')
        elif(self.material == "Plastic"):
            for assement in self.assesments:
                if(assement == "Scaling"):
                    ryzner = []
                    for r_input in requiredListRyzner:
                        try:
                            if(self.errors[r_input] == "Not Entered"):
                                ryzner.append(r_input)
                        except Exception as e:
                            print(f'Error Validation Ryzner: {e}')
                            continue
                    if(len(ryzner) > 0) : errorSheet["Required"].append({"Ryzner":ryzner})
                elif(assement == "Fouling"):
                    try:
                        if(self.errors["Suspended Solids"] == "Not Entered"):
                            errorSheet["Optional"].append({"Fouling":["Suspended Solids"]})
                    except Exception as e:
                        print(f'Error Suspended Solids Fouling: {e}')
        elif(self.material == "Membranes"):
            for assement in self.assesments:
                if(assement == "Corrosion" or assement == "Scaling"):
                    langLReq = ["pH","Calcium","Alkalinity","Total Dissolved Solids","Temperature"]
                    langRate = []
                    for langInp in langLReq:
                        try:
                            if(self.errors[langInp] == "Not Entered"):
                                langRate.append(langInp)
                        except Exception as e:
                            print(f'Error validation Langleier Index: {e}')
                            continue
                    if(len(langRate)>0):errorSheet["Required"].append({"Langlier Index":langRate})
                elif(assement == "Fouling"):
                    try:
                        if(self.errors["Suspended Solids"] == "Not Entered"):
                            errorSheet["Required"].append({"Fouling":["Suspended Solids"]})
                    except Exception as e:
                        print(f'Error Suspended Solids Validation Fouling: {e}')
                    #---------------------------------------------------------------Particle Size----------------------------------------------
                    try:
                        if(self.errors["Particle Size"] == "Not Entered"):
                            errorSheet["Optional"].append({"Fouling":["Particle Size"]})
                    except Exception as e:
                        print(f'Error Particle Size Validation Fouling: {e}')
                    #--------------------------------------------------------------------Silt Index---------------------------------------------
                    try:
                        if(self.errors["Silt Density Index"] == "Not Entered"):
                            errorSheet["Optional"].append({"Fouling":["Silt Density Index"]})
                    except Exception as e:
                        print(f'Error Silt Density Index Validation Fouling: {e}')
        if(len(errorSheet["Required"]) > 0 or len(errorSheet["Optional"]) > 0):
            data = {}
            if(len(errorSheet["Required"]) > 0):
                data['Required'] = errorSheet["Required"]
            if(len(errorSheet["Optional"]) > 0):
                data['Optional'] = errorSheet["Optional"]
            self.ui_validationDialog = self.ctx.input_validation_setter(data)
            self.ui_validationDialog.show()

            if(self.ui_validationDialog.exec() == 1):
                self.calculate()
        else:
            self.calculate()
        #if(len(errorSheet['Required']) <= 0):
            #self.calculate()

        # for error_keys,error_items in errorSheet.items():
        #     print(f'keys -> {error_keys}')
        #     print("----------")
        #     print(f"Items: -> {error_items}")
 