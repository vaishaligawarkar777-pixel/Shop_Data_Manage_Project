from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem,QMessageBox
from Block_User.Block_user import Ui_MainWindow
import sqlite3
class clsBlock_User(QMainWindow):
    def __init__(self):
        super(clsBlock_User,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.id=0
        self.setFixedHeight(110)
        self.setFixedWidth(360)
        self.ui.cmbselectuser.setFocus()
        self.conn=sqlite3.connect('DataBase.db')
        self.cursor=self.conn.cursor()
        self.ui.btnBlock.clicked.connect(self.BlockBtnClick)
        sql=f"Select * From User_LoginData"
        self.cursor.execute(sql)
        result=self.cursor.fetchall()
        for row in result:
            self.ui.cmbselectuser.addItem(str(row[1]))

    def BlockBtnClick(self):
        sql = f"delete from User_LoginData where UserName='{self.ui.cmbselectuser.currentText()}'"
        self.cursor.execute(sql)
        self.conn.commit()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Info")
        msg.setText("Delete user Successfully ")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Ok)
        result = msg.exec_()
        self.ui.cmbselectuser.setCurrentText("")
