from fbs_runtime.application_context.PyQt5 import ApplicationContext,cached_property
from PyQt5.QtWebEngineWidgets import QWebEngineView,QWebEnginePage
from PyQt5.QtWidgets import QComboBox,QApplication, QDialog, QDialogButtonBox, QLabel, QMainWindow, QTableWidget, QTextEdit, QWidget, QDesktopWidget,QFileDialog

from PyQt5 import QtPrintSupport
from PyQt5.QtPrintSupport import QPrinter

import sys
import pandas as pd
from PyQt5 import QtCore, QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import uic
from typing import Any
import json
import math
import os


from Proxy import ProxyModel
from reporting import GeneratePDF

#-----------------------------------------------------------------------------------------------------Global Variables-----------------------------------------------------------
Field_data = {
            
            "unit" : 0,
            "material": 0,
            "unit" : 0,
            "corrosion": False,
            "scaling": False,
            "fouling": False
        }
#-----------------------------------------------------------------------------------------------------Calculations----------------------------------------------------------------
#------------------------------------------------------------------------------------------------------App Context----------------------------------------------------------------
class AppContext(ApplicationContext):
    App_data={

    }
    def __init__(self):
        super().__init__()
        self.inputWindow = None
        self.validationWindow = None
    def run(self):
        self.main_window.show()
        self.app.setStyle('Fusion')
        return self.app.exec_()

    @cached_property
    def main_window(self):
        return MainWindow(self)


    @cached_property
    def about_window(self):
        return AboutWindow(self)

    @cached_property
    def license_window(self):
        return LicenseWindow(self)
    @cached_property
    def app_window(self):
        return AppWindow(self)
    @cached_property
    def water_window(self):
        return WaterQualityWindow(self)
    # @cached_property 
    # def sector_window(self):
    #     return SectorWindow(self,self.App_data)

    def sector_setter(self,level):
        self.App_data["level"] = "Advanced"
        return self.sector_window

    def report_window_setter(self,analysis,material,assesments,inputs,user,info):
        return ReportsWindow(self,analysis,material,assesments,inputs,user,info)
        

    
    def input_window(self):
        return self.inputWindow

    def input_window_setter(self,data):        
        self.App_data.update(data)
        self.inputWindow = InputsWindow(self,self.App_data)
        return self.inputWindow

    def input_validation_setter(self,data):
        self.validationWindow = ValidationDialog(self,data)
        return self.validationWindow   

    def user_info_setter(self,data):
        return UserInfo(self,data)

    @cached_property
    def get_appWindow(self):
        return self.get_resource("New_UI/Main.ui")
    @cached_property 
    def get_waterQuality(self):
        return self.get_resource("New_UI/WaterQuality.ui")
    @cached_property
    def get_siteSpecific(self):
        return self.get_resource("New_UI/SiteSpecific.ui")
    
    @cached_property
    def get_about(self):
        return self.get_resource("about.ui")
    @cached_property
    def get_report(self):
        #return self.get_resource("reports.ui")
        return self.get_resource("New_UI/Report.ui")
    @cached_property
    def get_main(self):
        return self.get_resource("New_UI/Home.ui")
    @cached_property
    def get_sector(self):
        return self.get_resource("sector_new.ui")
    @cached_property
    def get_inputs(self):
        #return self.get_resource("bInput.ui")
        return self.get_resource("New_UI/parameterInputs.ui")
    @cached_property
    def get_validation(self):
        return self.get_resource("validation.ui")
    @cached_property
    def get_license(self):
        return self.get_resource("license.ui")
    @cached_property
    def get_userInfo(self):
        return self.get_resource("userInfo.ui")
    @cached_property
    def get_help(self):
        return self.get_resource("help.ui")
    @cached_property
    def get_background(self):
        return self.get_resource("background.ui")
    @cached_property
    def homePic(self):
        return qtg.QImage(self.get_resource("images/homeImage.png"))
    @cached_property
    def import_data(self):
        fileCreator = self.get_resource("data/Sectors.csv")
        sector_inputs = pd.read_csv(fileCreator,header=None,delimiter=";")
        return sector_inputs

    @cached_property
    def import_inputs_data(self):
        fileName = self.get_resource("data/data.json")
        with open(fileName,'r') as file:
            # Opening JSON file
            data = json.load(file)
        return data
    @cached_property
    def import_units_data(self):
        fileName = self.get_resource("data/units.json")
        with open(fileName,'r') as file:
            # Opening JSON file
            data = json.load(file)
        return data

    
    def retrieve_html(self, material):
        fileName = self.get_resource(f"data/{material}.html")
        with open(fileName, 'r') as file:
            html = file.read()
        return html
    
    @cached_property
    def get_param_filename(self):
        return self.get_resource("data/parameters.json")

    def import_param_data(self):
        fileName = self.get_param_filename
        with open(fileName,'r') as file:
            # Opening JSON file
            data = json.load(file)
        return data
    def write_json(self,new_data):
        fileName = self.get_param_filename
        with open(fileName,'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data.update(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file)
            file.truncate()
    def delete_json(self,new_data):
        fileName = self.get_param_filename
        with open(fileName,'r+') as file:
            file.seek(0)
            # convert back to json.
            json.dump(new_data, file)
            file.truncate()
#----------------------------------------------------------------------------------------------------------HTML REPORT----------------------------------------------------
#--------------------------------------------------------------------------------------------------------Calculations----------------------------------------------------------
def Bicarbonate(pAlkalinity, tAlkalinity):
    bCarb = 0
    if(pAlkalinity == 0):
        bCarb = tAlkalinity
    elif(pAlkalinity == tAlkalinity ):
        bCarb = 0       #J5
    elif(2 * pAlkalinity == tAlkalinity):
        bCarb = 0       #J6
    elif(2 * pAlkalinity < tAlkalinity):
        bCarb = (tAlkalinity - 2* pAlkalinity) if (pAlkalinity > 0) else 0  #J7
    elif(2 * pAlkalinity > tAlkalinity):
        bCarb = 0       #J8
    else :
        bCarb = 0 

    return bCarb
def Carbonate(pAlkalinity, tAlkalinity):
    carb = 0
    if(pAlkalinity == 0):
        carb = 0
    elif(pAlkalinity == tAlkalinity ):
        carb = 0       #I5
    elif(2 * pAlkalinity == tAlkalinity):
        carb = 2 * pAlkalinity #I6
    elif(2 * pAlkalinity < tAlkalinity):
        carb = 2 * pAlkalinity if (pAlkalinity > 0) else 0      #i7
    elif(2* pAlkalinity > tAlkalinity):
        carb = 2 * (tAlkalinity - pAlkalinity)
    else:
        carb = 0
    return carb
def Aggressive(inputs):
    TotalHardness = (inputs["Calcium"] * 2.5) + (inputs["Magnesium"] *4.1)
    carbonate = Carbonate(inputs['P Alkalinity'], inputs['Alkalinity'])
    bicarbonate = Bicarbonate(inputs["P Alkalinity"], inputs["Alkalinity"])

    alkalinity = (bicarbonate * 50.04/61.008) + (2 * carbonate * (50.04/61.008))

    print(f"Carbonate: {carbonate}")
    print(f"Bicarbonate: {bicarbonate}")
    print(f'Alkalinity: {alkalinity}')
    print(f'Hardness: {TotalHardness}')
    temp = TotalHardness * alkalinity
    aggressive = inputs["pH"] + math.log(temp, 10)
    return aggressive
def Langelier(inputs):
    CalciumHardness = inputs['Calcium'] / 0.401
    A = (math.log((inputs['Total Dissolved Solids']),10) -1) / 10
    B = (-13.12) *math.log((inputs["Temperature"] +273.2), 10) + 34.55
    C = math.log(CalciumHardness,10) - 0.4
    D = math.log(inputs['Alkalinity'],10)  #needs to be investigated
    
    print(f"Langlier A:{A}")
    print(f"Langlier B:{B}")
    print(f"Langlier C:{C}")
    print(f"Langlier D:{D}")
    phs = (9.3 + A + B) - (C + D) 
    print(f"Langlier phs{phs}")
    langelier = inputs["pH"] - phs
    print(f"Langlier : {langelier}")
    return langelier    
def rsiAtTemp(temp, inputs):
    CalciumHardness = inputs['Calcium'] / (40.08/2)
    TotalHardness = (inputs["Calcium"] * 2.5) + (inputs["Magnesium"] *4.1) 
    rsi = (
        2 * (
                11.017 + 0.197* math.log(abs(inputs['Total Dissolved Solids'] +1), 10)
                - 0.995 * math.log(abs((CalciumHardness * 0.4) - 1), 10)
                - 0.016 * math.log(abs((TotalHardness - CalciumHardness)* 0.24 + 1)) 
                - 1.041 * math.log(abs(inputs["Alkalinity"] - 1), 10)
                + 0.021 * math.log(abs(inputs["Sulphate"] + 1), 10)
                - (temp * (9 / 5) + 32 - 77)/120.5
            ) - inputs["ph"]
    )
    return rsi
def Pisigan(inputs):
    CalciumHardness = inputs['Calcium'] / (40.08/2)
    #MagnesiumHardness = inputs["Magnesium"]/(24.32/2)
    #TotalHardness = (inputs["Calcium"] * 2.5) + (inputs["Magnesium"] *4.1) 
    langlier = Langelier(inputs)
    #rsi_40 = rsiAtTemp(40,inputs)
    #rsi_60 = rsiAtTemp(60, inputs)
    #rsi_80 = rsiAtTemp(80, inputs)
    #phs = rsiAtTemp(inputs["Temperature"], inputs)

    ea = inputs["Alkalinity"] / 50045.5
    i = inputs["Total Dissolved Solids"] /40000
    t = ts = inputs["Temperature"] + 273.15
    d = -7.047968 + 0.016796 * t + 1795.711/t - 0.0000141566*(t**2)-153541/(t**2)
    dw = 87.74-0.4008* inputs["Temperature"] + 0.0009398*(inputs["Temperature"]**2)+0.00000141*(inputs["Temperature"]**3)
    aa = 1824600*(d**0.5)/(dw*t)**1.5
    bb = 50.29*d**0.5/(dw*t)**0.5
    yc =(-aa*4*(i**0.5)/(1+(bb*5*(i**0.5)))+0.165*i)
    yr = - aa *4*(i**0.5)/(1+(bb*5.4*(i**0.5)))
    ya = -aa*1*(i**0.5)/(1+(bb*5.4*(i**0.5)))
    yh = -aa*1*(i**0.5)/(1+(bb*9*(i**0.5)))
    yx = -aa*1*(i**0.5)/(1+(bb*3.5*(i**0.5)))
    yu = -0.5 * i
    k1_a  = -356.3094-0.06091964*t+21834.37/t+126.8339*math.log(t,10)-1684915/(t**2)
    k2_a = -107.8871-0.03252849*t+5151.79/t+38.92561*math.log(t,10)-563713.9/(t**2)
    kw_a = 35.3944-0.00853*t-5242.39/t-11.8261*math.log(t,10)

    k1_b = 10**(k1_a+yu-yh-ya)
    k2_b = 10**(k2_a+ya-yh-yr)
    kw_b = 10**(kw_a-yh-yx)

    h =10**(-inputs["pH"]- yh)
    cd = h*h+k1_b*h+k1_b*k2_b
    r3 = k1_b * k2_b/cd
    oh = kw_b/h

    b1 =r3*h*((ea*h)+(h*h)-kw_b)
    b2 =(k1_b*h)+(2*k1_b*k2_b)
    b3 =(h/k2_b)+(k1_b/h)+4
    bi =2.303*((b1*b3/b2)+oh+h)*50045

    js =(inputs["Chloride"]**0.509)*(inputs["Sulphate"]**0.0249)*(inputs["Alkalinity"]**0.423)*(inputs["Dissolved Oxygen"]**0.799)
    rp = ((0.4*CalciumHardness)**0.676)*(bi**0.0304)*((10**langlier)**0.107)*(inputs['Days of Exposure']**0.382)

    corrosionRate = js/rp
    return corrosionRate
def Larson(inputs):
    chloride_ = inputs["Chloride"] /35.45
    sulphate_ = inputs["Sulphate"]/48.03

    bicarbonate = Bicarbonate(inputs['P Alkalinity'],inputs['Alkalinity'])/61
    carbonate = Carbonate(inputs['P Alkalinity'],inputs["Alkalinity"])/30

    #print(f"Larson cl-: {chloride_}")
    #print(f"Larson SO-: {sulphate_}")
    #print(f"Larson HCO-: {carbonate}")
    #print(f"Larson CO3-: {bicarbonate}")
    larson = (chloride_ + sulphate_ )/(bicarbonate + carbonate)

    return larson
def Ryzner(inputs):
    tempCalcium = (inputs["Calcium"] * 10) / 4.01
    print("Temp Calcium:{}".format(tempCalcium))
    A = (math.log((inputs['Total Dissolved Solids']),10)-1) / 10
    print("A:{}".format(A))
    B = (-13.12) *math.log((inputs["Temperature"] +273.2), 10) + 34.55
    print("B:{}".format(B))
    C = math.log(tempCalcium,10) - 0.4
    print("C:{}".format(C))
    D = math.log(inputs['Alkalinity'],10)  #needs to be investigated
    print("D:{}".format(D))
    phs = (9.3 + A + B) - (C + D)
    print("phs:{}".format(phs))
    ryzner = 2 * phs - inputs["pH"] 

    return ryzner
def Analyze(material,assesments,inputs):
    data = {}
    print(f"Inputs : {inputs}")
    if(material == "Stainless steel 304/304L" or material == "Stainless steel 316/316L" or 
        material == "Stainless steel Alloy 20" or material == "Stainless steel 904L" or material == "Duplex Stainless Steel" ):

        
        for assessment in assesments:
            try:
                if(assessment == "Corrosion" or assessment == "Scaling"):
                #calculate Ryzner
                    data['ryzner'] = Ryzner(inputs)
                    print("Ryzner Index: {}".format(data['ryzner']))
                if(assessment == "Corrosion"):
                    #Calclulate Flouride
                    data["Flouride"] = inputs["Flouride"]
                    #Calclualte Chloride
                    data["Chloride"] = inputs["Chloride"]
                    #Calculate Temperature
                    data["Temperature"] = inputs["Temperature"]
                    #Calculate pH
                    data["pH"] = inputs["pH"]
                    if(material == "Stainless steel 316/316L"):
                        data["Critical Pitting Temp"] = 18
                        data["PREN"] = 20
                    elif(material == "Stainless steel 316/316L"):
                        data["Critical Pitting Temp"] = 20
                        data["PREN"] = 25
                    elif(material == "Stainless steel Alloy 20"):
                        data["Critical Pitting Temp"] = 90
                        data["PREN"] = 30
                    elif(material == "Stainless steel 904L"):
                        data["Critical Pitting Temp"] = 40
                        data["PREN"] = 36
                    elif(material == "Duplex Stainless Steel"):
                        data["Critical Pitting Temp"] = 65
                        data["PREN"] = 46    
                elif(assessment == "Scaling"):
                    #Calculate Silica in steam
                    if(inputs["Silica in steam"] > 1):
                        data["Silica Concentration in steam"] = inputs["Silica in steam"]
                    #Calculate pH, Magnesium and Silica 
                    data["pH"] = inputs["pH"]
                    if(inputs["Silica"]):
                        data["SilicaMagnesium"] = inputs["Silica"] * inputs["Magnesium"]
                    #Water Treatment, Ca * S0$
                    ##data["WaterTreatment"] = inputs["WaterTreatment"]
                    data['WaterTreatment'] = inputs["Contains Antiscalants?"]
                    
                    data["CalciumSulphate"] = inputs["Calcium"] * inputs["Sulphate"]
                elif(assessment == "Fouling"):
                    #Calculate Suspended solids
                    data["Suspended Solids"] = inputs["Suspended Solids"]
                    print( data["Suspended Solids"])
            except Exception as e:
                print(f"Stainless Steal Calculation Error: {e}")
                continue
    elif(material == "Carbon Steel"):
        for assessment in assesments:
            try:
                if(assessment == "Corrosion" or assessment == "Scaling"):
                    #calculate Ryzner
                    data['ryzner'] = Ryzner(inputs)
                    print("Ryzner Index: {}".format(data['ryzner']))
                if(assessment == "Corrosion"):
                    #Larson Scold Index
                    data['larson'] = Larson(inputs)
                    print(f'Larson Index: {data["larson"]}')
                    #pisigan and Shingley Index & Corrosion Rate
                    data["pisigan corrosion"] = Pisigan(inputs) 
                    #If Open or Closed Reticulation
                    data["reticulation"] = inputs["Open reticulation system?"]

                    print(f'Pisigan Index:{ data["pisigan corrosion"]}')
                elif(assessment == "Scaling"):
                    #Calculate Silica in steam
                    if(inputs["Silica in steam"] > 1):
                        data["Silica Concentration in steam"] = inputs["Silica in steam"]
                    data["pH"] = inputs["pH"]
                    if(inputs["Silica"]):
                        data["SilicaMagnesium"] = inputs["Silica"] * inputs["Magnesium"]
                    #Water Treatment, Ca * S0$
                    #data["WaterTreatment"] = inputs["WaterTreatment"]
                    data['WaterTreatment'] = inputs["Contains Antiscalants?"]
                    data["CalciumSulphate"] = inputs["Calcium"] * inputs["Sulphate"]

                    print(" Calcium Sulpahate: {}...".format(data["CalciumSulphate"]))
                elif(assessment == "Fouling"):
                    #Calculate Suspended solids
                    data["Suspended Solids"] = inputs["Suspended Solids"]
                    print( data["Suspended Solids"])
            except Exception as e:
                print(f'Carbon Steel Calculation error: {e}')
                continue
    elif(material == "Concrete"):
        for assessment in assesments:
            try:
                if(assessment == "Corrosion" or assessment == "Scaling"):
                    #calculate Ryzner
                    data['ryzner'] = Ryzner(inputs)
                    print("Ryzner Index: {}".format(data['ryzner']))
                if(assessment == "Corrosion"):
                    #Calculate Aggressive Index
                    data["Aggressive"] = Aggressive(inputs)
                    #IsConcrete Reinforced
                    data["Concrete Reinforced"] = inputs['Is the concrete reinforced?']
                    print(data["Aggressive"])
                elif(assessment == "Scaling"):
                    
                    #Calculate The Sulphate
                    data["Sulphate"] = inputs["Sulphate"]
                    print("Sulpahate Conc: {}...".format( data["Sulphate"]))
                elif(assessment == "Fouling"):
                    #Calculate Suspended solids
                    data["Suspended Solids"] = inputs["Suspended Solids"]
                    print( data["Suspended Solids"])
            except Exception as e:
                print(f"Error !Concrete in Fouling,: {e}")
                continue
    elif(material == "Monel-Lead/Copper Alloys"):
        for assessment in assesments:
            try:
                if(assessment == "Corrosion" or assessment == "Scaling"):
                    #calculate Ryzner
                    data['ryzner'] = Ryzner(inputs)
                    print("Ryzner Index: {}".format(data['ryzner']))
                if(assessment == "Corrosion"):
                    #Larson Skold Index
                    data['larson'] = Larson(inputs)
                    print(data["larson"])
                    #Chloride to Sulphate Mass Ratio
                    data["csmr"] = inputs['Chloride'] / inputs["Sulphate"]
                    #PREN
                    #Does material Contain lead or copper
                    data["Lead or Copper"] = True if (inputs["Does Material contain Lead?"] or inputs["Does Material contain Copper?"]) else False

                    print(data["csmr"])
                elif(assessment == "Scaling"):
                    #Calculate Silica in boiler steam
                    if(inputs["Silica in steam"] > 1):
                        data["Silica Concentration in steam"] = inputs["Silica in steam"]
                    #Calculate pH, Magnesium and Silica 
                    
                    data["pH"] = inputs["pH"]
                    try:
                        data["SilicaMagnesium"] = inputs["Silica"] * inputs["Magnesium"]
                    except Exception as e:
                        print(f'Alloy Error Silica Magnesium: {e}')
                    #Water Treatment, Ca * S0$
                    #data["WaterTreatment"] = inputs["WaterTreatment"]
                    data['WaterTreatment'] = inputs["Contains Antiscalants?"]
                    try:
                        
                        data["CalciumSulphate"] = inputs["Calcium"] * inputs["Sulphate"]
                    except Exception as e:
                        print("Alloy Error Calcium: {e}")
                elif(assessment == "Fouling"):
                    #Calculate Suspended solids
                    data["Suspended Solids"] = inputs["Suspended Solids"]
                    print( data["Suspended Solids"])
            except Exception as e:
                print(f"Alloy calculation error: {e}")
                continue
    elif(material == "Plastic"):
        for assessment in assesments:
            try:
                if(assessment == "Scaling"):
                    #Calculate Ryzner Index
                    data['ryzner'] = Ryzner(inputs)
                    print("Ryzner Index: {}".format(data['ryzner']))
                elif(assessment == "Fouling"):
                    #Suspended Solids
                    data["Suspended Solids"] = inputs["Suspended Solids"]
                    print( data["Suspended Solids"])
            except Exception as e:
                print(f"Plastic Caclution error: {e}")

    elif(material == "Membranes"):
        for assessment in assesments:
            try:
                if(assessment == "Corrosion" or assessment == "Scaling"):
                    try:
                        data["Langlier"] = Langelier(inputs)
                    except Exception as e:
                        print(f"Langlier Calculation Error: {e}")
                elif(assessment == "Fouling"):
                    #Silt Index Sensity
                    try:
                        if(inputs["Silt Density Index"] > 0):
                            data["Silt Density Index"] = inputs["Silt Density Index"]
                    except KeyError as k:
                        print("Error Silt Density")
                        
                    #Particle Size
                    try:
                        if(inputs["Particle Size"] > 0):
                            data["Particle Size"] = inputs["Particle Size"]
                            data["Technology Type"] = inputs['Technology Type']
                    except KeyError as k:
                        print(f"Particle Size key error: {k}")
                        
                    #Suspended Solids
                    data["Suspended Solids"] = inputs["Suspended Solids"]
                    print( data["Suspended Solids"])
            except Exception as e:
                print(f"Error Membranes Calculation: {e}")
                continue
    print(f'Calucalted Data: {data}')
    return data
#--------------------------------------------------------------------------------------------------------License Window--------------------------------------------------------
class LicenseWindow(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.ctx = args[0]
        uic.loadUi(self.ctx.get_license,self)

#--------------------------------------------------------------------------------------------------------About Page-------------------------------------------------------------
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

#--------------------------------------------------------------------------------------------------------User Information---------------------------------------------------------
class UserInfo(QDialog,qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.ctx = args[0]
        uic.loadUi(self.ctx.get_userInfo,self)

        self.data = args[1]

        self.fullNameLineEdit.setText(self.data["fullName"])
        self.emailLineEdit.setText(self.data["email"])
        self.roleLineEdit.setText(self.data["role"])
        self.companyLineEdit.setText(self.data["company"])
        self.locationLineEdit.setText(self.data["location"])
        self.descriptionLineEdit.appendPlainText(self.data["description"])
        
        self.buttonInfo.accepted.connect(self.saveData)

    def saveData(self):
        self.data["fullName"] = self.fullNameLineEdit.text()
        self.data["email"] = self.emailLineEdit.text()
        self.data["role"] = self.roleLineEdit.text()
        self.data["company"] = self.companyLineEdit.text()
        self.data["location"] = self.locationLineEdit.text()
        self.data["description"] = self.descriptionLineEdit.toPlainText()
#--------------------------------------------------------------------------------------------------------Reports Window-----------------------------------------------------------

class HighlightDelegate(qtw.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(HighlightDelegate, self).__init__(parent)
        self._filters = []
        self._wordwrap = False
        self.doc = qtg.QTextDocument(self)
    def createEditor(self,parent,option,index):
        print('createEditor event fired')
        return

    def paint(self, painter, option, index):
        painter.save()
        options = qtw.QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        self.doc.setPlainText(options.text)
        self.apply_highlight()

        if self._wordwrap:
            self.doc.setTextWidth(options.rect.width())
        options.text = ""

        style = QApplication.style() if options.widget is None else options.widget.style()
        style.drawControl(qtw.QStyle.CE_ItemViewItem, options, painter)

        if self._wordwrap:
            painter.translate(options.rect.left(), options.rect.top())
            clip = QtCore.QRectF(QtCore.QPointF(), QtCore.QSizeF(options.rect.size()))
            self.doc.drawContents(painter, clip)
        else:
            ctx = qtg.QAbstractTextDocumentLayout.PaintContext()
            if option.state & qtw.QStyle.State_Selected:
                ctx.palette.setColor(qtg.QPalette.Text, option.palette.color(
                    qtg.QPalette.Active, qtg.QPalette.HighlightedText))
            else:
                ctx.palette.setColor(qtg.QPalette.Text, option.palette.color(
                    qtg.QPalette.Active, qtg.QPalette.Text))
            textRect = style.subElementRect(qtw.QStyle.SE_ItemViewItemText, options, None)
            if index.column() != 0:
                textRect.adjust(5, 0, 0, 0)
            constant = 4
            margin = (option.rect.height() - options.fontMetrics.height()) // 2
            margin = margin - constant
            textRect.setTop(textRect.top() + margin)
            painter.translate(textRect.topLeft())
            painter.setClipRect(textRect.translated(-textRect.topLeft()))
            self.doc.documentLayout().draw(painter, ctx)

        painter.restore()
        s = QtCore.QSize(self.doc.idealWidth(), self.doc.size().height())
        index.model().setData(index, s, QtCore.Qt.SizeHintRole)
    def apply_highlight(self):
        cursor = qtg.QTextCursor(self.doc)
        cursor.beginEditBlock()
        fmt = qtg.QTextCharFormat()
        fmt.setForeground(QtCore.Qt.red)
        for f in self.filters():
            highlightCursor = qtg.QTextCursor(self.doc)
            while not highlightCursor.isNull() and not highlightCursor.atEnd():
                highlightCursor = self.doc.find(f, highlightCursor)
                if not highlightCursor.isNull():
                    highlightCursor.mergeCharFormat(fmt)
        cursor.endEditBlock()

    @QtCore.pyqtSlot(list)
    def setFilters(self, filters):
        if self._filters == filters: return
        self._filters = filters
        self.parent().viewport().update()

    def filters(self):
        return self._filters

    def setWordWrap(self, on):
        self._wordwrap = on
        mode = qtg.QTextOption.WordWrap if on else qtg.QTextOption.WrapAtWordBoundaryOrAnywhere

        textOption = qtg.QTextOption(self.doc.defaultTextOption())
        textOption.setWrapMode(mode)
        self.doc.setDefaultTextOption(textOption)
        #self.parent().viewport().update()

class AlignDelegate(qtw.QStyledItemDelegate):
    def createEditor(self,parent,option,index):
        print('createEditor event fired')
        return
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = qtc.Qt.AlignCenter
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

        

       
        
        self.setWindowTitle("Fitness-of-use Report")
        print(args[1])
        self.report_data = self.parseTable()

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
        print("grid left done")


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

        print("grid right done")

        assesment_keys = list(self.report_data.keys())
        tabNumber = 0
        for key in assesment_keys:
            self.tab1 = QWidget()
            self.resultTab.addTab(self.tab1, f'{key}')
            self.tab1UI(key,self.report_data,tabNumber)
            tabNumber = tabNumber + 1
    def tab1UI(self,key,data,tabNumber):
        styleSheet = "QHeaderView::section{Background-color:#404040;color:#fff;text-align:center;font-weight:900}"

        layout = qtw.QVBoxLayout()
        
        table = qtw.QTableWidget()

        #Colum Count
        table.setColumnCount(5)
        #RowCount
        table.setRowCount(len(data[key]))
        table.setHorizontalHeaderLabels(["  Parameter ","Value","Risk Category","Description","Treatment Recommendations"])
        table.horizontalHeader().setStyleSheet("border: 1px solid #000;background-color:rgb(17, 111, 125);font-weight:700")
        table.horizontalHeader().setSectionResizeMode(0, qtw.QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(1, qtw.QHeaderView.Fixed)
        table.horizontalHeader().setSectionResizeMode(2, qtw.QHeaderView.Fixed)
        table.horizontalHeader().setSectionResizeMode(3, qtw.QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(4, qtw.QHeaderView.Stretch)

        table.horizontalHeader().resizeSection(1, 90)
        table.horizontalHeader().resizeSection(1, 120)

        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().hide()
        
        
        table.setStyleSheet(styleSheet)
        table.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        rowCount = 0
        
        
        

        self._delegate = HighlightDelegate(table)
        for item_key,item_value in data[key].items():
            
            table.setItemDelegate(self._delegate)
            self._delegate.setWordWrap(True)
            item1 = qtw.QTableWidgetItem(item_value['Risk'])

            if(item_value["Risk"] == "Unacceptable"):
                item1.setBackground(qtg.QColor(255,0,0))
                item1.setForeground(qtg.QColor(0,0,0))
            elif(item_value["Risk"] == "Tolerable"):
                item1.setBackground(qtg.QColor(255,255,0))
            elif(item_value["Risk"] == "Acceptable"):
                item1.setBackground(qtg.QColor(146,208,80)) 
            elif(item_value["Risk"] == "Ideal"):
                item1.setBackground(qtg.QColor(0,176,240))
            else:
                 item1.setBackground(qtg.QColor(40,40,40))

            table.setItem(rowCount, 0, qtw.QTableWidgetItem(f'{item_key}'))
            try:
                table.setItem(rowCount, 1, qtw.QTableWidgetItem(f"{round(item_value['Index'],2)}"))
                
            except TypeError as e:
                table.setItem(rowCount, 1, qtw.QTableWidgetItem(f"{item_value['Index']}"))
            table.setItem(rowCount, 2, item1)
            table.setItem(rowCount, 3, qtw.QTableWidgetItem(f"{item_value['Description']}"))
            table.setItem(rowCount, 4, qtw.QTableWidgetItem(f"{item_value['Treatment']}"))
            delegateAlign = AlignDelegate(table)
            table.setItemDelegateForColumn(1, delegateAlign)
            table.setItemDelegateForColumn(2, delegateAlign)
           
            
            table.setStyleSheet("font-size:13px;border:none")
            rowCount = rowCount + 1

            table.resizeRowsToContents()
            table.setMinimumSize(self.getQTableWidgetSize(table))
        
        
        
        
        
        
        

        layout.addWidget(table,0)
        layout.addStretch(1)
        self.resultTab.setTabText(tabNumber,f"{key}")
        self.tab1.setLayout(layout)  

    def showBack(self):
        print("Back pressed")
        self.inputs_window = self.ctx.input_window()
        self.inputs_window.show()
        self.close()    
    def getQTableWidgetSize(self,table):
        w = table.verticalHeader().width() + 4  # +4 seems to be needed
        for i in range(table.columnCount()):
            w += table.columnWidth(i)  # seems to include gridline (on my machine)
        h = table.horizontalHeader().height() + 4
        for i in range(table.rowCount()):
            h += table.rowHeight(i)
        return QtCore.QSize(w, h)

    def parseTable(self):
        analysis = self.analysis
        results = {

        }
        if(self.material == "Stainless steel 304/304L" or self.material == "Stainless steel 316/316L" or 
        self.material == "Stainless steel Alloy 20" or self.material == "Stainless steel 904L" or self.material == "Duplex Stainless Steel" ):
            for assessment in self.assessments:
                if(assessment == "Corrosion"):
                    Corrosion = {}
                    RyznerRes = {}
                    FlourideRes = {}
                    prenRes = {}
                    PittingRes = {}
                    chlorideRes = {}

                    #------------------------------------------------------Corrosion Ryzner-------------------------------------
                    if(analysis['ryzner'] >= 8.5):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Severe Corrosion due to lack of CaCO3 formation"
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] = """Chemical Treatment Recommended - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality
                        """
                    elif(analysis['ryzner'] < 8.5 and analysis['ryzner'] >= 7.8):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Mild Corrosion due to lack of CaCO3 formation"
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    elif(analysis['ryzner'] < 7.8 and analysis['ryzner'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Mild Corrosion due to lack of CaCO3 formation"
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    else:
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Minimal to no corrosion "
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = "No Treatment Required"
                    Corrosion["Ryzner Index"] = RyznerRes
                    #--------------------------------------------------Corrosion Flouride-------------------------------------------
                    try:
                        if(analysis["Flouride"] > 10):
                            FlourideRes["Index"] = round(analysis['Flouride'], 2)
                            FlourideRes["Description"] = "Severe pitting corrosion due to Flouride"
                            FlourideRes["Risk"] = "Unacceptable"
                            FlourideRes["Treatment"] = """
                                Consider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                        elif(analysis["Flouride"] <= 10 and analysis["Flouride"] > 5):
                            FlourideRes["Index"] = round(analysis['Flouride'], 2)
                            FlourideRes["Description"] = "Moderate pitting corrosion due to Flouride"
                            FlourideRes["Risk"] = "Tolerable"
                            FlourideRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                        elif(analysis["Flouride"] <= 5 and analysis["Flouride"] >= 1):
                            FlourideRes["Index"] = round(analysis['Flouride'], 2)
                            FlourideRes["Description"] = "Mild pitting corrosion due to Flouride"
                            FlourideRes["Risk"] = "Acceptable"
                            FlourideRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                        else:
                            FlourideRes["Index"] = round(analysis['Flouride'], 2)
                            FlourideRes["Description"] = "No pitting corrosion due to Flouride"
                            FlourideRes["Risk"] = "Ideal"
                            FlourideRes["Treatment"] = "No Treatment"
                        Corrosion["Pitting Corrosion due to Flouride (mg/l) "] = FlourideRes
                    except Exception as e:
                        print(f"Flouride Concentration Error- Report: {e}")
                        
                    #-------------------------------------------Pitting Corrosion----------------------------------------------------
                    try:
                        if(self.material == "Stainless steel 304/304L"):
                            prenRes["Index"] = 20
                            prenRes["Description"] = "Low sea water resistance"
                            prenRes["Risk"] = "Unacceptable"
                            prenRes["Treatment"] = """Treatment recommended - 
                                Consider a higher PREN alloy for use\nOR\nAddition of chemical corrosion inhibitors"""
                            
                            #Chloride Concentration
                            try:
                                limit = 50 if(analysis['pH'] < 7 and analysis['Temperature'] > 35) else 200
                                if(analysis["Chloride"] < limit):
                                    chlorideRes["Risk"] = "Acceptable"
                                    chlorideRes["Treatment"] = "No Treatment"
                                else:
                                    
                                    chlorideRes["Risk"] = "Unacceptable"
                                    chlorideRes["Treatment"] = "Water treatment for chloride removal such as reverse osmosis"
                                chlorideRes['Index'] = round(analysis["Chloride"], 2)
                                chlorideRes["Description"] = "-"
                                
                                Corrosion["Chloride Concentration (mg/l)"] = chlorideRes
                            except Exception as e:
                                print(f"Error Chloride Corrosion 304 {e}")
                                
                            
                            #Pitting Temperature
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
                                Corrosion["Pitting Temperature"] = PittingRes  
                            except Exception as e:
                                print(f'Error Pitting Temperature 304 {e}')
                                
                        elif(self.material == "Stainless steel 316/316L" ):
                            prenRes["Index"] = 25
                            prenRes["Description"] = "Low sea water resistance"
                            prenRes["Risk"] = "Unacceptable"
                            prenRes["Treatment"] = """ Treatment recommended - 
                                Consider a higher PREN alloy for use\nOR\nAddition of chemical corrosion inhibitors"""

                            #Chloride Concentration
                            try:
                                limit = 100 if(analysis['pH'] < 7 and analysis['Temperature'] > 35) else 300
                                if(analysis["Chloride"] < limit):
                                    chlorideRes["Risk"] = "Acceptable"
                                    chlorideRes["Treatment"] = "No Treatment"
                                else:
                                    
                                    chlorideRes["Risk"] = "Unacceptable"
                                    chlorideRes["Treatment"] = "Water treatment for chloride removal such as reverse osmosis"
                                chlorideRes['Index'] = round(analysis["Chloride"], 2)
                                chlorideRes["Description"] = "-"
                                Corrosion["Chloride Concentration (mg/l)"] = chlorideRes
                            except Exception as e:
                                print(f"Error Chloride Corrosion 316 {e}")
                                
                            #Pitting Temperature
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
                                Corrosion["Pitting Temperature"] = PittingRes  
                            except Exception as e:
                                print(f'Error Pitting Temperature 304 {e}')
                                
                        elif(self.material == "Stainless steel Alloy 20"):
                            prenRes["Index"] = 30
                            prenRes["Description"] = "Low sea water resistance"
                            prenRes["Risk"] = "Unacceptable"
                            prenRes["Treatment"] = """Treatment recommended - 
                                Consider a higher PREN alloy for use\nOR\nAddition of chemical corrosion inhibitors"""

                            #Chloride Concentration
                            try:
                                limit = 150 if(analysis['pH'] < 7 and analysis['Temperature'] > 35) else 400
                                if(analysis["Chloride"] < limit):
                                    chlorideRes["Risk"] = "Acceptable"
                                    chlorideRes["Treatment"] = "No Treatment"
                                else:
                                    
                                    chlorideRes["Risk"] = "Unacceptable"
                                    chlorideRes["Treatment"] = "Water treatment for chloride removal such as reverse osmosis"
                                chlorideRes['Index'] = round(analysis["Chloride"], 2)
                                chlorideRes["Description"] = "-"
                                
                                Corrosion["Chloride Concentration (mg/l)"] = chlorideRes
                            except Exception as e:
                                print(f"Error Chloride Corrosion Aloy 20 {e}")
                                
                            #Pitting Temperature
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
                                Corrosion["Pitting Temperature"] = PittingRes  
                            except Exception as e:
                                print(f'Error Pitting Temperature 304 {e}')
                                
                        elif(self.material == "Stainless steel 904L"):
                            prenRes["Index"] = 36
                            prenRes["Description"] = "Sea water resistance"
                            prenRes["Risk"] = "Acceptable"
                            prenRes["Treatment"] = "No Treatment"

                            #Chloride Concentration
                            try:
                                limit = 2000 if(analysis['pH'] < 7 and analysis['Temperature'] > 35) else 3000
                                if(analysis["Chloride"] < limit):
                                    chlorideRes["Risk"] = "Acceptable"
                                    chlorideRes["Treatment"] = "No Treatment"
                                else:
                                    
                                    chlorideRes["Risk"] = "Unacceptable"
                                    chlorideRes["Treatment"] = "Water treatment for chloride removal such as reverse osmosis"
                                chlorideRes['Index'] = round(analysis["Chloride"], 2)
                                chlorideRes["Description"] = "-"
                                
                                Corrosion["Chloride Concentration (mg/l)"] = chlorideRes
                            except Exception as e:
                                print(f"Error Chloride Corrosion 904 {e}")
                                
                            #Pitting Temperature
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
                                Corrosion["Pitting Temperature"] = PittingRes  
                            except Exception as e:
                                print(f'Error Pitting Temperature 304 {e}')
                                
                        elif(self.material == "Duplex Stainless Steel"):
                            prenRes["Index"] = 46
                            prenRes["Description"] = "Sea water resistance with temp > 30°C"
                            prenRes["Risk"] = "Acceptable"
                            prenRes["Treatment"] = "No Treatment"

                            #Chloride Concentration
                            try:
                                limit = 3000 if(analysis['pH'] < 7 and analysis['Temperature'] > 35) else 3600
                                if(analysis["Chloride"] < limit):
                                    chlorideRes["Risk"] = "Acceptable"
                                    chlorideRes["Treatment"] = "No Treatment"
                                else:
                                    
                                    chlorideRes["Risk"] = "Unacceptable"
                                    chlorideRes["Treatment"] = "Water treatment for chloride removal such as reverse osmosis"
                                chlorideRes['Index'] = round(analysis["Chloride"], 2)
                                chlorideRes["Description"] = "-"
                                Corrosion["Chloride Concentration (mg/l)"] = chlorideRes
                            except Exception as e:
                                print(f"Error Chloride Corrosion duplex {e}")
                                
                            #Pitting Temperature
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
                                Corrosion["Pitting Temperature (°C)"] = PittingRes  
                            except Exception as e:
                                print(f'Error Pitting Temperature 304 {e}')
                                 
                    except Exception as e:
                        print("Error Pitting Corrosion: {e}")
                        
                    Corrosion["PREN of Alloy"] = prenRes
                    #-------------------------------End of Corrosion-------------------------------------------------------------------------------------------------------------------
                    results["Corrosion"] = Corrosion
                elif(assessment == "Scaling"):
                    Scaling = {}
                    RyznerRes = {}
                    silicaSteamRes = {}
                    magnesiumSilicaRes = {}
                    calciumSulphateRes = {}


                    #------------------------------------------------------Ryzner for Scaling---------------------------
                    if(analysis['ryzner'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "No scale formation due to CaCO3"
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = "No Treatment"
                    elif(analysis['ryzner'] < 6.8 and analysis['ryzner'] >= 6.2):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Moderate Scale Formation due to CaCO3"
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""
                    elif(analysis['ryzner'] < 6.2 and analysis['ryzner'] >= 5.5):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Mild Scale Formation due to CaCO3"
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""
                    else:
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Severe Scale Formation due to CaCO3"
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""
                    Scaling["Ryzner Index"] = RyznerRes
                    #-----------------------------------------------------Silica Concentration in Steam-----------------------
                    try:
                        if(analysis["Silica Concentration in steam"] <= 0.02):
                            silicaSteamRes["Index"] = round(analysis["Silica Concentration in steam"],2)
                            silicaSteamRes["Description"] = "Minimal silica film formation"
                            silicaSteamRes["Risk"] = "Ideal"
                            silicaSteamRes["Treatment"] = "No Treatment"
                        else:
                            silicaSteamRes["Index"] = round(analysis["Silica Concentration in steam"],2)
                            silicaSteamRes["Description"] = "High silica film formation"
                            silicaSteamRes["Risk"] = "Tolerable"
                            silicaSteamRes["Treatment"] = """Treatment Recommended - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for silica removal"""
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
                            magnesiumSilicaRes['Treatment'] = """ Treatment recommended - Chemical treatment through addition of Antisca\nOR\nWater treatment for softening and/or silica removal required"""

                        magnesiumSilicaRes["Index"] = None
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
                            calciumSulphateRes["Treatment"] = "-"
                        calciumSulphateRes["Index"] = None
                        Scaling["Calcium Sulphate Scale Formation"] = calciumSulphateRes
                    except Exception as e:
                        print(f"Error Calcium Sulphate SS: {e}")    
                    results["Scaling"] = Scaling
                elif(assessment == "Fouling"):
                    Fouling = {}
                    ssFoulRes = {}
                    if(analysis['Suspended Solids'] >= 30):
                        ssFoulRes["Description"] = "High Chance of Fouling"
                        ssFoulRes["Risk"] = "Unacceptable"
                        ssFoulRes["Treatment"] = "Treatment Recommended - Upfront filtration pre-treatment "
                    elif(analysis['Suspended Solids'] < 30 and analysis['Suspended Solids'] >= 15):
                        ssFoulRes["Description"] = "Moderate Fouling"
                        ssFoulRes["Risk"] = "Tolerable"
                        ssFoulRes["Treatment"] = """Treatment May Be Needed - Upfront filtration pre-treatment\nOR\nChemical treatment by addition of dispersants"""
                    elif(analysis['Suspended Solids'] < 15 and analysis['Suspended Solids'] >= 5):
                        ssFoulRes["Description"] = "Mild of Fouling"
                        ssFoulRes["Risk"] = "Acceptable"
                        ssFoulRes["Treatment"] = """Treatment May Be Needed - Upfront filtration pre-treatment\nOR\nChemical treatment by addition of dispersants"""
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
                    Corrosion = {}
                    RyznerRes = {}
                    LarsonRes = {}
                    PisiganRes = {}
                    #------------------------------------------------------Corrosion Ryzner-------------------------------------
                    if(analysis['ryzner'] >= 8.5):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Severe Corrosion due to lack of CaCO3 formation"
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] = """Chemical Treatment Recommended - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    elif(analysis['ryzner'] < 8.5 and analysis['ryzner'] >= 7.8):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Mild Corrosion due to lack of CaCO3 formation "
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    elif(analysis['ryzner'] < 7.8 and analysis['ryzner'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Mild Corrosion due to lack of CaCO3 formation "
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    else:
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Minimal to no corrosion "
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = "No Treatment"
                    Corrosion["Ryzner Index"] = RyznerRes

                    #------------------------------------------------------Corrosion Larson--------------------------------------
                    if(analysis['larson'] >= 1.2):
                        LarsonRes["Description"] = "Severe pitting corrosion"
                        LarsonRes["Risk"] = "Unacceptable"
                        LarsonRes["Treatment"] = """Treatment Recommended - Water treatment to reduce the sulphate or chloride concentration\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    elif(analysis['larson'] < 1.2 and analysis['larson'] >= 1):
                        LarsonRes["Description"] = "Significant pitting corrosion"
                        LarsonRes["Risk"] = "Tolerable"
                        LarsonRes["Treatment"] = """Treatment May Be Needed - Water treatment to reduce the sulphate or chloride concentration\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    elif(analysis['larson'] < 1 and analysis['larson'] >= 0.8):
                        LarsonRes["Description"] = "Mild pitting corrosion"
                        LarsonRes["Risk"] = "Acceptable"
                        LarsonRes["Treatment"] = """Treatment May Be Needed - Water treatment to reduce the sulphate or chloride concentration\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    else:
                        LarsonRes["Description"] = "Minimal risk of pitting corrosion"
                        LarsonRes["Risk"] = "Ideal"
                        LarsonRes["Treatment"] = "No Treatment"
                    LarsonRes["Index"] = round(analysis["larson"],2)
                    Corrosion['Larson Index'] = LarsonRes

                    #---------------------------------------------------------Corrosion Pisigan----------------------------------------
                    try:
                        if(analysis['reticulation']):
                            if(analysis['pisigan corrosion'] > 10):
                                PisiganRes["Description"] = "High corrosion rate - Severe corrosion will be experienced"
                                PisiganRes["Risk"] = "Unacceptable"
                                PisiganRes["Treatment"] = """Treatment Recommended - Treatment through addition of corrosion inhibitors\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                            elif(analysis['pisigan corrosion'] <= 10 and analysis['pisigan corrosion'] > 5):
                                PisiganRes["Description"] = "Intermediate corrosion rate - Moderate corrosion may be experienced"
                                PisiganRes["Risk"] = "Tolerable"
                                PisiganRes["Treatment"] = """Treatment may be needed - Treatment through addition of corrosion inhibitors\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                            elif(analysis['pisigan corrosion'] <= 5 and analysis['pisigan corrosion'] >= 1):
                                PisiganRes["Description"] = "Intermediate corrosion rate - Mild corrosion may be experienced"
                                PisiganRes["Risk"] = "Acceptable"
                                PisiganRes["Treatment"] = """Treatment may be needed - Treatment through addition of corrosion inhibitors\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                            else:
                                PisiganRes["Description"] = "Low corrosion rate - Minimal corrosion experienced"
                                PisiganRes["Risk"] = "Ideal"
                                PisiganRes["Treatment"] = "No Treatment"
                        else:
                            if(analysis['pisigan corrosion'] > 1):
                                PisiganRes["Description"] = "High corrosion rate - Severe corrosion will be experienced"
                                PisiganRes["Risk"] = "Unacceptable"
                                PisiganRes["Treatment"] = """Treatment Recommended - Treatment through addition of corrosion inhibitors\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                            elif(analysis['pisigan corrosion'] <= 1 and analysis['pisigan corrosion'] >= 0.5):
                                PisiganRes["Description"] = "Intermediate corrosion rate - Moderate corrosion may be experienced"
                                PisiganRes["Risk"] = "Tolerable"
                                PisiganRes["Treatment"] = """Treatment may be needed - Treatment through addition of corrosion inhibitors\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                            elif(analysis['pisigan corrosion'] < 0.5 and analysis['pisigan corrosion'] >= 0.2):
                                PisiganRes["Description"] = "Intermediate corrosion rate - Mild corrosion may be experienced"
                                PisiganRes["Risk"] = "Acceptable"
                                PisiganRes["Treatment"] = """Treatment may be needed - Treatment through addition of corrosion inhibitors\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                            else:
                                PisiganRes["Description"] = "Low corrosion rate - Minimal corrosion experienced"
                                PisiganRes["Risk"] = "Ideal"
                                PisiganRes["Treatment"] = "No treatment"
                        PisiganRes["Index"] = round(analysis['pisigan corrosion'], 2)
                        Corrosion["Corrosion Rate due to the Pisigan and Shingley Correlation (mmpy)"] = PisiganRes
                    except KeyError as e:
                        print("Error For corrosion Rate :{e}")
                    
                    #-------------------------------End of Corrosion-------------------------------------------------------------------------------------------------------------------
                    results["Corrosion"] = Corrosion
                elif(assessment == "Scaling"):
                    Scaling = {}
                    RyznerRes = {}
                    silicaSteamRes = {}
                    magnesiumSilicaRes = {}
                    calciumSulphateRes = {}


                    #------------------------------------------------------Ryzner for Scaling---------------------------
                    if(analysis['ryzner'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "No scale formation due to CaCO3"
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = "No Treatment"
                    elif(analysis['ryzner'] < 6.8 and analysis['ryzner'] >= 6.2):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Moderate Scale Formation due to CaCO3"
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""
                    elif(analysis['ryzner'] < 6.2 and analysis['ryzner'] >= 5.5):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Mild Scale Formation due to CaCO3"
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""
                    else:
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Severe Scale Formation due to CaCO3"
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""
                    Scaling["Ryzner Index"] = RyznerRes
                    #-----------------------------------------------------Silica Concentration in Steam-----------------------
                    try:
                        if(analysis["Silica Concentration in steam"] <= 0.02):
                            silicaSteamRes["Index"] = analysis["Silica Concentration in steam"]
                            silicaSteamRes["Description"] = "Minimal silica film formation"
                            silicaSteamRes["Risk"] = "Ideal"
                            silicaSteamRes["Treatment"] = "No Treatment"
                        else:
                            silicaSteamRes["Index"] = analysis["Silica Concentration in steam"]
                            silicaSteamRes["Description"] = "High silica film formation"
                            silicaSteamRes["Risk"] = "Tolerable"
                            silicaSteamRes["Treatment"] = """Treatment Recommended - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for silica removal"""
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
                            magnesiumSilicaRes['Treatment'] = "No Treatment"
                        else:
                            magnesiumSilicaRes['Description'] = "Unacceptable Magnesium Silicate Scaling"
                            magnesiumSilicaRes['Risk'] = "Unacceptable"
                            magnesiumSilicaRes['Treatment'] = """Chemical treatment through addition of Antiscalants
                   \nOR\nWater treatment for softening and/or silica removal required"""

                        magnesiumSilicaRes["Index"] = None
                        Scaling["Magnesium Silicate Scale Formation"] = magnesiumSilicaRes
                    except Exception as e:
                        print(f'Error magnesium * silica SS : {e}')
                    #-------------------------------------------------------Calcium Sulphate------------------------------------------------
                    try:
                        calSulLimit = 10000000 if(analysis['WaterTreatment'] == True) else 50000
                        if(analysis["CalciumSulphate"] < calSulLimit):
                            calciumSulphateRes["Description"] = "Acceptable Calcium Sulphate Scaling"
                            calciumSulphateRes["Risk"] = "Acceptable"
                            calciumSulphateRes["Treatment"] = "No Treatment"
                        else:
                            calciumSulphateRes["Description"] = "Unacceptable Calcium Sulphate Scaling"
                            calciumSulphateRes["Risk"] = "Unacceptable"
                            calciumSulphateRes["Treatment"] = """Treatment recommended - Chemical treatment through addition of Antiscal\nOR\nWater treatment for softenining required"""
                        calciumSulphateRes["Index"] = None
                        Scaling["Calcium Sulphate Scale Formation"] = calciumSulphateRes
                    except Exception as e:
                        print(f"Error Calcium Sulphate SS: {e}")    
                    results["Scaling"] = Scaling
                elif(assessment == "Fouling"):
                    Fouling = {}
                    ssFoulRes = {}
                    if(analysis['Suspended Solids'] >= 30):
                        ssFoulRes["Description"] = "High Chance of Fouling"
                        ssFoulRes["Risk"] = "Unacceptable"
                        ssFoulRes["Treatment"] = "Treatment Recommended - Upfront filtration pre-treatment"
                    elif(analysis['Suspended Solids'] < 30 and analysis['Suspended Solids'] >= 15):
                        ssFoulRes["Description"] = "Moderate Fouling"
                        ssFoulRes["Risk"] = "Tolerable"
                        ssFoulRes["Treatment"] = """Treatment May Be Needed - Upfront filtration pre-treatment\nOR\nChemical treatment by addition of dispersants"""
                    elif(analysis['Suspended Solids'] < 15 and analysis['Suspended Solids'] >= 5):
                        ssFoulRes["Description"] = "Mild of Fouling"
                        ssFoulRes["Risk"] = "Acceptable"
                        ssFoulRes["Treatment"] = """Treatment May Be Needed - Upfront filtration pre-treatment\nOR\nChemical treatment by addition of dispersants"""
                    else:
                        ssFoulRes["Description"] = "No Fouling predicted"
                        ssFoulRes["Risk"] = "Ideal"
                        ssFoulRes["Treatment"] = "No treatment"
                    
                    ssFoulRes['Index'] = analysis["Suspended Solids"]
                    Fouling["Suspended Solids Fouling (mg/l)"] = ssFoulRes
                    results["Fouling"] = Fouling   
        elif(self.material == "Concrete"):
            for assessment in self.assessments:
                if(assessment == "Corrosion"):
                    Corrosion = {}
                    RyznerRes = {}
                    AggressiveRes = {}
                    #------------------------------------------------------Corrosion Ryzner-------------------------------------
                    if(analysis['ryzner'] >= 8.5):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Severe Corrosion"
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] = """Chemical Treatment Recommended - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    elif(analysis['ryzner'] < 8.5 and analysis['ryzner'] >= 7.8):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Mild Corrosion"
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    elif(analysis['ryzner'] < 7.8 and analysis['ryzner'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Mild Corrosion"
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    else:
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Balanced No Corrosion"
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = "No Treatment"
                    Corrosion["Ryzner Index"] = RyznerRes

                    #----------------------------------------------------------Corrosion Aggressive-------------------------------------
                    try:
                        if(analysis["Concrete Reinforced"]):
                            if(analysis["Aggressive"] >= 12):
                                AggressiveRes["Description"] = "Non aggressive, Lack of pitting corrosion of the concrete reinforced bars"
                                AggressiveRes["Risk"] = "Ideal"
                                AggressiveRes["Treatment"] = "No Treatment"
                            elif(analysis["Aggressive"] < 12 and analysis["Aggressive"] >= 11):
                                AggressiveRes["Description"] = "Moderately aggressive, Moderate pitting corrosion of the concrete reinforced bars"
                                AggressiveRes["Risk"] = "Acceptable"
                                AggressiveRes["Treatment"] = """"Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softening"""
                            elif(analysis["Aggressive"] < 11 and analysis["Aggressive"] >= 10):
                                AggressiveRes["Description"] = "Mildly aggressive, Mild pitting corrosion of the concrete reinforced bars"
                                AggressiveRes["Risk"] = "Ideal"
                                AggressiveRes["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softening"""
                            else:
                                AggressiveRes["Description"] = "Very aggressive, Severe pitting corrosion of the concrete reinforced bars"
                                AggressiveRes["Risk"] = "Unacceptable"
                                AggressiveRes["Treatment"] = """Treatment Recommended - Treatment recommended - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softening"""
                            AggressiveRes["Index"] = round(analysis["Aggressive"],2)
                            Corrosion["Aggressive Index"] = AggressiveRes
                    except Exception as e:
                        print(f"Error Aggressive in Concrete: {e}")
                    
                    #-------------------------------End of Corrosion-------------------------------------------------------------------------------------------------------------------
                    results["Corrosion"] = Corrosion
                elif(assessment == "Scaling"):
                    Scaling = {}
                    RyznerRes = {}
                    sulphateAttackRez = {}

                    #--------------------------------------------------------------------Ryzner for scaling------------------------------------------
                    if(analysis['ryzner'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "No scale formation due to CaCO3"
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = "No Treatment"
                    elif(analysis['ryzner'] < 6.8 and analysis['ryzner'] >= 6.2):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Moderate Scale Formation due to CaCO3"
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required """
                    elif(analysis['ryzner'] < 6.2 and analysis['ryzner'] >= 5.5):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Mild Scale Formation due to CaCO3"
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required """
                    else:
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Severe Scale Formation due to CaCO3"
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required """
                    Scaling["Ryzner Index"] = RyznerRes

                    #-------------------------------------------------------------------Sulpahate attack Scaling--------------------------------------------
                    if(analysis['Sulphate'] >= 10000):
                        sulphateAttackRez["Description"] = "Very severe risk of sulphate attack"
                        sulphateAttackRez["Risk"] = "Unacceptable"
                        sulphateAttackRez["Treatment"] = "Treatment Recommended - Water treatment for sulphate removal "
                    elif(analysis["Sulphate"] < 10000 and analysis["Sulphate"] >= 1500 ):
                        sulphateAttackRez["Description"] = "Severe risk of sulphate attack"
                        sulphateAttackRez["Risk"] = "Unacceptable"
                        sulphateAttackRez["Treatment"] = "Treatment Recommended - Water treatment for sulphate removal "
                    elif(analysis["Sulphate"] < 1500 and analysis["Sulphate"] >= 150):
                        sulphateAttackRez["Description"] = "Moderate risk of sulphate attack"
                        sulphateAttackRez["Risk"] = "Tolerable"
                        sulphateAttackRez["Treatment"] = "Treatment May Be Needed - Water treatment for sulphate removal "
                    else:
                        sulphateAttackRez["Description"] = "Low risk of sulphate attack"
                        sulphateAttackRez["Risk"] = "Ideal"
                        sulphateAttackRez["Treatment"] = "No Treatment" 
                    sulphateAttackRez["Index"] = analysis["Sulphate"]
                    Scaling["Sulphate attack"] = sulphateAttackRez
                    results["Scaling"] = Scaling
                elif(assessment == "Fouling"):
                    Fouling = {}
                    ssFoulRes = {}
                    if(analysis['Suspended Solids'] >= 30):
                        ssFoulRes["Description"] = "High Chance of Fouling"
                        ssFoulRes["Risk"] = "Unacceptable"
                        ssFoulRes["Treatment"] = "Treatment Recommended - Upfront filtration pre-treatment "
                    elif(analysis['Suspended Solids'] < 30 and analysis['Suspended Solids'] >= 15):
                        ssFoulRes["Description"] = "Moderate Fouling"
                        ssFoulRes["Risk"] = "Tolerable"
                        ssFoulRes["Treatment"] = """Treatment May Be Needed - Upfront filtration pre-treatment\nOR\nChemical treatment by addition of dispersants"""
                    elif(analysis['Suspended Solids'] < 15 and analysis['Suspended Solids'] >= 5):
                        ssFoulRes["Description"] = "Mild of Fouling"
                        ssFoulRes["Risk"] = "Acceptable"
                        ssFoulRes["Treatment"] = """Treatment May Be Needed - Upfront filtration pre-treatment\nOR\nChemical treatment by addition of dispersants"""
                    else:
                        ssFoulRes["Description"] = "No Fouling predicted"
                        ssFoulRes["Risk"] = "Ideal"
                        ssFoulRes["Treatment"] = "No treatment"
                    
                    ssFoulRes['Index'] = analysis["Suspended Solids"]
                    Fouling["Suspended Solids Fouling (mg/l)"] = ssFoulRes
                    results["Fouling"] = Fouling
        elif(self.material == "Monel-Lead/Copper Alloys"):
            for assessment in self.assessments:
                if(assessment == "Corrosion"):
                    Corrosion = {}
                    RyznerRes = {}
                    LarsonRes = {}
                    AggressiveRes = {}
                    csmr = {}
                    prenRes = {}
                    #------------------------------------------------------Corrosion Ryzner-------------------------------------
                    if(analysis['ryzner'] >= 8.5):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Severe Corrosion due to lack of CaCO3 formation "
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] =  """Chemical Treatment Recommended - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    elif(analysis['ryzner'] < 8.5 and analysis['ryzner'] >= 7.8):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Mild Corrosion due to lack of CaCO3 formation "
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    elif(analysis['ryzner'] < 7.8 and analysis['ryzner'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Mild Corrosion due to lack of CaCO3 formation "
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    else:
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Minimal to no corrosion"
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = "No Treatment"
                    Corrosion["Ryzner Index"] = RyznerRes
                    
                    #--------------------------------------------------------Chloride to Sulphate MAss Ratio-----------------------------
                    try:
                        if(analysis["Lead or Copper"]):
                            if(analysis["csmr"] > 0.5):
                                csmr["Index"] = round(analysis["csmr"],2)
                                csmr["Description"] = "Significant corrosion risk and lead exposure"
                                csmr["Risk"] = "Unacceptable"
                                csmr['Treatment'] = "Treatment recommended - Water treatment to remove the chloride and sulphate concentration "
                            else:
                                csmr["Index"] = round(analysis["csmr"],2)
                                csmr["Description"] = "Minimal corrosion risk"
                                csmr["Risk"] = "Ideal"
                                csmr['Treatment'] = "No Treatment"
                            Corrosion["Chloride to Sulphate Mass Ratio "] = csmr
                    except Exception as e:
                        print(f"Error CSMR :{e}")

                    #-----------------------------------------------------------Larson Alloys------------------------------------------------
                    if(analysis['larson'] >= 1.2):
                        LarsonRes["Description"] = "Severe corrosion"
                        LarsonRes["Risk"] = "Unacceptable"
                        LarsonRes["Treatment"] = """Treatment Recommended - Water treatment to reduce the sulphate or chloride concentration\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    elif(analysis['larson'] < 1.2 and analysis['larson'] >= 1):
                        LarsonRes["Description"] = "Significant corrosion"
                        LarsonRes["Risk"] = "Tolerable"
                        LarsonRes["Treatment"] = """Treatment May Be Needed - Water treatment to reduce the sulphate or chloride concentration\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    elif(analysis['larson'] < 1 and analysis['larson'] >= 0.8):
                        LarsonRes["Description"] = "Mild corrosion"
                        LarsonRes["Risk"] = "Acceptable"
                        LarsonRes["Treatment"] = """Treatment May Be Needed - Water treatment to reduce the sulphate or chloride concentration\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    else:
                        LarsonRes["Description"] = "Non corrosive water"
                        LarsonRes["Risk"] = "Ideal"
                        LarsonRes["Treatment"] = "No Treatment"
                    LarsonRes["Index"] = round(analysis["larson"],2)
                    Corrosion['Larson Index'] = LarsonRes

                    #--------------------------------------------------------------Add PREN ALLOYS---------------------------------
                    try:
                        if(analysis['PREN'] <= 35):
                            prenRes["Description"] = "-"
                            prenRes["Risk"] = "Unacceptable"
                            prenRes["Treatment"] = """Treatment recommended - 
                                Consider a higher PREN alloy for use\nOR\nAddition of chemical corrosion inhibitors"""
                        elif(analysis['PREN'] > 35 and analysis["PREN"] <= 40):
                            prenRes["Description"] = "Sea water resistance"
                            prenRes["Risk"] = "Acceptable"
                            prenRes["Treatment"] = """No Treatment"""
                        elif(analysis["PREN"] > 40 and analysis["PREN"] <= 45):
                            prenRes["Description"] = "Sea water resistance with temperature >30°C"
                            prenRes["Risk"] = "Acceptable"
                            prenRes["Treatment"] = """No Treatment"""
                        else:
                            prenRes["Description"] = "Crevice corrosion resistance"
                            prenRes["Risk"] = "Acceptable"
                            prenRes["Treatment"] = """No Treatment"""
                        
                        prenRes["Index"] = round(analysis['PREN'],2)
                        Corrosion["PREN of Alloy"] = prenRes
                    except Exception as e:
                        print(f"Error PREN for Alloys: {e}")
                    #End Corosion-------------------------------------------------------------------------
                    results["Corrosion"] = Corrosion
                elif(assessment == "Scaling"):
                    Scaling = {}
                    RyznerRes = {}
                    silicaSteamRes = {}
                    magnesiumSilicaRes = {}
                    calciumSulphateRes = {}


                    #------------------------------------------------------Ryzner for Scaling---------------------------
                    if(analysis['ryzner'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "No scale formation due to CaCO3"
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = "No Treatment"
                    elif(analysis['ryzner'] < 6.8 and analysis['ryzner'] >= 6.2):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Moderate Scale Formation due to CaCO3"
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""
                    elif(analysis['ryzner'] < 6.2 and analysis['ryzner'] >= 5.5):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Mild Scale Formation due to CaCO3"
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""
                    else:
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Severe Scale Formation due to CaCO3"
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""
                    Scaling["Ryzner Index"] = RyznerRes
                    #-----------------------------------------------------Silica Concentration in Steam-----------------------
                    try:
                        if(analysis["Silica Concentration in steam"] <= 0.02):
                            silicaSteamRes["Index"] = round(analysis["Silica Concentration in steam"],2)
                            silicaSteamRes["Description"] = "Minimal silica film formation"
                            silicaSteamRes["Risk"] = "Ideal"
                            silicaSteamRes["Treatment"] = "No Treatment"
                        else:
                            silicaSteamRes["Index"] = round(analysis["Silica Concentration in steam"],2)
                            silicaSteamRes["Description"] = "High silica film formation"
                            silicaSteamRes["Risk"] = "Tolerable"
                            silicaSteamRes["Treatment"] =  """Treatment Recommended - Chemical treatment through addition of Antiscalant\nOR\nWater treatment for silica removal"""
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
                            magnesiumSilicaRes['Treatment'] = "No Treatment"
                        else:
                            magnesiumSilicaRes['Description'] = "Unacceptable Magnesium Silicate Scaling"
                            magnesiumSilicaRes['Risk'] = "Unacceptable"
                            magnesiumSilicaRes['Treatment'] = """Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softening and/or silica removal required"""

                        magnesiumSilicaRes["Index"] = None
                        Scaling["Magnesium Silicate Scale Formation"] = magnesiumSilicaRes
                    except Exception as e:
                        print(f'Error magnesium * silica SS : {e}')
                    #-------------------------------------------------------Calcium Sulphate------------------------------------------------
                    try:
                        calSulLimit = 10000000 if(analysis['WaterTreatment'] == True) else 50000
                        
                        if(analysis["CalciumSulphate"] < calSulLimit):
                            calciumSulphateRes["Description"] = "Acceptable Calcium Sulphate Scaling"
                            calciumSulphateRes["Risk"] = "Acceptable"
                            calciumSulphateRes["Treatment"] = "No Treatment"
                        else:
                            calciumSulphateRes["Description"] = "Unacceptable Calcium Sulphate Scaling"
                            calciumSulphateRes["Risk"] = "Unacceptable"
                            calciumSulphateRes["Treatment"] = """Treatment recommended - Chemical treatment through addition of Antiscal\nOR\nWater treatment for softenining required"""
                        calciumSulphateRes["Index"] = None
                        Scaling["Calcium Sulphate Scale Formation"] = calciumSulphateRes
                    except Exception as e:
                        print(f"Error Calcium Sulphate SS: {e}")    
                    results["Scaling"] = Scaling
                elif(assessment == "Fouling"):
                    Fouling = {}
                    ssFoulRes = {}
                    if(analysis['Suspended Solids'] >= 30):
                        ssFoulRes["Description"] = "High Chance of Fouling"
                        ssFoulRes["Risk"] = "Unacceptable"
                        ssFoulRes["Treatment"] = "Treatment Recommended - Upfront filtration pre-treatment "
                    elif(analysis['Suspended Solids'] < 30 and analysis['Suspended Solids'] >= 15):
                        ssFoulRes["Description"] = "Moderate Fouling"
                        ssFoulRes["Risk"] = "Tolerable"
                        ssFoulRes["Treatment"] = """Treatment May Be Needed - Upfront filtration pre-treatment\nOR\nChemical treatment by addition of dispersants"""
                    elif(analysis['Suspended Solids'] < 15 and analysis['Suspended Solids'] >= 5):
                        ssFoulRes["Description"] = "Mild of Fouling"
                        ssFoulRes["Risk"] = "Acceptable"
                        ssFoulRes["Treatment"] = """Treatment May Be Needed - Upfront filtration pre-treatment\nOR\nChemical treatment by addition of dispersants"""
                    else:
                        ssFoulRes["Description"] = "No Fouling predicted"
                        ssFoulRes["Risk"] = "Ideal"
                        ssFoulRes["Treatment"] = "No treatment"
                    
                    ssFoulRes['Index'] = analysis["Suspended Solids"]
                    Fouling["Suspended Solids Fouling (mg/l)"] = ssFoulRes
                    results["Fouling"] = Fouling   
        elif(self.material == "Plastic"):
            for assessment in self.assessments:
                if(assessment == "Scaling"):
                    Scaling = {}
                    RyznerRes = {}
                    #------------------------------------------------------Ryzner for Scaling---------------------------
                    if(analysis['ryzner'] >= 6.8):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Minimal to no corrosion"
                        RyznerRes["Risk"] = "Ideal"
                        RyznerRes["Treatment"] = "No Treatment"
                    elif(analysis['ryzner'] < 6.8 and analysis['ryzner'] >= 6.2):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Mild Corrosion due to lack of CaCO3 formation "
                        RyznerRes["Risk"] = "Acceptable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""
                    elif(analysis['ryzner'] < 6.2 and analysis['ryzner'] >= 5.5):
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Mild Corrosion due to lack of CaCO3 formation "
                        RyznerRes["Risk"] = "Tolerable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""
                    else:
                        RyznerRes["Index"] = round(analysis['ryzner'], 2)
                        RyznerRes["Description"] = "Severe Corrosion due to lack of CaCO3 formation "
                        RyznerRes["Risk"] = "Unacceptable"
                        RyznerRes["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""
                    Scaling["Ryzner Index"] = RyznerRes
                    results["Scaling"] = Scaling
                elif(assessment == "Fouling"):
                    Fouling = {}
                    ssFoulRes = {}
                    if(analysis['Suspended Solids'] >= 30):
                        ssFoulRes["Description"] = "High Chance of Fouling"
                        ssFoulRes["Risk"] = "Unacceptable"
                        ssFoulRes["Treatment"] = "Treatment Recommended - Upfront filtration pre-treatment"
                    elif(analysis['Suspended Solids'] < 30 and analysis['Suspended Solids'] >= 15):
                        ssFoulRes["Description"] = "Moderate Fouling"
                        ssFoulRes["Risk"] = "Tolerable"
                        ssFoulRes["Treatment"] = """Treatment May Be Needed - Upfront filtration pre-treatment\nOR\nChemical treatment by addition of dispersants"""
                    elif(analysis['Suspended Solids'] < 15 and analysis['Suspended Solids'] >= 5):
                        ssFoulRes["Description"] = "Mild of Fouling"
                        ssFoulRes["Risk"] = "Acceptable"
                        ssFoulRes["Treatment"] = """Treatment May Be Needed - Upfront filtration pre-treatment\nOR\nChemical treatment by addition of dispersants"""
                    else:
                        ssFoulRes["Description"] = "No Fouling predicted"
                        ssFoulRes["Risk"] = "Ideal"
                        ssFoulRes["Treatment"] = "No treatment"
                    
                    ssFoulRes['Index'] = analysis["Suspended Solids"]
                    Fouling["Suspended Solids Fouling (mg/l)"] = ssFoulRes
                    results["Fouling"] = Fouling 
        elif(self.material == "Membranes"):
            for assessment in self.assessments:
                if(assessment == "Corrosion"):
                    Corrosion = {}
                    langlierRes = {}
                    if(analysis["Langlier"] >= 5):
                        langlierRes["Description"] = "Severe Corrosion due to CaCO3"
                        langlierRes["Risk"] = "Unacceptable"
                        langlierRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    elif(analysis["Langlier"] < 5 and analysis["Langlier"] >= 2):
                        langlierRes["Description"] = "Mild Corrosion due to CaCO3"
                        langlierRes["Risk"] = "Tolerable"
                        langlierRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""

                    elif(analysis["Langlier"] < 2 and analysis["Langlier"] >= 0.5):
                        langlierRes["Description"] = "Mild Corrosion due to CaCO3"
                        langlierRes["Risk"] = "Acceptable"
                        langlierRes["Treatment"] = """Treatment May Be Needed - Treatment through addition of corrosion inhibitors\nOR\nConsider an alternative Material of Construction\nOR\nConsider additional treatment of the water to more suitable feed quality"""
                    else:
                        langlierRes["Description"] = "Minimal to no risk of corrosion"
                        langlierRes["Risk"] = "Ideal"
                        langlierRes["Treatment"] = "No Treatment"
                    langlierRes["Index"] = round(analysis["Langlier"],2)
                    Corrosion["Langelier Saturation Index"] = langlierRes
                    results["Corrosion"] = Corrosion
                elif(assessment == "Scaling"):
                    Scaling = {}
                    langlierResScaling = {}
                    if(analysis["Langlier"] > 3.5):
                        langlierResScaling["Description"] = "Severe Scale Formation due to CaCO3"
                        langlierResScaling["Risk"] = "Unacceptable"
                        langlierResScaling["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""

                    elif(analysis["Langlier"] <= 3.5 and analysis["Langlier"] > 2):
                        langlierResScaling["Description"] = "Mild Scale Formation due to CaCO3"
                        langlierResScaling["Risk"] = "Tolerable"
                        langlierResScaling["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""

                    elif(analysis["Langlier"] <= 2 and analysis["Langlier"] > 0):
                        langlierResScaling["Description"] = "Moderate Scale Formation due to CaCO3"
                        langlierResScaling["Risk"] = "Acceptable"
                        langlierResScaling["Treatment"] = """Treatment May Be Needed - Chemical treatment through addition of Antiscalants\nOR\nWater treatment for softenining required"""
                    else:
                        langlierResScaling["Description"] = "No scale formation due to CaCO3"
                        langlierResScaling["Risk"] = "Ideal"
                        langlierResScaling["Treatment"] = "No Treatment"
                    langlierResScaling["Index"] = round(analysis["Langlier"],2)
                    Scaling["Langelier Saturation Index"] = langlierResScaling
                    results["Scaling"] = Scaling
                elif(assessment == "Fouling"):
                    Fouling = {}
                    ssFoulRes = {}
                    psRes = {}
                    sdensityRes = {}
                    if(analysis['Suspended Solids'] >= 30):
                        ssFoulRes["Description"] = "High Chance of Fouling"
                        ssFoulRes["Risk"] = "Unacceptable"
                        ssFoulRes["Treatment"] = "Treatment Recommended - Upfront filtration pre-treatment"
                    elif(analysis['Suspended Solids'] < 30 and analysis['Suspended Solids'] >= 15):
                        ssFoulRes["Description"] = "Moderate Fouling"
                        ssFoulRes["Risk"] = "Tolerable"
                        ssFoulRes["Treatment"] = """Treatment May Be Needed - Upfront filtration pre-treatment\nOR\nChemical treatment by addition of dispersants"""
                    elif(analysis['Suspended Solids'] < 15 and analysis['Suspended Solids'] >= 5):
                        ssFoulRes["Description"] = "Mild of Fouling"
                        ssFoulRes["Risk"] = "Acceptable"
                        ssFoulRes["Treatment"] = """Treatment May Be Needed - Upfront filtration pre-treatment\nOR\nChemical treatment by addition of dispersants"""
                    else:
                        ssFoulRes["Description"] = "No Fouling predicted"
                        ssFoulRes["Risk"] = "Ideal"
                        ssFoulRes["Treatment"] = "No treatment"
                    ssFoulRes['Index'] = analysis["Suspended Solids"]

                    #--------------------------------------------------------------------------Fouling Silt Density----------------------
                    try:
                        if(analysis["Silt Density Index"] >= 5):
                            psRes["Description"] = "Several years without collodial fouling"
                            psRes['Risk'] = "Ideal"
                            psRes["Treatment"] = "Treatment not recommended"
                        if(analysis["Silt Density Index"] < 5 and analysis["Silt Density Index"] >= 3):
                            psRes["Description"] = "Several months between cleaning"
                            psRes['Risk'] = "Acceptable"
                            psRes["Treatment"] = "Treatment Recommended - Regular cleaning required"
                        elif(analysis["Silt Density Index"] > 3 and analysis["Silt Density Index"] <= 1):
                            psRes["Description"] = "Particular fouling likely a problem, frequent cleaning"
                            psRes['Risk'] = "Tolerable"
                            psRes["Treatment"] = "Treatment Recommended - Regular cleaning required"
                        else:
                            psRes["Description"] = "Unacceptable, additional pre-treatment is needed"
                            psRes['Risk'] = "Unacceptable"
                            psRes["Treatment"] = "Treatment Required - Additional upfront pre-treatment required"
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
        print(results)
        return results  
#------------------------------------------------------------------------------------------------------- Validation Window--------------------------------------------------------
class ValidationDialog(QDialog,QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.ctx = args[0]
        uic.loadUi(self.ctx.get_validation,self)
        

        self.requiredFrame.hide()
        self.optionalFrame.hide()

        self.buttonBox.addButton("OK", QDialogButtonBox.RejectRole)
        buttonOk = self.buttonBox.buttons()
        buttonOk[0].setStyleSheet(
            """
                QPushButton{
                    padding:7px 42px;border:2px solid rgb(12, 75, 85);background:#fff;color:rgb(12, 75, 85);border-radius:8px;font-size:12px;font-weight:900
                }
                QPushButton:hover{
                    padding:7px 42px;border:2px solid rgb(12, 75, 85);color:#fff;background:rgb(12, 75, 85);border-radius:8px;font-size:12px;font-weight:900
                }
            """
        )

        
        
        
        reqList = []
        optList = []
        for keys,items in args[1].items():
            if(keys == "Required"):
                
                for item in args[1][keys]:
                    dictKeys = list(item.keys())
                    for item in item[dictKeys[0]]:
                        reqList.append(f'<li style="margin:1px 0px">&#8608; {item}</li>')
                
                reqHtml = ''.join(list(set(reqList)))
                labelWidgetRequired = qtw.QLabel(f'<ul style="list-style-type:none">{reqHtml}</ul>')
                labelWidgetRequired.setStyleSheet("font-size:12px")
                self.verticalRequired.addWidget(labelWidgetRequired)
                self.requiredFrame.show()
            else:
                
                for item in args[1][keys]:
                    dictKeys = list(set(item.keys()))
                    for item in item[dictKeys[0]]:
                        optList.append(f'<li style="margin:1px 0px">&#8608; {item}</li>')
                
                optHtml = ''.join(list(set(filter(lambda x: x not in reqList,optList))))
                labelWdgetOptional = qtw.QLabel(f'<ul style="list-style-type:none">{optHtml}</ul>')
                labelWdgetOptional.setStyleSheet("font-size:12px")
                self.verticalOptional.addWidget(labelWdgetOptional)
                self.optionalFrame.show()
                   
        if(self.requiredFrame.isHidden() == True):
            self.buttonBox.clear()
            self.label_3.setText('Proceeding without the parameters marked as Optional will result in a limited assessment.\nClick "Cancel" to return to Inputs Window or click "Proceed" to continue.')
            self.buttonBox.addButton("Cancel", QDialogButtonBox.RejectRole)
            self.buttonBox.addButton("Proceed", QDialogButtonBox.AcceptRole)

            buttonCancel = self.buttonBox.buttons()[1]
            buttonProceed = self.buttonBox.buttons()[0]
            buttonCancel.setStyleSheet(
                """
                    QPushButton{
                        padding:7px 22px;border:2px solid rgb(12, 75, 85);background:#fff;color:rgb(12, 75, 85);border-radius:8px;font-size:12px;font-weight:900
                    }
                    QPushButton:hover{
                        padding:7px 22px;border:2px solid rgb(12, 75, 85);background:#dfdfdf;color:rgb(12, 75, 85);border-radius:8px;font-size:12px;font-weight:900
                    }
                """
            )
            buttonProceed.setStyleSheet(
                """
                    QPushButton{
                        padding:7px 22px;border:2px solid rgb(12, 75, 85);color:#fff;background:rgb(12, 75, 85);border-radius:8px;font-size:12px;font-weight:900
                    }
                    QPushButton:hover{
                        padding:7px 22px;border:2px solid rgb(12, 75, 85);color:#fff;background:#127281;border-radius:8px;font-size:12px;font-weight:900
                    }
                """
            )

        else:
            self.label_3.setText('You did not provided enough data to proceed. Click "OK" to return to the Inputs Window')
            self.label_3.setStyleSheet("color:red;font-weight:900")
            
    def center(self):
        frameGm = self.frameGeometry()
        screen = qtw.QApplication.desktop().screenNumber(qtw.QApplication.desktop().cursor().pos())
        centerPoint = qtw.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())           
class FloatingButtonWidget(qtw.QPushButton):

    def __init__(self, parent):
        super().__init__(parent)
        self.paddingLeft = 228
        self.paddingTop = 103
        self.setText("Background Information")
        self.setMinimumWidth(200)
        self.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))
        self.setStyleSheet("""
            QPushButton{
                        padding:10px 10px;border:1px solid rgba(12, 75, 85, 0.8);color:rgba(12, 75, 85, 1);background:white;border-radius:8px;font-size:12px;font-weight:900
                    }
            QPushButton:hover{
                padding:10px 10px;border:1px solid rgba(12, 75, 85,0.8);color:#fff;background:#127281;border-radius:8px;font-size:12px;font-weight:900
            }
        """)

    def update_position(self):
        try:
            if hasattr(self.parent(), 'viewport'):
                parent_rect = self.parent().viewport().rect()
            else:
                parent_rect = self.parent().rect()

            if not parent_rect:
                return

            x = parent_rect.width() - self.width() - self.paddingLeft
            y = self.paddingTop
            self.setGeometry(x, y, self.width(), self.height())
        except Exception as e:
            print(e)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_position()

    def mousePressEvent(self, event):
        print(event)
#-------------------------------------------------------------------------------------------------------Inputs Window-------------------------------------------------------------


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
        typeText = ""
        for word in args[1]['type']:
            typeText += (" " + word)
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
 
#---------------------------------------------------------------------------------------------------------App Window--------------------------------------------------------------
class AppWindow(QMainWindow):

    updateVisual = qtc.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(AppWindow, self).__init__()
        self.ctx = args[0]
        uic.loadUi(self.ctx.get_appWindow, self)
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.center()
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
        self.label_14.setText("The processing unit refers to the component or unit to be assessed.")

        #Buttons
        self.buttonProceed.clicked.connect(self.SectorValidate)
    
        self.buttonBack.clicked.connect(self.showBack)
        self.buttonUserInfoEdit.clicked.connect(self.editUserInfo)
        self.buttonAbout.clicked.connect(self.showAbout)
        self.buttonSelectAll.clicked.connect(self.selectAll)
        
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
           
    def printPDF(self):
            fn, _ = QFileDialog.getSaveFileName(self, 'Export PDF', None, 'PDF files (.pdf);;All Files()')
            if fn != '':
                try:
                    self.doc.printToPdf(fn)
                    self.updateStatusBar_2("green", f"Successfully saved PDF Report in {fn}")
                except Exception as e:
                    self.updateStatusBar_2("red", f"Failed to save PDF Report")
                    print(e)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
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
            self.buttonCurrentPage1.setEnabled(False)
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

            self.buttonCurrentPage1.setEnabled(False)
            self.buttonCurrentPage2.setEnabled(False)
            self.buttonCurrentPage3.setEnabled(True)
    def selectAll(self):
        if(self.checkBoxCorrosion_2.isEnabled() == True):
            self.checkBoxCorrosion_2.setChecked(True)
        if(self.checkBoxFouling_2.isEnabled() == True):
            self.checkBoxFouling_2.setChecked(True)
        if(self.checkBoxScaling_2.isEnabled() == True):
            self.checkBoxScaling_2.setChecked(True)
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
            self.label_14.setText("The processing unit refers to the component or unit to be assessed.\nNot Lined - Applies to storage units without lining considerations. \nLined - Applies to storage unit that has any lining considerations.")
            
        else:
            
            self.radioButton.hide()
            self.radioButton_2.hide()
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

#----------------------------------------------------------------------------------------- -------------Main Window ---------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self, ctx):
        super(MainWindow, self).__init__()
        self.ctx = ctx
        uic.loadUi(self.ctx.get_main, self)
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        
        #buttons
        self.buttonAdvancedAssess.mouseReleaseEvent = self.showNext
        self.buttonWaterQuality.mouseReleaseEvent = self.showWaterQuality
        self.buttonAbout.clicked.connect(self.showAbout)

        self.buttonNice = FloatingButtonWidget(parent = self.label)
        #Show Window
        #self.show()
        
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = qtc.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    def center(self):
        frameGm = self.frameGeometry()
        screen = qtw.QApplication.desktop().screenNumber(qtw.QApplication.desktop().cursor().pos())
        centerPoint = qtw.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
    def showNext(self,a):
        self.app_window = self.ctx.app_window
        self.app_window.show()
        self.close()
    def showAbout(self):
        self.about_window = self.ctx.about_window
        self.about_window.show()
    def showWaterQuality(self,a):
        self.water_window = self.ctx.water_window
        self.water_window.show()
        self.close()


# See ``pyi_rth_qt5.py`: use a "standard" PyQt5 layout.
if sys.platform == 'darwin':
    # Try PyQt5 5.15.4-style path first...
    pyqt_path = os.path.join(sys._MEIPASS, 'PyQt5', 'Qt5')
    if not os.path.isdir(pyqt_path):
        # ... and fall back to the older version
        pyqt_path = os.path.join(sys._MEIPASS, 'PyQt5', 'Qt')
    os.environ['QTWEBENGINEPROCESS_PATH'] = os.path.normpath(os.path.join(
        pyqt_path, 'lib', 'QtWebEngineCore.framework', 'Helpers',
        'QtWebEngineProcess.app', 'Contents', 'MacOS', 'QtWebEngineProcess'))
if __name__ == '__main__':
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        qtw.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        qtw.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    appctxt = AppContext()       # 1. Instantiate ApplicationContext
    exit_code = appctxt.run()     # 2. Invoke appctxt.app.exec_()

    sys.exit(exit_code)

  