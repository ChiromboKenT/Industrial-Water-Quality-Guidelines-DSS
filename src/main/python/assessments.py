from PyQt5.QtWidgets import QApplication, QDialog,  QLabel, QWidget


from PyQt5 import QtCore, QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import uic
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
