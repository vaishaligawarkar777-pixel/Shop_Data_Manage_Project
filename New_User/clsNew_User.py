from PyQt5.QtWidgets import QMainWindow,QTableWidget,QTableWidgetItem,QMessageBox
from New_User.New_User import Ui_MainWindow
import sqlite3
class clsNew_User(QMainWindow):
    def __init__(self):
        super(clsNew_User,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedHeight(220)
        self.setFixedWidth(380)
        self.ui.txtusername.setFocus()
        self.conn=sqlite3.connect('DataBase.db')
        self.cursor=self.conn.cursor()
        self.ui.btnregister.clicked.connect(self.RegisterBtnClick)

    def RegisterBtnClick(self):
        if self.ui.txtusername.text()!="":
            if self.ui.txtpassword.text()!="":
                if self.ui.txtpassword.text()==self.ui.txtpassword1.text():

                        sql = f"insert into User_LoginData values(null,'{self.ui.txtusername.text()}','{self.ui.txtpassword.text()}','{self.ui.txtpassword1.text()}')"
                        self.cursor.execute(sql)
                        self.conn.commit()
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setWindowTitle("Info")
                        msg.setText("User Added Successfully ")
                        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                        msg.setDefaultButton(QMessageBox.Ok)
                        result = msg.exec_()
                        self.ui.txtusername.setText("")
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
                msg.setText("Password  can not be blank")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.setDefaultButton(QMessageBox.Ok)
                result = msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Info")
            msg.setText("User Name can not be blank")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Ok)
            result = msg.exec_()















