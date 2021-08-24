from fbs_runtime.application_context.PyQt5 import ApplicationContext,cached_property
from PyQt5.QtWidgets import QMainWindow, QApplication


from waterQuality import WaterQualityWindow
from license import LicenseWindow
from validation import ValidationDialog
from inputs import InputsWindow
from fitnessForUse import AppWindow
from about import AboutWindow
from assessments import ReportsWindow
from userInfo import UserInfo
from floatingButton import FloatingButtonWidget

import sys
import pandas as pd
from PyQt5.QtCore import Qt,QPoint
from PyQt5.QtGui import QImage
from PyQt5 import uic
import json
import os


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
        return QImage(self.get_resource("images/homeImage.png"))
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

#----------------------------------------------------------------------------------------- -------------Main Window ---------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self, ctx):
        super(MainWindow, self).__init__()
        self.ctx = ctx
        uic.loadUi(self.ctx.get_main, self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
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
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
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
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    appctxt = AppContext()       # 1. Instantiate ApplicationContext
    exit_code = appctxt.run()     # 2. Invoke appctxt.app.exec_()

    sys.exit(exit_code)

  