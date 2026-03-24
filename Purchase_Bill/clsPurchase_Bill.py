from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem,QMessageBox
from Purchase_Bill.Purchase_Bill import Ui_MainWindow
import sqlite3
class clsPurchase_Bill(QMainWindow):
    def __init__(self):
        super(clsPurchase_Bill,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.id=0
        self.setFixedHeight(1180)
        self.setFixedWidth(1895)
        self.last_row = None  # 🔥 store previous row
        self.ui.tableWidget.cellClicked.connect(self.onCellClick)
        self.ui.tableWidget_2.cellClicked.connect(self.onCellClick_2)
        self.ui.tableWidget.keyPressEvent = self.move_to_next_column
        self.ui.tableWidget_2.keyPressEvent = self.move_to_next_column_2
        self.ui.txtBillNumber.setFocus()
        self.conn = sqlite3.connect('DataBase.db')
        self.cursor = self.conn.cursor()
        # self.ui.tableWidget.itemChanged.connect(self.calculate_row)
        # self.ui.tableWidget_2.itemChanged.connect(self.calculate_row_Table_2)

        self.ui.btnNew.clicked.connect(self.NewBtnClick)
        self.ui.btnSave.clicked.connect(self.SaveBtnClick)
        self.ui.btnUpdate.clicked.connect(self.UpdateBtnClick)
        self.ui.btnDelete.clicked.connect(self.DeleteBtnClick)
        self.ui.btnPrint.clicked.connect(self.PrintBtnClick)
        self.ui.btnRemove.clicked.connect(self.RemoveBtnClick)

        self.ui.tableWidget.setColumnCount(12)
        self.ui.tableWidget.verticalHeader().setVisible(0)
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ["", "Sr", "Item Name", "HSN Code", "Qty", "Rate", "GST %", "Sub Total", "IGST", "SGST", "CGST", "Total"])

        self.ui.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        self.ui.tableWidget.setRowCount(1)
        star_item = QTableWidgetItem("*")
        star_item.setTextAlignment(Qt.AlignCenter)  # Center align the star
        self.ui.tableWidget.setItem(0, 0, star_item)

        for col in range(2, 12):
            self.ui.tableWidget.setItem(0, col, QTableWidgetItem(""))

        self.ui.tableWidget.setStyleSheet("""
               QHeaderView::section {
                   background-color: #2E86C1;
                   color: white;
                   font-weight: bold;
                   padding: 4px;
                   border: 1px solid #1B4F72;
               }
               """)
        self.ui.tableWidget.setColumnWidth(0, 50)
        self.ui.tableWidget.setColumnWidth(1, 50)
        self.ui.tableWidget.setColumnWidth(2, 400)
        self.ui.tableWidget.setColumnWidth(3, 150)
        self.ui.tableWidget.setColumnWidth(4, 100)
        self.ui.tableWidget.setColumnWidth(5, 120)
        self.ui.tableWidget.setColumnWidth(6, 120)
        self.ui.tableWidget.setColumnWidth(8, 150)
        self.ui.tableWidget.setColumnWidth(9, 100)
        self.ui.tableWidget.setColumnWidth(10, 120)
        self.ui.tableWidget.setColumnWidth(11, 120)
        self.ui.tableWidget.currentCellChanged.connect(self.add_new_row)
        self.update_sr_numbers()
        self.ui.tableWidget.cellChanged.connect(self.calculateRowTotals)
        # Connect after table setup

        self.ui.tableWidget_2.setColumnCount(13)
        self.ui.tableWidget_2.verticalHeader().setVisible(0)
        self.ui.tableWidget_2.setHorizontalHeaderLabels(
            ["", "Sr. \n No", "Bill \n Number", "Date", "Party Name", "Address", "Item Name", "Qty", "Rate", "GST",
             "Grand_Total", "Total_In_Word", "Id"])
        self.ui.tableWidget_2.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        self.ui.tableWidget_2.setRowCount(1)
        star_item = QTableWidgetItem("*")
        star_item.setTextAlignment(Qt.AlignCenter)  # Center align the star
        self.ui.tableWidget_2.setItem(0, 0, star_item)

        for col in range(2, 13):
            self.ui.tableWidget_2.setItem(0, col, QTableWidgetItem(""))
        self.ui.tableWidget_2.setStyleSheet("""
                      QHeaderView::section {
                          background-color: #2E86C1;
                          color: white;
                          font-weight: bold;
                          padding: 4px;
                          border: 1px solid #1B4F72;
                      }
                      """)

        self.ui.tableWidget_2.setColumnWidth(0, 50)
        self.ui.tableWidget_2.setColumnWidth(1, 50)
        self.ui.tableWidget_2.setColumnWidth(2, 100)
        self.ui.tableWidget_2.setColumnWidth(3, 150)
        self.ui.tableWidget_2.setColumnWidth(4, 300)
        self.ui.tableWidget_2.setColumnWidth(5, 150)
        self.ui.tableWidget_2.setColumnWidth(6, 120)
        self.ui.tableWidget_2.setColumnWidth(7, 100)
        self.ui.tableWidget_2.setColumnWidth(8, 100)
        self.ui.tableWidget_2.setColumnWidth(9, 50)
        self.ui.tableWidget_2.setColumnWidth(11, 150)
        self.ui.tableWidget_2.setColumnWidth(12, 150)

        self.ui.tableWidget_2.currentCellChanged.connect(self.add_new_row_2)

        self.ui.txtBillNumber.editingFinished.connect(self.loadData)

    def add_new_row_2(self, currentRow, currentCol, previousRow, previousCol):
        table = self.ui.tableWidget_2

        if currentRow == table.rowCount() - 1:
            table.insertRow(table.rowCount())

            row = table.rowCount() - 1

            # ⭐ Column 0 → "*"
            star_item = QTableWidgetItem("*")
            star_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 0, star_item)

            # ✅ Column 1 → Sr No
            sr_item = QTableWidgetItem(str(row + 1))
            sr_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 1, sr_item)

            # Empty cells
            for col in range(2, 12):
                table.setItem(row, col, QTableWidgetItem(""))

                self.update_sr_numbers_2()

    def update_sr_numbers_2(self):
        table = self.ui.tableWidget_2
        for row in range(table.rowCount()):
            sr_item = QTableWidgetItem(str(row + 1))
            sr_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 1, sr_item)

    def update_sr_numbers(self):
        table = self.ui.tableWidget
        for row in range(table.rowCount()):
            sr_item = QTableWidgetItem(str(row + 1))
            sr_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 1, sr_item)

    def add_new_row(self, currentRow, currentCol, previousRow, previousCol):

        table = self.ui.tableWidget

        if currentRow == table.rowCount() - 1:
            table.insertRow(table.rowCount())

            row = table.rowCount() - 1

            # ⭐ Column 0 → "*"
            star_item = QTableWidgetItem("*")
            star_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 0, star_item)

            # ✅ Column 1 → Sr No
            sr_item = QTableWidgetItem(str(row + 1))
            sr_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 1, sr_item)

            # Empty cells
            for col in range(2, 12):
                table.setItem(row, col, QTableWidgetItem(""))

    def move_to_next_column(self, event):
        table = self.ui.tableWidget
        row = table.currentRow()
        col = table.currentColumn()

        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Move to next column if not last column
            if col < table.columnCount() - 1:
                table.setCurrentCell(row, col + 1)
            else:
                # If last column, optionally move to next row first column
                if row < table.rowCount() - 1:
                    table.setCurrentCell(row + 1, 2)  # Start at Item Name of next row
                else:
                    # Or add new row automatically
                    table.insertRow(table.rowCount())
                    table.setCurrentCell(row + 1, 2)
        else:
            # Normal key event
            super(type(table), table).keyPressEvent(event)

    def move_to_next_column_2(self, event=None):
        table = self.ui.tableWidget_2
        row = table.currentRow()
        col = table.currentColumn()

        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Move to next column if not last column
            if col < table.columnCount() - 1:
                table.setCurrentCell(row, col + 1)
            else:
                # If last column, optionally move to next row first column
                if row < table.rowCount() - 1:
                    table.setCurrentCell(row + 1, 2)  # Start at Item Name of next row
                else:
                    # Or add new row automatically
                    table.insertRow(table.rowCount())
                    table.setCurrentCell(row + 1, 2)
        else:
            # Normal key event
            super(type(table), table).keyPressEvent(event)

    def onCellClick(self, row, column):

        print("Clicked:", row, column)  # debug

        # ✅ Correct column check (Item Name = 2)
        if column != 2:
            return

        columns_to_fill = [3, 4, 5, 6, 7, 8, 9, 10, 11]

        # 🔴 Step 1: Clear ALL rows
        for r in range(self.ui.tableWidget.rowCount()):
            for col in columns_to_fill:
                self.ui.tableWidget.setItem(r, col, QTableWidgetItem(""))

        # 🟢 Step 2: Fill ONLY clicked row
        for col in columns_to_fill:
            self.ui.tableWidget.setItem(row, col, QTableWidgetItem("0"))

    def calculateRowTotals(self, row, column):
        # Only recalc if Qty, Rate, GST% change
        if column not in [4, 5, 6]:
            return

        try:
            # Safe read
            qty_item = self.ui.tableWidget.item(row, 4)
            rate_item = self.ui.tableWidget.item(row, 5)
            gst_item = self.ui.tableWidget.item(row, 6)

            qty = float(qty_item.text()) if qty_item and qty_item.text().strip() != "" else 0
            rate = float(rate_item.text()) if rate_item and rate_item.text().strip() != "" else 0
            gst = float(gst_item.text()) if gst_item and gst_item.text().strip() != "" else 0

            # Subtotal = Qty × Rate
            subtotal = qty * rate
            self.ui.tableWidget.setItem(row, 7, QTableWidgetItem(f"{subtotal:.2f}"))

            # IGST → always 0, ignored in total
            self.ui.tableWidget.setItem(row, 8, QTableWidgetItem("0"))

            # SGST & CGST = 50% of GST on subtotal
            sgst = subtotal * (gst / 100) / 2
            cgst = subtotal * (gst / 100) / 2

            self.ui.tableWidget.setItem(row, 9, QTableWidgetItem(f"{sgst:.2f}"))
            self.ui.tableWidget.setItem(row, 10, QTableWidgetItem(f"{cgst:.2f}"))

            # Total = subtotal + SGST + CGST (IGST ignored)
            total = subtotal + sgst + cgst
            self.ui.tableWidget.setItem(row, 11, QTableWidgetItem(f"{total:.2f}"))

        except Exception as e:
            print("Calculation error:", e)

    def onCellClick_2(self, row, column):

        print("Clicked:", row, column)  # debug

        # ✅ Correct column check (Item Name = 2)
        if column != 2:
            return

        columns_to_fill = [3, 4, 5, 6, 7, 8, 9, 10, 11]

        # 🔴 Step 1: Clear ALL rows
        for r in range(self.ui.tableWidget_2.rowCount()):
            for col in columns_to_fill:
                self.ui.tableWidget_2.setItem(r, col, QTableWidgetItem(""))

        # 🟢 Step 2: Fill ONLY clicked row
        for col in columns_to_fill:
            self.ui.tableWidget_2.setItem(row, col, QTableWidgetItem("0"))

    def loadData(self):
        bill_no = self.ui.txtBillNumber.text()

        if bill_no == "":
            return

        sql = "SELECT * FROM Sale_Purchase_Data WHERE Bill_Number=?"
        self.cursor.execute(sql, (bill_no,))
        data = self.cursor.fetchone()

        if data:
            self.ui.dateEdit.setDate(QDate.fromString(data[2], "yyyy/MM/dd"))
            self.ui.txtShriMS.setText(str(data[3]))
            self.ui.txtAddress.setText(str(data[4]))
            self.ui.txtState.setText(str(data[5]))
            self.ui.txtStatePin.setText(str(data[6]))
            self.ui.txtGST_IN.setText(str(data[7]))
            self.ui.txtIncRecNo.setText(str(data[8]))
            self.ui.cmbTransaction_Type.setCurrentText(data[9])
        else:
            # Optional: clear if not found
            self.clearFocus()

    def NewBtnClick(self):
        pass

    def SaveBtnClick(self):
        Date = self.ui.dateEdit.date().toString("yyyy/MM/dd")
        Transaction_Type = self.ui.cmbTransaction_Type.currentText()
        sql = f"insert into Sale_Purchase_Data values(null,'{self.ui.txtBillNumber.text()}','{Date}','{self.ui.txtShriMS.text()}','{self.ui.txtAddress.text()}','{self.ui.txtState.text()}','{self.ui.txtStatePin.text()}','{self.ui.txtGST_IN.text()}','{self.ui.txtIncRecNo.text()}','{Transaction_Type}')"
        self.cursor.execute(sql)
        self.conn.commit()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Info")
        msg.setText("Data Save Successfully")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Ok)
        result = msg.exec_()

    def UpdateBtnClick(self):
        Date = self.ui.dateEdit.date().toString("yyyy/MM/dd")
        Transaction_Type = self.ui.cmbTransaction_Type.currentText()
        sql = f"update Sale_Purchase_Data set Date='{Date}',ShriMS='{self.ui.txtShriMS.text()}',Address='{self.ui.txtAddress.text()}',State='{self.ui.txtState.text()}',State_Pin='{self.ui.txtStatePin.text()}',GST_IN='{self.ui.txtGST_IN.text()}', IncRecNo='{self.ui.txtIncRecNo.text()}',Transaction_Type='{Transaction_Type}' where Bill_Number='{self.ui.txtBillNumber.text()}'"
        self.cursor.execute(sql)
        self.conn.commit()

        QMessageBox.information(self, "Success", "Data Updated Successfully")

    def DeleteBtnClick(self):
        sql = "DELETE FROM Sale_Purchase_Data WHERE Bill_Number=?"
        self.cursor.execute(sql, (self.ui.txtBillNumber.text(),))
        self.conn.commit()

        QMessageBox.information(self, "Deleted", "Record Deleted Successfully")

    def PrintBtnClick(self):
        print("------ BILL ------")
        print("Bill No:", self.ui.txtBillNumber.text())
        print("Date:", self.ui.dateEdit.date().toString("yyyy/MM/dd"))
        print("Name:", self.ui.txtShriMS.text())
        print("Address:", self.ui.txtAddress.text())
        print("State:", self.ui.txtState.text())
        print("GST:", self.ui.txtGST_IN.text())
        print("Transaction:", self.ui.cmbTransaction_Type.currentText())

    def RemoveBtnClick(self):
        self.ui.txtBillNumber.clear()
        self.ui.txtShriMS.clear()
        self.ui.txtAddress.clear()
        self.ui.txtState.clear()
        self.ui.txtStatePin.clear()
        self.ui.txtGST_IN.clear()
        self.ui.txtIncRecNo.clear()
        self.ui.cmbTransaction_Type.setCurrentIndex(0)





