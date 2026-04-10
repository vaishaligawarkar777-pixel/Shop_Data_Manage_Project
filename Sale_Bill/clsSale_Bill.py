import math

from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem,QMessageBox
from Sale_Bill.Sale_Bill import Ui_MainWindow
import sqlite3

class clsSale_Bill(QMainWindow):
    def __init__(self):
        super(clsSale_Bill,self).__init__()
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
        self.update_grand_total_and_words()

        self.ui.btnNew.clicked.connect(self.NewBtnClick)
        self.ui.btnSave.clicked.connect(self.SaveBtnClick)
        self.ui.btnSave.clicked.connect(self.SaveBtnClick_2)
        self.ui.btnUpdate.clicked.connect(self.UpdateBtnClick)
        self.ui.btnDelete.clicked.connect(self.DeleteBtnClick)
        self.ui.btnPrint.clicked.connect(self.PrintBtnClick)
        self.ui.btnRemove.clicked.connect(self.RemoveBtnClick)

        self.ui.tableWidget.setColumnCount(12)
        self.ui.tableWidget.verticalHeader().setVisible(0)
        self.ui.tableWidget.setHorizontalHeaderLabels(["", "Sr", "Item Name", "HSN Code", "Qty", "Rate", "GST %", "Sub Total", "IGST", "SGST","CGST","Total"])

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
        #self.ui.tableWidget.itemChanged.connect(self.calculate_grand_total)
        # Connect after table setup



        self.ui.tableWidget_2.setColumnCount(13)
        self.ui.tableWidget_2.verticalHeader().setVisible(0)
        self.ui.tableWidget_2.setHorizontalHeaderLabels(["", "Sr. \n No", "Bill \n Number", "Date", "Party Name", "Address", "Item Name", "Qty", "Rate", "GST", "Grand_Total", "Total_In_Word","Id"])
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

        # self.loadDataInTable()

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

    def move_to_next_column(self, event=None):
        table = self.ui.tableWidget
        row = table.currentRow()
        col = table.currentColumn()

        START_COL = 2  # First editable column (Item Name)

        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            # Move forward
            if col < table.columnCount() - 1:
                table.setCurrentCell(row, col + 1)
            else:
                if row < table.rowCount() - 1:
                    table.setCurrentCell(row + 1, START_COL)
                else:
                    table.insertRow(table.rowCount())
                    table.setCurrentCell(row + 1, START_COL)

        elif event.key() == Qt.Key_Backspace:
            current_item = table.currentItem()

            # If in protected column → do nothing
            if col < START_COL:
                return

            # If cell has data → clear only data
            if current_item and current_item.text():
                current_item.setText("")
            else:
                # Move backward but NEVER go into Sr No column
                if col > START_COL:
                    table.setCurrentCell(row, col - 1)
                else:
                    # If at first editable column → go to previous row last editable column
                    if row > 0:
                        table.setCurrentCell(row - 1, table.columnCount() - 1)

        else:
            super(type(table), table).keyPressEvent(event)

    def move_to_next_column_2(self, event=None):
        table = self.ui.tableWidget
        row = table.currentRow()
        col = table.currentColumn()

        START_COL = 2  # First editable column (Item Name)

        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            # Move forward
            if col < table.columnCount() - 1:
                table.setCurrentCell(row, col + 1)
            else:
                if row < table.rowCount() - 1:
                    table.setCurrentCell(row + 1, START_COL)
                else:
                    table.insertRow(table.rowCount())
                    table.setCurrentCell(row + 1, START_COL)

        elif event.key() == Qt.Key_Backspace:
            current_item = table.currentItem()

            # If in protected column → do nothing
            if col < START_COL:
                return

            # If cell has data → clear only data
            if current_item and current_item.text():
                current_item.setText("")
            else:
                # Move backward but NEVER go into Sr No column
                if col > START_COL:
                    table.setCurrentCell(row, col - 1)
                else:
                    # If at first editable column → go to previous row last editable column
                    if row > 0:
                        table.setCurrentCell(row - 1, table.columnCount() - 1)

        else:
            super(type(table), table).keyPressEvent(event)


    def onCellClick(self, row, column):

        print("Clicked:", row, column)

        if column != 2:
            return

        columns_to_fill = [3, 4, 5, 6, 7, 8, 9, 10, 11]

        # 🟢 ONLY update clicked row (do NOT clear others)
        for col in columns_to_fill:
            item = self.ui.tableWidget.item(row, col)

            if item is None:
                item = QTableWidgetItem()
                self.ui.tableWidget.setItem(row, col, item)

            # Only set default if empty (optional)
            if item.text() == "":
                item.setText("0")

    def calculateRowTotals(self, row, column):

        if column not in [4, 5, 6]:
            return

        try:
            table = self.ui.tableWidget

            qty_item = table.item(row, 4)
            rate_item = table.item(row, 5)
            gst_item = table.item(row, 6)

            qty = float(qty_item.text()) if qty_item and qty_item.text().strip() else 0
            rate = float(rate_item.text()) if rate_item and rate_item.text().strip() else 0
            gst = float(gst_item.text()) if gst_item and gst_item.text().strip() else 0

            subtotal = qty * rate
            gst_amount = subtotal * gst / 100

            sgst = gst_amount / 2
            cgst = gst_amount / 2

            total = subtotal + gst_amount

            table.blockSignals(True)

            table.setItem(row, 7, QTableWidgetItem(f"{subtotal:.2f}"))
            table.setItem(row, 8, QTableWidgetItem("0"))
            table.setItem(row, 9, QTableWidgetItem(f"{sgst:.2f}"))
            table.setItem(row, 10, QTableWidgetItem(f"{cgst:.2f}"))
            table.setItem(row, 11, QTableWidgetItem(f"{total:.2f}"))

            table.blockSignals(False)

            # ✅ MUST BE AFTER blockSignals(False)
            self.update_grand_total_and_words()

        except Exception as e:
            print("Calculation error:", e)

    def onCellClick_2(self, row, column):

        print("Clicked:", row, column)

        if column != 2:
            return

        columns_to_fill = [3, 4, 5, 6, 7, 8, 9, 10, 11,12]

        # 🟢 ONLY update clicked row (do NOT clear others)
        for col in columns_to_fill:
            item = self.ui.tableWidget_2.item(row, col)

            if item is None:
                item = QTableWidgetItem()
                self.ui.tableWidget_2.setItem(row, col, item)

            # Only set default if empty (optional)
            if item.text() == "":
                item.setText("0")


    def number_to_words(self, number):
        units = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
                 "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]

        tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

        if number < 20:
            return units[number]

        if number < 100:
            return tens[number // 10] + (" " + units[number % 10] if number % 10 != 0 else "")

        if number < 1000:
            return units[number // 100] + " Hundred " + (
                "and " + self.number_to_words(number % 100) if number % 100 != 0 else "")

        if number < 100000:
            return self.number_to_words(number // 1000) + " Thousand " + (
                self.number_to_words(number % 1000) if number % 1000 != 0 else "")

        if number < 10000000:
            return self.number_to_words(number // 100000) + " Lakh " + (
                self.number_to_words(number % 100000) if number % 100000 != 0 else "")

        return str(number)


    def update_grand_total_and_words(self):
        table = self.ui.tableWidget
        grand_total = 0.0

        # Calculate grand total
        for row in range(table.rowCount()):
            item = table.item(row, 11)
            if item is not None:
                text = item.text().strip()
                if text != "":
                    try:
                        value = float(text)
                        grand_total += value
                    except:
                        pass

        # ROUNDING (.50 and above → UP)
        rounded_total = int(math.floor(grand_total + 0.5))

        # Show rounded total
        self.ui.txtGrand_Total.setText(str(rounded_total))

        # ✅ Round Off value (this was missing)
        round_off = rounded_total - grand_total
        self.ui.txtRoundOff.setText(f"{round_off:+.2f}")

        # Words (based on rounded total)
        words = self.number_to_words(rounded_total)
        words += " Rupees Only"
        self.ui.txtTotaWord.setText(words)

    # def loadDataInTable(self):
    #     self.cursor.execute(f"select * from Sale_Purchase_Data")
    #     result = self.cursor.fetchall()
    #     self.ui.tableWidget_2.setRowCount(0)
    #     rw = 0
    #     for row in result:
    #         rw = int(rw) + 1
    #         self.ui.tableWidget_2.setRowCount(rw)
    #
    #         self.ui.tableWidget_2.setItem(rw - 1, 1, QTableWidgetItem(str(row[1])))
    #         # self.ui.tableWidget_2.setItem(rw - 1, 2, QTableWidgetItem(str(row[2])))
    #         # self.ui.tableWidget_2.setItem(rw - 1, 3, QTableWidgetItem(str(row[3])))
    #         # self.ui.tableWidget_2.setItem(rw - 1, 4, QTableWidgetItem(str(row[4])))
    #         # self.ui.tableWidget_2.setItem(rw - 1, 5, QTableWidgetItem(str(row[5])))
    #         # self.ui.tableWidget_2.setItem(rw - 1, 6, QTableWidgetItem(str(row[6])))


    def NewBtnClick(self):
        self.ui.txtBillNumber.setText("")
        self.ui.txtShriMS.setText("")
        self.ui.txtAddress.setText("")
        self.ui.txtState.setText("")
        self.ui.txtStateCode.setText("")
        self.ui.txtGST_IN.setText("")
        self.ui.txtIncRecNo.setText("")

    def SaveBtnClick(self):
        # First main table
        Date = self.ui.dateEdit.date().toString("yyyy/MM/dd")
        Transaction_Type = self.ui.cmbTransaction_Type.currentText()

        sql = f"insert into Sale_Data values(null,'{self.ui.txtBillNumber.text()}','{Date}','{self.ui.txtShriMS.text()}','{self.ui.txtAddress.text()}','{self.ui.txtState.text()}','{self.ui.txtStateCode.text()}','{self.ui.txtGST_IN.text()}','{self.ui.txtIncRecNo.text()}','{Transaction_Type}','{self.ui.txtGrand_Total.text()}','{self.ui.txtRoundOff.text()}')"

        self.cursor.execute(sql)

        # Then detail table
        self.SaveBtnClick_2()

        self.conn.commit()
        #print("Full Bill Saved")

    def SaveBtnClick_2(self):
        BillNo = self.ui.txtBillNumber.text()

        for row in range(self.ui.tableWidget.rowCount()):

            if self.ui.tableWidget.item(row, 1) is None:
                continue

            def getVal(col):
                item = self.ui.tableWidget.item(row, col)
                return item.text() if item else "0"

            sql = f"""
            insert into Sale_Data_Detail 
            values(
            null,
            '{BillNo}',
            '{getVal(1)}',
            '{getVal(2)}',
            '{getVal(3)}',
            '{getVal(4)}',
            '{getVal(5)}',
            '{getVal(6)}',
            '{getVal(7)}',
            '{getVal(8)}',
            '{getVal(9)}',
            '{getVal(10)}'
            )
            """

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
        sql = f"update Sale_Data set Date='{Date}',ShriMS='{self.ui.txtShriMS.text()}',Address='{self.ui.txtAddress.text()}',State='{self.ui.txtState.text()}',State_Pin='{self.ui.txtStateCode.text()}',GST_IN='{self.ui.txtGST_IN.text()}', IncRecNo='{self.ui.txtIncRecNo.text()}',Transaction_Type='{Transaction_Type}', Grand_Total='{self.ui.txtGrand_Total.text()}',Round_Off='{self.ui.txtRoundOff.text()}'where Bill_Number='{self.ui.txtBillNumber.text()}'"
        self.cursor.execute(sql)
        self.conn.commit()

        QMessageBox.information(self, "Success", "Data Updated Successfully")
    def DeleteBtnClick(self):
        sql = "DELETE FROM Sale_Data WHERE Bill_Number=?"
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
        self.ui.txtStateCode.clear()
        self.ui.txtGST_IN.clear()
        self.ui.txtIncRecNo.clear()
        self.ui.cmbTransaction_Type.setCurrentIndex(0)