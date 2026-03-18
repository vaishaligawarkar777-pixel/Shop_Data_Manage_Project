from PyQt5.QtWidgets import QMainWindow,QTableWidget,QTableWidgetItem,QMessageBox
from Change_Password.Change_Password import Ui_MainWindow
import sqlite3
class clsChange_Password(QMainWindow):
    def __init__(self):
        super(clsChange_Password,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedHeight(250)
        self.setFixedWidth(390)
        self.ui.cmbusername.setFocus()
        self.conn = sqlite3.connect('DataBase.db')
        self.cursor = self.conn.cursor()
        self.ui.btnchange.clicked.connect(self.changeBtnClick)
        sql = "select * from User_LoginData"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for row in result:
            self.ui.cmbusername.addItem(str(row[1]))

    def changeBtnClick(self):
        sql = f"select * from User_LoginData where UserName='{self.ui.cmbusername.currentText()}'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        oldPass = ""
        for row in result:
            oldPass = str(row[2])
        if self.ui.cmbusername.currentText() != "":
            if self.ui.txtoldpassword.text() == oldPass:
                if self.ui.txtpassword.text() != "":
                    if self.ui.txtpassword.text() == self.ui.txtpassword1.text():

                        UserName = self.ui.cmbusername.currentText()
                        sql = f"update User_LoginData set Password='{self.ui.txtpassword1.text()}',NewPassword='{self.ui.txtpassword1.text()}' where UserName='{self.ui.cmbusername.currentText()}'"
                        self.cursor.execute(sql)
                        self.conn.commit()
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setWindowTitle("Info")
                        msg.setText("Password Change Successfully ")
                        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                        msg.setDefaultButton(QMessageBox.Ok)
                        result = msg.exec_()
                        self.ui.cmbusername.setCurrentText("")
                        self.ui.txtoldpassword.setText("")
                        self.ui.txtpassword.setText("")
                        self.ui.txtpassword1.setText("")
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setWindowTitle("Info")
                        msg.setText("Both Password Must be Same")
                        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                        msg.setDefaultButton(QMessageBox.Ok)
                        result = msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("Info")
                    msg.setText("Password can not be blank Or Old Password Not Match")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    msg.setDefaultButton(QMessageBox.Ok)

            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Info")
                msg.setText("Old Password Not Match")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.setDefaultButton(QMessageBox.Ok)

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Info")
            msg.setText("User Name can not be blank")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Ok)
            result = msg.exec_()


