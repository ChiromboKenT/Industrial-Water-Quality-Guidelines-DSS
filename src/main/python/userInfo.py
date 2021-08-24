from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5 import uic
class UserInfo(QDialog,QWidget):
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