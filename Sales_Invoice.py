import sys
import sqlite3
from fpdf import FPDF
import mysql.connector
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel, QGridLayout

import os
import subprocess
from datetime import date, datetime

import mysql.connector
from hijri_converter import Hijri, Gregorian
from num2words import num2words
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication,
                             QCheckBox,
                             QComboBox,
                             QDateEdit,
                             QDateTimeEdit,
                             QDial,
                             QDoubleSpinBox,
                             QFontComboBox,
                             QLabel,
                             QLCDNumber,
                             QLineEdit,
                             QMainWindow,
                             QProgressBar,
                             QPushButton,
                             QRadioButton,
                             QSlider,
                             QSpinBox,
                             QTimeEdit,
                             QVBoxLayout,
                             QWidget,
                             QHBoxLayout,
                             QGridLayout,
                             QTableWidget,
                             QHeaderView, QMenu, QAction, QInputDialog, QTableWidgetItem
                             )
from PyQt5.QtGui import (QPalette,
                         QColor,
                         QFont,
                         )

import sys
from random import choice

class SalesInv(QMainWindow):
    def __init__(self):
        super().__init__()
        global mydb
        global mycursor
        import utils
        mydb = utils.connection
        mycursor = mydb.cursor()
        
        self.setWindowTitle("Sales Invoice")
        self.setGeometry(150, 150, 1200, 600)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)
        
        self.create_buttons()
        self.create_header()
        self.create_table()
        self.create_summary()
        self.create_footer()
        

        self.current_record = None  # To keep track of the current record index

        self.connect_db()

    def connect_db(self):
     self.conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Somsoc1retupmoc",
        port=3306,
        database='sugarBilling'
    )
    


    def create_header(self):
        
        custQ = "SELECT * FROM Customer"
        mycursor.execute(custQ)
        result = mycursor.fetchall()
        
        header_layout = QGridLayout()

        header_layout.addWidget(QLabel("Acc No"), 0, 0)
        self.acc_no_input = QComboBox()
        self.acc_no_input.setCurrentIndex(1)
        self.acc_no_input.setStyleSheet("QComboBox"
                                  "{"
                                  "background-color: white"
                                  "}")
        header_layout.addWidget(self.acc_no_input, 0, 1)

        header_layout.addWidget(QLabel("State Name"), 0, 2)
        self.state_name_input = QLineEdit()
        header_layout.addWidget(self.state_name_input, 0, 3)

        header_layout.addWidget(QLabel("Date"), 0, 4)
        self.date_input = QLabel(str(date.today()))
        header_layout.addWidget(self.date_input, 0, 5)

        header_layout.addWidget(QLabel("Name"), 1, 0)
        self.name_input = QComboBox()
        self.name_input.setCurrentIndex(1)
        self.name_input.setStyleSheet("QComboBox"
                                  "{"
                                  "background-color: white"
                                  "}")
        header_layout.addWidget(self.name_input, 1, 1)

        header_layout.addWidget(QLabel("Code"), 1, 2)
        self.code_input = QLineEdit()
        header_layout.addWidget(self.code_input, 1, 3)

        header_layout.addWidget(QLabel("Time"), 1, 4)
        self.time_input = QLabel(datetime.now().strftime("%H:%M"))
        header_layout.addWidget(self.time_input, 1, 5)

        header_layout.addWidget(QLabel("GSTIN"), 2, 0)
        self.gstin_input = QLabel(result[0][5])
        header_layout.addWidget(self.gstin_input, 2, 1)

        header_layout.addWidget(QLabel("Bill No"), 2, 2)
        self.bill_no_input = QLabel(str(self.billNum()))
        header_layout.addWidget(self.bill_no_input, 2, 3)

        self.layout.addLayout(header_layout)
        
        
        for row in result:
            self.acc_no_input.addItem(str(row[0]))
            self.name_input.addItem(row[1])
        print(result)
        
        self.name_input.currentIndexChanged.connect(
            lambda: self.comboValueChanged(self.name_input, self.name_input.currentIndex()))
        self.acc_no_input.currentIndexChanged.connect(
            lambda: self.comboValueChanged(self.acc_no_input, self.acc_no_input.currentIndex()))
        
        
        
    def comboValueChanged(self, combo, index):
        mycursor.execute("SELECT * FROM Customer")
        result = mycursor.fetchall()
        if combo == self.name_input:
            self.acc_no_input.setCurrentIndex(index)
            self.editBalanceSheet(self.footer_table)

            # self.VATno.setText(result[index][5])
        else:
            self.name_input.setCurrentIndex(index)
            self.editBalanceSheet(self.footer_table)

            # self.VATno.setText(result[index][5])

    def editBalanceSheet(self, balanceSheet):
        balanceSheet.setCellWidget(0, 0, QLabel(self.acc_no_input.currentText()))
        balanceSheet.setCellWidget(0, 1, QLabel(self.name_input.currentText()))
        balanceSyntax = "SELECT SUM(cashDebit), SUM(cashCredit) FROM Cust_Bal WHERE accNo = '" + str(self.acc_no_input.currentText()) + "'"
        mycursor.execute(balanceSyntax)
        balanceResult = mycursor.fetchall()
        print(str(self.acc_no_input.currentText()), "balanceResult")

        cDebit = balanceResult[0][0]
        cCredit = balanceResult[0][1]

        balanceSheet.setCellWidget(0, 2, QLabel(str(round(cDebit, 2))))
        balanceSheet.setCellWidget(0, 3, QLabel(str(round(cCredit, 2))))

    def create_table(self):
        table_layout = QVBoxLayout()

        self.table = QTableWidget(5, 7)
        self.table.setHorizontalHeaderLabels(
            ["Description of goods", "HSN Code", "Quantity", "Rate", "Total", "Discount", "Discounted price"])

        # Stretch columns to fit the available space
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setColumnWidth(1, 130)
        self.table.setColumnWidth(2, 130)
        self.table.setColumnWidth(3, 130)
        self.table.setColumnWidth(4, 130)
        self.table.setColumnWidth(5, 130)
        self.table.setColumnWidth(6, 130)
        # Connect Quantity, Rate, and Discount cells to the calculation function
        for row in range(self.table.rowCount()):
            itemName = QLineEdit()
            itemName.setText("")
            itemName.setFrame(False)
            itemName.setProperty('row', row)
            self.table.setCellWidget(row, 0, itemName)
            
            quantity_item = QLineEdit()
            quantity_item.setText("0")
            quantity_item.setFrame(False)
            self.table.setCellWidget(row, 2, quantity_item)

            rate_item = QLineEdit()
            rate_item.setText("0")
            rate_item.setFrame(False)
            self.table.setCellWidget(row, 3, rate_item)

            discount_item = QLineEdit()
            discount_item.setText("0")
            discount_item.setFrame(False)
            self.table.setCellWidget(row, 5, discount_item)

            itemName.editingFinished.connect(self.counter)
            quantity_item.editingFinished.connect(self.update_totals)
            rate_item.editingFinished.connect(self.update_totals)
            discount_item.editingFinished.connect(self.update_totals)
        

        table_layout.addWidget(self.table)
        self.layout.addLayout(table_layout)
        # initialize the array to store item names
        self.itemName = []

    def clear_table(self):
        self.table.setHorizontalHeaderLabels(
            ["Description of goods", "HSN Code", "Quantity", "Rate", "Total", "Discount", "Discounted price"])

        # Stretch columns to fit the available space
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setColumnWidth(1, 130)
        self.table.setColumnWidth(2, 130)
        self.table.setColumnWidth(3, 130)
        self.table.setColumnWidth(4, 130)
        self.table.setColumnWidth(5, 130)
        self.table.setColumnWidth(6, 130)
        # Connect Quantity, Rate, and Discount cells to the calculation function
        for row in range(self.table.rowCount()):
            itemName = QLineEdit()
            itemName.setText("")
            itemName.setFrame(False)
            itemName.setProperty('row', row)
            self.table.setCellWidget(row, 0, itemName)
            
            quantity_item = QLineEdit()
            quantity_item.setText("0")
            quantity_item.setFrame(False)
            self.table.setCellWidget(row, 2, quantity_item)

            rate_item = QLineEdit()
            rate_item.setText("0")
            rate_item.setFrame(False)
            self.table.setCellWidget(row, 3, rate_item)

            discount_item = QLineEdit()
            discount_item.setText("0")
            discount_item.setFrame(False)
            self.table.setCellWidget(row, 5, discount_item)

            itemName.editingFinished.connect(self.counter)
            quantity_item.editingFinished.connect(self.update_totals)
            rate_item.editingFinished.connect(self.update_totals)
            discount_item.editingFinished.connect(self.update_totals)
        self.itemName = []
        self.editBalanceSheet(self.footer_table)

    def update_totals(self):
        for row in range(self.table.rowCount()):
            quantity_widget = self.table.cellWidget(row, 2)
            rate_widget = self.table.cellWidget(row, 3)
            discount_widget = self.table.cellWidget(row, 5)

            if quantity_widget or rate_widget or discount_widget:
                try:
                    quantity = float(quantity_widget.text())
                    rate = float(rate_widget.text())
                    discount = float(discount_widget.text())

                    total = quantity * rate
                    discounted_price = total - (total * discount / 100)

                    self.table.setItem(row, 4, QTableWidgetItem(f"{total:.2f}"))
                    self.table.setItem(row, 6, QTableWidgetItem(f"{discounted_price:.2f}"))
                    
                                        
                except ValueError:
                    self.table.setItem(row, 4, QTableWidgetItem("0.00"))
                    self.table.setItem(row, 6, QTableWidgetItem("0.00"))
        
        try:
            totalAmount = 0.0
            print(len(self.itemName), "itemName length")
            for i in range(len(self.itemName)):
                totalAmount += float(self.table.item(i, 6).text())
                print(self.table.item(i, 6).text(), "price")
            
            bulk_discount = float(self.discount_input.text())
            before_tax = float(self.total_before_tax_input.text())
            sgst = float(self.sgst_input.text())
            cgst = float(self.cgst_input.text())
            igst = float(self.igst_input.text())
            after_tax = float(self.total_after_tax_input.text())
            
            bulk_discount_price = totalAmount - (totalAmount * bulk_discount / 100)
            self.total_before_tax_input.setText(f"{bulk_discount_price:.2f}")
            tax_amt = bulk_discount_price + (bulk_discount_price * sgst / 100) + (bulk_discount_price * cgst / 100) + (bulk_discount_price * igst / 100)
            self.total_after_tax_input.setText(f"{tax_amt:.2f}")
        except ValueError or TypeError:
            bulk_discount = self.discount_input
            before_tax = self.total_before_tax_input
            sgst = self.sgst_input
            cgst = self.cgst_input
            igst = self.igst_input
            after_tax = self.total_after_tax_input

            
            bulk_discount.setText("0")
            before_tax.setText(totalAmount)
            sgst.setText("0")
            cgst.setText("0")
            igst.setText("0")
            after_tax.setText(totalAmount)
            
            
    def counter(self):
        item = self.sender()
        row = item.property('row')
        print(row)
        if self.table.cellWidget(row, 0).text() != "" and self.table.cellWidget(row, 0).text() != None:
            if row == len(self.itemName):
                self.itemName.append(self.table.cellWidget(row, 0).text())
            if row < len(self.itemName):
                self.itemName[row] = self.table.cellWidget(row, 0).text()               

    def create_summary(self):
        summary_layout = QGridLayout()

        summary_layout.addWidget(QLabel("Discount"), 0, 0)
        self.discount_input = QLineEdit("0")
        summary_layout.addWidget(self.discount_input, 0, 1)

        summary_layout.addWidget(QLabel("Total before tax"), 1, 0)
        self.total_before_tax_input = QLabel("0")
        summary_layout.addWidget(self.total_before_tax_input, 1, 1)

        summary_layout.addWidget(QLabel("Add SGST"), 2, 0)
        self.sgst_input = QLineEdit("0")
        summary_layout.addWidget(self.sgst_input, 2, 1)

        summary_layout.addWidget(QLabel("Add CGST"), 3, 0)
        self.cgst_input = QLineEdit("0")
        summary_layout.addWidget(self.cgst_input, 3, 1)

        summary_layout.addWidget(QLabel("Add IGST"), 4, 0)
        self.igst_input = QLineEdit("0")
        summary_layout.addWidget(self.igst_input, 4, 1)

        summary_layout.addWidget(QLabel("Total after tax"), 5, 0)
        self.total_after_tax_input = QLabel("0")
        summary_layout.addWidget(self.total_after_tax_input, 5, 1)

        self.layout.addLayout(summary_layout)
        
        self.discount_input.editingFinished.connect(self.update_totals)
        self.sgst_input.editingFinished.connect(self.update_totals)
        self.cgst_input.editingFinished.connect(self.update_totals)
        self.igst_input.editingFinished.connect(self.update_totals)
        

    def create_footer(self):
        footer_layout = QVBoxLayout()


        self.footer_table = QTableWidget(1, 4)
        
        # Set the headers for the table
        self.footer_table.setHorizontalHeaderLabels(["Acc No", "Name", "Debit", "Credit"])

        # Make sure the table stretches across the entire window width
        
        self.footer_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.footer_table.verticalHeader().setVisible(False)
        self.footer_table.setCellWidget(0, 0, QLabel(self.acc_no_input.currentText()))
        self.footer_table.setCellWidget(0, 1, QLabel(self.name_input.currentText()))
        balanceSyntax = "SELECT SUM(cashDebit), SUM(cashCredit) FROM Cust_Bal WHERE accNo = '" + str(self.acc_no_input.currentText()) + "'"
        mycursor.execute(balanceSyntax)
        balanceResult = mycursor.fetchall()


        cDebit = balanceResult[0][0]
        cCredit = balanceResult[0][1]

        self.footer_table.setCellWidget(0, 2, QLabel(str(round(cDebit, 2))))
        self.footer_table.setCellWidget(0, 3, QLabel(str(round(cCredit, 2))))
        self.footer_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
    
    
    
        # Add the table to the layout
        footer_layout.addWidget(self.footer_table)
        
        # Add the footer layout to the main layout
        self.layout.addLayout(footer_layout)

    def create_buttons(self):
        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(lambda: self.save_invoice([self.save_button, self.clear_button]))
        button_layout.addWidget(self.save_button)

        self.clear_button = QPushButton("Clear")
        self.save_button.clicked.connect(self.clear_table)
        button_layout.addWidget(self.clear_button)
        
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.load_previous)
        button_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.load_next)
        button_layout.addWidget(self.next_button)

        self.pdf_button = QPushButton("PDF")
        self.pdf_button.clicked.connect(self.generate_pdf)
        button_layout.addWidget(self.pdf_button)
        
        self.new_button = QPushButton("New")
        self.new_button.clicked.connect(lambda: self.new([self.save_button, self.clear_button]))
        button_layout.addWidget(self.new_button)

        self.layout.addLayout(button_layout)

    def save_invoice(self, buttons):
        self.setFocus()
        acc_no = self.acc_no_input.currentText()
        name = self.name_input.currentText()
        bill_no = self.bill_no_input.text()
        
        for i in range(len(buttons)):
            buttons[i].setEnabled(False)
        
        # changed column number
        hsn = [self.table.item(i, 1).text() for i in range(len(self.itemName))]
        qty = [self.table.cellWidget(i, 2).text() for i in range(len(self.itemName))]
        rate = [self.table.cellWidget(i, 3).text() for i in range(len(self.itemName))]
        total = [self.table.item(i, 4).text() for i in range(len(self.itemName))]
        discount = [self.table.cellWidget(i, 5).text() for i in range(len(self.itemName))]
        discountPrice = [self.table.item(i, 6).text() for i in range(len(self.itemName))]
        
        bulk_discount = self.discount_input.text()
        before_tax = self.total_before_tax_input.text()
        sgst = self.sgst_input.text()
        cgst = self.cgst_input.text()
        igst = self.igst_input.text()
        after_tax = self.total_after_tax_input.text()
        for i in range(len(self.itemName)):
            try:
                query = '''INSERT INTO sales_items 
                        (acc_no, state_name, date, name, code, time, gstin, bill_no, itemName, hsnCode, quantity, rate, total, discount, discountedPrice, total_before_tax, total_after_tax) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                
                data = []
                data.append(acc_no)
                data.append(self.state_name_input.text())
                data.append(date.today())
                data.append(name)
                data.append(self.code_input.text())
                data.append(self.time_input.text())
                data.append(self.gstin_input.text())
                data.append(bill_no)
                data.append(self.itemName[i])
                data.append(hsn[i])
                data.append(qty[i])
                data.append(rate[i])
                data.append(total[i])
                data.append(discount[i])
                data.append(discountPrice[i])
                data.append(before_tax)
                data.append(after_tax)
                mycursor.execute(query, data)
                mydb.commit()
                # self.current_record = mycursor.lastrowid
                print("Invoice saved!")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        try:
            query = '''INSERT INTO sales_bills 
                    (acc_no, date, name, bill_no, discount, total_before_tax, sgst, cgst, igst, total_after_tax) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            
            data = []
            data.append(acc_no)
            data.append(date.today())
            data.append(name)
            data.append(bill_no)
            data.append(bulk_discount)
            data.append(before_tax)
            data.append(sgst)
            data.append(cgst)
            data.append(igst)
            data.append(after_tax)
            mycursor.execute(query, data)
            mydb.commit()
            self.current_record = mycursor.lastrowid
            print("Invoice saved!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            
        try:
            query = '''INSERT INTO cust_bal 
                    (date, accNo, cashDebit, cashCredit, billtype, billNo) 
                    VALUES (%s, %s, %s, %s, %s, %s)'''
            
            data = []
            data.append(date.today())
            data.append(acc_no)
            data.append(after_tax)
            data.append(0)
            data.append("Sales Invoice")
            data.append(bill_no)
            mycursor.execute(query, data)
            mydb.commit()
            # self.current_record = self.c.lastrowid
            print("Invoice saved!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        

    def billNum(self):
        from datetime import date
        datee = date.today().day
        billQuery = "SELECT bill_no FROM sales_Bills ORDER BY bill_no DESC LIMIT 1"
        mycursor.execute(billQuery)
        bills = mycursor.fetchone()
        print(bills, "fetched value")
        try:
            bills = bills[0]
            billNo = int(bills) + 1
        except TypeError:
            billNo = "1"
        except ValueError:
            billNo = "1"

        month = str(date.today().month)

        if month == "1" and str(datee) == "1":
            billNo = 1

        billNo = str(billNo)
        print(billNo, "given bill value")
        return billNo


    def printdef(self, billNo, accNo):
        self.pdf()
        location = 'salesBills/' + str(billNo) + "-" + str(accNo) + '.pdf'
        GHOSTSCRIPT_PATH = os.path.join(os.getcwd(), "gs\\gs10.01.2\\bin\\gswin64c")
        if sys.platform == 'win32':
            args = f'"{GHOSTSCRIPT_PATH}" ' \
                    '-sDEVICE=mswinpr2 ' \
                    '-dBATCH ' \
                    '-dNOPAUSE ' \
                    '-dFitPage ' \
                    '-dNOPROMPT ' \
                    '-dPrinted ' \
                    '-sOutputFile="%printer%myPrinterName" '
            ghostscript = args + os.path.join(os.getcwd(), location).replace('\\', '\\\\')
            subprocess.call(ghostscript, shell=True)

            os.remove(location)

    def new(self, buttons):

        currentBill = int(self.bill_no_input.text())
        prevBill = str(currentBill + 1)
        print(self.bill_no_input.text(), "current bill No")
        billQuery = "select count(bill_no) from sales_bills where bill_no = '" + str(int(self.bill_no_input.text()) + 1) + "'"
        mycursor.execute(billQuery)
        billBool = mycursor.fetchone()
        print(billBool[0], "billbool value")
        if billBool[0] == 0 and not int(prevBill) > int(self.billNum()):
            # bill doesnt exist
            self.clear_table()
            print(self.billNum(), "bill nO function")
            newBill = self.billNum()
            self.bill_no_input.setText(newBill)
            self.date_input.setText(str(date.today()))
            # Enable the other buttons to allow changes
            for i in range(len(buttons)):
                buttons[i].setEnabled(True)
        else:
            # self.dialog = errPopup("Bill doesn't exist")
            # self.dialog.show()
            pass

        if billBool[0] == 1:
            # self.dialog = errPopup("Bill number already in use")
            # self.dialog.show()
            pass


    def load_invoice(self, invoice_id):
        mycursor.execute("SELECT * FROM sales_bills WHERE bill_no=%s", (invoice_id,))
        record = mycursor.fetchone()
        print(record[2], "acc_no")
        if record:
            self.acc_no_input.setCurrentIndex(record[2]-1)
            self.bill_no_input.setText(str(record[4]))
            self.sgst_input.setText(str(record[7]))
            self.cgst_input.setText(str(record[8]))
            self.igst_input.setText(str(record[9]))

            # for row in range(len(items)):
            #     self.table.setItem(row, 0, QTableWidgetItem(items[row]["description"]))
            #     self.table.setItem(row, 1, QTableWidgetItem(items[row]["hsn_code"]))
            #     self.table.cellWidget(row, 2).setText(items[row]["quantity"])
            #     self.table.cellWidget(row, 3).setText(items[row]["rate"])
            #     self.table.setItem(row, 4, QTableWidgetItem(items[row]["total"]))
            #     self.table.cellWidget(row, 5).setText(items[row]["discount"])
            #     self.table.setItem(row, 6, QTableWidgetItem(items[row]["discounted_price"]))

            # self.total_before_tax_input.setText(str(record[10]))
            # self.sgst_input.setText(str(record[11]))
            # self.cgst_input.setText(str(record[12]))
            # self.igst_input.setText(str(record[13]))
            # self.total_after_tax_input.setText(str(record[14]))
            
        mycursor.execute("SELECT * FROM sales_items WHERE bill_no=%s", (invoice_id,))
        record = mycursor.fetchall()
        
        if record:
            for row in range(len(record)):
                
                self.table.cellWidget(row, 0).setText(record[row][9])
                self.table.setItem(row, 1, QTableWidgetItem(record[row][10]))
                self.table.cellWidget(row, 2).setText(str(record[row][11]))
                self.table.cellWidget(row, 3).setText(str(record[row][12]))
                # self.table.setItem(row, 4, QTableWidgetItem(record[row][12]))
                self.table.cellWidget(row, 5).setText(str(record[row][14]))
                # self.table.setItem(row, 6, QTableWidgetItem(record[row][14]))
            self.state_name_input.setText(record[0][2])
            self.date_input.setText(record[0][3])
            self.code_input.setText(record[0][5])
            self.time_input.setText(record[0][6])
            
                

    def load_next(self):
        if self.current_record is None:
            mycursor.execute("SELECT bill_no FROM sales_bills ORDER BY bill_no ASC LIMIT 1")
        else:
            mycursor.execute("SELECT bill_no FROM sales_bills WHERE bill_no > %s ORDER BY bill_no ASC LIMIT 1", (self.bill_no_input.text(),))
        
        result = mycursor.fetchone()
        if result:
            self.current_record = result[0]
            self.load_invoice(self.current_record)

    def load_previous(self):
        if self.current_record is None:
            mycursor.execute("SELECT bill_no FROM sales_bills ORDER BY bill_no DESC LIMIT 1")
        else:
            mycursor.execute("SELECT bill_no FROM sales_bills WHERE bill_no < %s ORDER BY bill_no DESC LIMIT 1", (self.bill_no_input.text(),))

        result = mycursor.fetchone()
        if result:
            self.current_record = result[0]
            self.load_invoice(self.current_record)
    def generate_pdf(self):
        if self.current_record is None:
            print("No invoice loaded to generate PDF.")
            return

        self.c.execute("SELECT * FROM invoices WHERE id=%s", (self.current_record,))
        record = self.c.fetchone()

        if not record:
            print("No data found for the current invoice.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Sales Invoice", ln=True, align="C")

        pdf.cell(100, 10, txt=f"Acc No: {record[1]}", ln=True)
        pdf.cell(100, 10, txt=f"State Name: {record[2]}", ln=True)
        pdf.cell(100, 10, txt=f"Date: {record[3]}", ln=True)
        pdf.cell(100, 10, txt=f"Name: {record[4]}", ln=True)
        pdf.cell(100, 10, txt=f"Code: {record[5]}", ln=True)
        pdf.cell(100, 10, txt=f"Time: {record[6]}", ln=True)
        pdf.cell(100, 10, txt=f"GSTIN: {record[7]}", ln=True)
        pdf.cell(100, 10, txt=f"Bill No: {record[8]}", ln=True)

        pdf.cell(200, 10, txt="Items", ln=True)
        items = eval(record[9])
        for item in items:
            pdf.cell(200, 10, txt=f"Description: {item['description']}, HSN Code: {item['hsn_code']}, Quantity: {item['quantity']}, Rate: {item['rate']}, Total: {item['total']}, Discount: {item['discount']}, Discounted Price: {item['discounted_price']}", ln=True)

        pdf.cell(200, 10, txt=f"Total before tax: {record[10]}", ln=True)
        pdf.cell(200, 10, txt=f"SGST: {record[11]}", ln=True)
        pdf.cell(200, 10, txt=f"CGST: {record[12]}", ln=True)
        pdf.cell(200, 10, txt=f"IGST: {record[13]}", ln=True)
        pdf.cell(200, 10, txt=f"Total after tax: {record[14]}", ln=True)

        pdf.output("invoice.pdf")
        print("PDF generated!")

    def closeEvent(self, event):
        self.conn.close()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainWindow = SalesInvoice()
#     mainWindow.show()
#     sys.exit(app.exec_())