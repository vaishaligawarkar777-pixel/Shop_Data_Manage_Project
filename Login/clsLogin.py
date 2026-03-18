from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem,QMessageBox
from Login.Login import Ui_MainWindow
import sqlite3
from MainWindow.clsMainWindow import clsMainWindow
class clsLogin(QMainWindow):
    def __init__(self):
        super(clsLogin,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.id=0
        self.setFixedHeight(170)
        self.setFixedWidth(340)
        self.ui.txtusername.setFocus()
        self.ui.btnLogin.clicked.connect(self.LoginBtnClick)
        self.m = clsMainWindow()
    def LoginBtnClick(self):
        conn = sqlite3.connect('DataBase.db')
        cursor = conn.cursor()
        sql = f"select * from User_LoginData where UserName='{self.ui.txtusername.text()}' and Password='{self.ui.txtpassword.text()}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        i = 0
        for row in result:
            i += 1

        if i==0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Info")
            msg.setText("Invalid Username or Password")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Ok)
            result = msg.exec_()
        else:

            self.m.show()
            self.close()
