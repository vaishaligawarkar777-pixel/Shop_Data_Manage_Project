from PyQt5.QtWidgets import QMainWindow

from MainWindow.MainWindow import Ui_MainWindow
from New_User.clsNew_User import clsNew_User
from Change_Password.clsChange_Password import clsChange_Password
from Block_User.clsBlock_User import clsBlock_User
class clsMainWindow(QMainWindow):
    def __init__(self):
        super(clsMainWindow,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionNew_User.triggered.connect(self.new_UserClick)
        self.ui.actionChange_Password.triggered.connect(self.Change_PasswordClick)
        self.ui.actionBlock_User.triggered.connect(self.Block_UserClick)

    def new_UserClick(self):
        self.n1=clsNew_User()
        self.ui.mdiArea.addSubWindow(self.n1)
        self.n1.show()

    def Change_PasswordClick(self):
        self.c1=clsChange_Password()
        self.ui.mdiArea.addSubWindow(self.c1)
        self.c1.show()

    def Block_UserClick(self):
        self.b1=clsBlock_User()
        self.ui.mdiArea.addSubWindow(self.b1)
        self.b1.show()
