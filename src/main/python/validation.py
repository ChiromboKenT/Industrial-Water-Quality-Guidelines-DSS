#------------------------------------------------------------------------------------------------------- Validation Window--------------------------------------------------------
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QWidget,QDialogButtonBox,QLabel,QApplication
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
                labelWidgetRequired = QLabel(f'<ul style="list-style-type:none">{reqHtml}</ul>')
                labelWidgetRequired.setStyleSheet("font-size:12px")
                self.verticalRequired.addWidget(labelWidgetRequired)
                self.requiredFrame.show()
            else:
                
                for item in args[1][keys]:
                    dictKeys = list(set(item.keys()))
                    for item in item[dictKeys[0]]:
                        optList.append(f'<li style="margin:1px 0px">&#8608; {item}</li>')
                
                optHtml = ''.join(list(set(filter(lambda x: x not in reqList,optList))))
                labelWdgetOptional = QLabel(f'<ul style="list-style-type:none">{optHtml}</ul>')
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
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())           
