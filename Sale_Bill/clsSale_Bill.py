from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem,QMessageBox
from Sale_Bill.Sale_Bill import Ui_MainWindow
import sqlite3
class clsSale_Bill(QMainWindow):
    def __init__(self):
        super(clsSale_Bill,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.id=0
        self.setFixedHeight(500)
        self.setFixedWidth(1200)