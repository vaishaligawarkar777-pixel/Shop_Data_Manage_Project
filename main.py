import sqlite3
from PyQt5.QtWidgets import QApplication
from MainWindow.clsMainWindow import clsMainWindow
from Login.clsLogin import clsLogin
import sys

app=QApplication([])
conn=sqlite3.connect('DataBase.db')
cursor=conn.cursor()
sql=f"Select * From User_LoginData"
cursor.execute(sql)
result=cursor.fetchall()
i=0
for row in result:
    i+=1
m=clsMainWindow()
l=clsLogin()

if i==0:
    m.show()
else:
   l.show()
sys.exit(app.exec_())