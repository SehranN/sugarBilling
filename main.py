import os
from datetime import date, datetime
# Hello manan
import mysql.connector
# Hello from Sehran
from hijri_converter import Hijri, Gregorian
from num2words import num2words
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
import sys
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
from googletrans import Translator

from backup import BackupApp
from settings import Settings
import openpyxl


mydb = mysql.connector.connect(
    # trail3server.mysql.database.azure.com
    # host= "trail3server.mysql.database.azure.com",
    # user="sehran",
    # passwd="Noor123!@",
    # port=3306,
    host= "localhost",
    user="root",
    passwd="Somsoc1retupmoc",
    port=3306,

)

mycursor = mydb.cursor()
# connect and create database
mycursor.execute("CREATE DATABASE IF NOT EXISTS sugarBilling")
#
#
# # connect to server
import Sales_Invoice
# import Sales_Ret_Invoice
# import Purchase_Invoice
# import Purchase_Ret_Invoice
# import Expenses
import TotalBalance
# import TotalExpBalance
import addClients
# import addExpItem
# import addItems
import getClients
# import getExpItems
# import getItems
import utils

from utils import errPopup


mydb = utils.connection
mycursor = mydb.cursor()

# create tables
stmt = "SHOW TABLES LIKE 'Sales_Items'"
mycursor.execute(stmt)
result = mycursor.fetchone()
if result:
    pass
else:
    mycursor.execute(
        '''CREATE TABLE IF NOT EXISTS Sales_Items (id INT AUTO_INCREMENT PRIMARY KEY,
            acc_no INTEGER(10),
            state_name VARCHAR(255),
            date VARCHAR(255),
            name VARCHAR(255),
            code VARCHAR(255),
            time VARCHAR(255),
            gstin VARCHAR(255),
            bill_no INTEGER(10),
            itemName VARCHAR(255),
            hsnCode VARCHAR(255),
            quantity FLOAT(10),
            rate FLOAT(10),
            total FLOAT(10),
            discount FLOAT(10),
            discountedPrice FLOAT(10),
            total_before_tax FLOAT(10),
            total_after_tax FLOAT(10))''')

stmt = "SHOW TABLES LIKE 'Sales_Bills'"
mycursor.execute(stmt)
result = mycursor.fetchone()
if result:
    pass
else:
    mycursor.execute(
        '''CREATE TABLE Sales_Bills (id INT AUTO_INCREMENT PRIMARY KEY,
        date VARCHAR(255),
        acc_no INTEGER(10),
        name VARCHAR(255),
        bill_no INTEGER(10),
        discount FLOAT(10),
        total_before_tax FLOAT(10),
        sgst FLOAT(10),
        cgst FLOAT(10),
        igst FLOAT(10),
        total_after_tax FLOAT(10))''')


# stmt = "SHOW TABLES LIKE 'SalesRet_Items'"
# mycursor.execute(stmt)
# result = mycursor.fetchone()
# if result:
#     pass
# else:
#     mycursor.execute(
#         "CREATE TABLE SalesRet_Items (date VARCHAR(255),accNo INTEGER(10),name VARCHAR(255),itemName VARCHAR(255), notes VARCHAR(255), rate FLOAT(20), quantity FLOAT(20), total FLOAT(20), transport FLOAT(20), gTotal FLOAT(20),  billNo INTEGER(20),sNo INTEGER(10) NOT NULL AUTO_INCREMENT PRIMARY KEY)")

# stmt = "SHOW TABLES LIKE 'SalesRet_Bills'"
# mycursor.execute(stmt)
# result = mycursor.fetchone()
# if result:
#     pass
# else:
#     mycursor.execute(
#         "CREATE TABLE SalesRet_Bills (date VARCHAR(255),accNo INTEGER(10),name VARCHAR(255),totalQuantity FLOAT(20),totalAmount FLOAT(20),totalTransport FLOAT(20), grandTotal FLOAT(20),billNo INTEGER(20),sNo INTEGER(10) NOT NULL AUTO_INCREMENT PRIMARY KEY)")



# stmt = "SHOW TABLES LIKE 'Purchase_Bills'"
# mycursor.execute(stmt)
# result = mycursor.fetchone()
# if result:
#     pass
# else:
#     mycursor.execute(
#         "CREATE TABLE Purchase_Bills (date VARCHAR(255),accNo INTEGER(10),name VARCHAR(255),totalQuantity FLOAT(20),totalAmount FLOAT(20),totalTransport FLOAT(20), grandTotal FLOAT(20),billNo INTEGER(20),sNo INTEGER(10) NOT NULL AUTO_INCREMENT PRIMARY KEY)")

# stmt = "SHOW TABLES LIKE 'Purchase_Items'"
# mycursor.execute(stmt)
# result = mycursor.fetchone()
# if result:
#     pass
# else:
#     mycursor.execute(
#         "CREATE TABLE Purchase_Items (date VARCHAR(255),accNo INTEGER(10),name VARCHAR(255),itemName VARCHAR(255), notes VARCHAR(255), rate FLOAT(20), quantity FLOAT(20), total FLOAT(20), transport FLOAT(20), gTotal FLOAT(20),  billNo INTEGER(20),sNo INTEGER(10) NOT NULL AUTO_INCREMENT PRIMARY KEY)")

# stmt = "SHOW TABLES LIKE 'PurchaseRet_Bills'"
# mycursor.execute(stmt)
# result = mycursor.fetchone()
# if result:
#     pass
# else:
#     mycursor.execute(
#         "CREATE TABLE PurchaseRet_Bills (date VARCHAR(255),accNo INTEGER(10),name VARCHAR(255),totalQuantity FLOAT(20),totalAmount FLOAT(20),totalTransport FLOAT(20), grandTotal FLOAT(20),billNo INTEGER(20),sNo INTEGER(10) NOT NULL AUTO_INCREMENT PRIMARY KEY)")

# stmt = "SHOW TABLES LIKE 'PurchaseRet_Items'"
# mycursor.execute(stmt)
# result = mycursor.fetchone()
# if result:
#     pass
# else:
#     mycursor.execute(
#         "CREATE TABLE PurchaseRet_Items (date VARCHAR(255),accNo INTEGER(10),name VARCHAR(255),itemName VARCHAR(255), notes VARCHAR(255), rate FLOAT(20), quantity FLOAT(20), total FLOAT(20), transport FLOAT(20), gTotal FLOAT(20),  billNo INTEGER(20),sNo INTEGER(10) NOT NULL AUTO_INCREMENT PRIMARY KEY)")




stmt = "SHOW TABLES LIKE 'Customer'"
mycursor.execute(stmt)
result = mycursor.fetchone()
if result:
    pass
else:
    mycursor.execute("CREATE TABLE Customer (accNo INTEGER(10) NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255),"
                     "phnNo VARCHAR(255), email VARCHAR(255), company VARCHAR(255), GSTIN VARCHAR(255),"
                     "address VARCHAR(255), oldCash FLOAT(10))"
                     )
# stmt = "SHOW TABLES LIKE 'Items'"
# mycursor.execute(stmt)
# result = mycursor.fetchone()
# if result:
#     pass
# else:
#     mycursor.execute(
#         "CREATE TABLE Items (Item_No INTEGER(10) NOT NULL AUTO_INCREMENT PRIMARY KEY, Item_Name VARCHAR(255),"
#         "Rate FLOAT(10), type VARCHAR(255))"
#         )

    # sqlFormula = "INSERT INTO Items (Item_Name,Purity,Labour, Vat) VALUES (%s,%s,%s,%s) "
    # details = ["cash", "0", "0", "0"]
    # try:
    #     mycursor.execute(sqlFormula, details)
    #     mydb.commit()
    # except:
    #     dialog = errPopup("items setup")
    #     dialog.show()

# stmt = "SHOW TABLES LIKE 'Payable_Items'"
# mycursor.execute(stmt)
# result = mycursor.fetchone()
# if result:
#     pass
# else:
#     mycursor.execute("CREATE TABLE Payable_Items (date VARCHAR(255), accNo INTEGER(10), name VARCHAR(255),"
#                      "itemName VARCHAR(255), notes VARCHAR(255), grossW FLOAT(20),"
#                      "K FLOAT(20),baseW FLOAT(20), cash FLOAT(20), labour FLOAT(20), totalLabour FLOAT(20)"
#                      ", billNo INTEGER(20), sNo INTEGER(10) NOT NULL AUTO_INCREMENT PRIMARY KEY)"
#                      )

# stmt = "SHOW TABLES LIKE 'Payable_Bills'"
# mycursor.execute(stmt)
# result = mycursor.fetchone()
# if result:
#     pass
# else:
#     mycursor.execute("CREATE TABLE Payable_Bills (date VARCHAR(255), accNo INTEGER(10), name VARCHAR(255),"
#                      "totalGross FLOAT(20), totalBase FLOAT(20), totalCash FLOAT(20), totalLabour FLOAT(20),"
#                      "grandTotal FLOAT(20), billNo INTEGER(20), sNo INTEGER(10) NOT NULL AUTO_INCREMENT PRIMARY KEY)"
#                      )

# stmt = "SHOW TABLES LIKE 'Recieving_Items'"
# mycursor.execute(stmt)
# result = mycursor.fetchone()
# if result:
#     pass
# else:
#     mycursor.execute("CREATE TABLE Recieving_Items (date VARCHAR(255), accNo INTEGER(10), name VARCHAR(255),"
#                      "itemName VARCHAR(255), notes VARCHAR(255), grossW FLOAT(20),"
#                      "K FLOAT(20),baseW FLOAT(20), cash FLOAT(20), labour FLOAT(20), totalLabour FLOAT(20)"
#                      ", billNo INTEGER(20), sNo INTEGER(10) NOT NULL AUTO_INCREMENT PRIMARY KEY)"
#                      )

# stmt = "SHOW TABLES LIKE 'Recieving_Bills'"
# mycursor.execute(stmt)
# result = mycursor.fetchone()
# if result:
#     pass
# else:
#     mycursor.execute("CREATE TABLE Recieving_Bills (date VARCHAR(255), accNo INTEGER(10), name VARCHAR(255),"
#                      "totalGross FLOAT(20), totalBase FLOAT(20), totalCash FLOAT(20), totalLabour FLOAT(20),"
#                      "grandTotal FLOAT(20), billNo INTEGER(20), sNo INTEGER(10) NOT NULL AUTO_INCREMENT PRIMARY KEY)"
#                      )

stmt = "SHOW TABLES LIKE 'Cust_Bal'"
mycursor.execute(stmt)
result = mycursor.fetchone()
if result:
    pass
else:
    mycursor.execute(
        "CREATE TABLE Cust_Bal (date VARCHAR(255), accNo VARCHAR(255), cashDebit FLOAT(15), cashCredit FLOAT(20), billType VARCHAR(255), billNo INTEGER(20), sNo INTEGER(10) NOT NULL AUTO_INCREMENT PRIMARY KEY)"
        )


# stmt = "SHOW TABLES LIKE 'expenseBalance'"
# mycursor.execute(stmt)

# result = mycursor.fetchone()
# if result:
#     pass
# else:
#     mycursor.execute(
#         "CREATE TABLE expenseBalance (id INT AUTO_INCREMENT PRIMARY KEY, Date VARCHAR(255), Item_Name VARCHAR(255), Amount FLOAT(20), Notes VARCHAR(255))")

# stmt = "SHOW TABLES LIKE 'Exp_Items'"
# mycursor.execute(stmt)
# result = mycursor.fetchone()
# if result:
#     pass
# else:
#     mycursor.execute("CREATE TABLE Exp_Items (Item_No INT AUTO_INCREMENT PRIMARY KEY, Item_Name VARCHAR(255))")
#     itemsreq = ["Disel Purchase", "Iqama Visa", "Canteen Expenses", "Labour Food", "Electric Bill", "Main Equipment Purchase",
#                 "International Equipment Purchase", "Cargo Shipment Charge", "Salary", "Overtime", "Petrol Company", "Motor Vehicle Repairing",
#                 "Machine Equipment Repairing", "Abreez AL Nader Co. Expenses", "Others"]
#     sqlFormula = "INSERT INTO Exp_Items (Item_Name) VALUES (%s) "
#     for i in range(14):
#         details = [itemsreq[i]]
#         try:
#             mycursor.execute(sqlFormula, details)
#             mydb.commit()
#         except:
#             dialog = errPopup("expense items setup")
#             dialog.show()

class Box(QWidget):

    def __init__(self, color):
        super(Box, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 100, 1200, 800)
        
        # defining all the rows for the layout
        row1 = Box("black")
        # defining header
        horiz_1 = QHBoxLayout(row1)
        horiz_1_r1 = Box("white")
        # logo and name goes here
        horiz_1_r2 = Box("white")
        horiz_1_1 = QHBoxLayout(horiz_1_r2)
        pixmap = QPixmap('items/Logo.jpg')
        smaller_pix = pixmap.scaled(32, 64, Qt.KeepAspectRatio)
        image = QLabel()
        image.setPixmap(smaller_pix)
        self.name = QLabel("Shree Krishna Traders")
        self.name.setStyleSheet("font-size: 22pt;"
                           "color: black")
        # horiz_1_1.addWidget(image)
        horiz_1_1.addWidget(self.name)
        horiz_1_r3 = Box("white")
        # putting the widgets in
        horiz_1.addWidget(horiz_1_r1)
        horiz_1.addWidget(horiz_1_r2)
        horiz_1.addWidget(horiz_1_r3)

        row2 = Box("white")
        row3 = Box("black")
        # defining row 1
        horiz_2 = QHBoxLayout(row3)
        horiz_2_r1 = Box("white")
        # salesBtn
        self.salesBtn = QPushButton("Sales Invoice")
        self.salesBtn.setStyleSheet("color: black")
        self.salesBtn.clicked.connect(self.open_sales)
        horiz_2_1 = QHBoxLayout(horiz_2_r1)
        horiz_2_1.addWidget(self.salesBtn)
        horiz_2_r2 = Box("white")
        # recivingBtn
        self.recieveBtn = QPushButton("Customer Recieveable")
        self.recieveBtn.setStyleSheet("color: black")
        self.recieveBtn.clicked.connect(self.open_return)
        horiz_2_2 = QHBoxLayout(horiz_2_r2)
        horiz_2_2.addWidget(self.recieveBtn)
        horiz_2_r3 = Box("white")
        # expenseBtn
        self.expBtn = QPushButton("Expenses Invoice")
        self.expBtn.setStyleSheet("color: black")
        self.expBtn.clicked.connect(self.open_expense)
        horiz_2_3 = QHBoxLayout(horiz_2_r3)
        horiz_2_3.addWidget(self.expBtn)
        horiz_2_r4 = Box("white")
        # salesRetBtn
        self.salesRetBtn = QPushButton("Sales Return")
        self.salesRetBtn.setStyleSheet("color: black")
        self.salesRetBtn.clicked.connect(self.open_salesRet)
        horiz_2_4 = QHBoxLayout(horiz_2_r4)
        horiz_2_4.addWidget(self.salesRetBtn)
        horiz_2_r5 = Box("white")
        # salesRetBtn
        self.payBtn = QPushButton("Customer payable")
        self.payBtn.setStyleSheet("color: black")
        self.payBtn.clicked.connect(self.open_pay)
        horiz_2_5 = QHBoxLayout(horiz_2_r5)
        horiz_2_5.addWidget(self.payBtn)
        horiz_2_r6 = Box("white")
        # PurchaseBtn
        self.purchBtn = QPushButton("Purchase Invoice")
        self.purchBtn.setStyleSheet("color: black")
        self.purchBtn.clicked.connect(self.open_purch)
        horiz_2_6 = QHBoxLayout(horiz_2_r6)
        horiz_2_6.addWidget(self.purchBtn)
        horiz_2_r7 = Box("white")
        # PurchaseRetBtn
        self.purchRetBtn = QPushButton("Purchase Return Invoice")
        self.purchRetBtn.setStyleSheet("color: black")
        self.purchRetBtn.clicked.connect(self.open_purchRet)
        horiz_2_7 = QHBoxLayout(horiz_2_r7)
        horiz_2_7.addWidget(self.purchRetBtn)
        # putting the widgets in
        horiz_2.addWidget(horiz_2_r1)
        # horiz_2.addWidget(horiz_2_r4)
        # horiz_2.addWidget(horiz_2_r2)
        # horiz_2.addWidget(horiz_2_r5)
        # horiz_2.addWidget(horiz_2_r6)
        # horiz_2.addWidget(horiz_2_r7)
        # horiz_2.addWidget(horiz_2_r3)
        row4 = Box("white")
        row5 = Box("black")
        # defining row 2
        horiz_3 = QHBoxLayout(row5)
        horiz_3_r1 = Box("white")
        # grandTotBtn
        self.grandTotBtn = QPushButton("Total Balance")
        self.grandTotBtn.setStyleSheet("color: black")
        self.grandTotBtn.clicked.connect(self.open_total)
        horiz_3_1 = QHBoxLayout(horiz_3_r1)
        horiz_3_1.addWidget(self.grandTotBtn)
        horiz_3_r2 = Box("white")
        # custBalBtn
        self.custBalBtn = QPushButton("Customer Balance")
        self.custBalBtn.setStyleSheet("color: black")
        self.custBalBtn.clicked.connect(self.open_custBal)
        horiz_3_2 = QHBoxLayout(horiz_3_r2)
        horiz_3_2.addWidget(self.custBalBtn)
        horiz_3_r3 = Box("white")
        # manCustBtn
        self.manCustBtn = QPushButton("Bill Balance")
        self.manCustBtn.setStyleSheet("color: black")
        self.manCustBtn.clicked.connect(self.open_Bill)
        horiz_3_3 = QHBoxLayout(horiz_3_r3)
        horiz_3_3.addWidget(self.manCustBtn)
        horiz_3_r4 = Box("white")
        # total exp
        self.expBalance = QPushButton("Total Expense Balance")
        self.expBalance.setStyleSheet("color: black")
        self.expBalance.clicked.connect(self.open_expenseTotal)
        horiz_3_4 = QHBoxLayout(horiz_3_r4)
        horiz_3_4.addWidget(self.expBalance)
        horiz_3_r5 = Box("white")
        # total exp
        self.expSpBalance = QPushButton("Specific Expense Balance")
        self.expSpBalance.setStyleSheet("color: black")
        self.expSpBalance.clicked.connect(self.open_expenseSp)
        horiz_3_5 = QHBoxLayout(horiz_3_r5)
        horiz_3_5.addWidget(self.expSpBalance)
        # putting the widgets in
        horiz_3.addWidget(horiz_3_r1)
        # horiz_3.addWidget(horiz_3_r2)
        # horiz_3.addWidget(horiz_3_r3)
        # horiz_3.addWidget(horiz_3_r4)
        # horiz_3.addWidget(horiz_3_r5)
        row6 = Box("white")
        row7 = Box("black")
        # defining row 3
        horiz_4 = QHBoxLayout(row7)
        horiz_4_r1 = Box("white")
        # add itemsBtn
        self.itemsBtn = QPushButton("Add Items")
        self.itemsBtn.setStyleSheet("color: black")
        self.itemsBtn.clicked.connect(self.add_Item)
        horiz_4_1 = QHBoxLayout(horiz_4_r1)
        horiz_4_1.addWidget(self.itemsBtn)
        horiz_4_r2 = Box("white")
        # view Items Btn
        self.vItemsBtn = QPushButton("View Items")
        self.vItemsBtn.setStyleSheet("color: black")
        self.vItemsBtn.clicked.connect(self.show_Item)
        horiz_4_2 = QHBoxLayout(horiz_4_r2)
        horiz_4_2.addWidget(self.vItemsBtn)
        horiz_4_r3 = Box("white")
        # add customer
        self.custBtn = QPushButton("Add Customer")
        self.custBtn.setStyleSheet("color: black")
        self.custBtn.clicked.connect(self.add_Cust)
        horiz_4_3 = QHBoxLayout(horiz_4_r3)
        horiz_4_3.addWidget(self.custBtn)
        horiz_4_r4 = Box("white")
        # view Customer Btn
        self.vCustBtn = QPushButton("View Customer")
        self.vCustBtn.setStyleSheet("color: black")
        self.vCustBtn.clicked.connect(self.show_Cust)
        horiz_4_4 = QHBoxLayout(horiz_4_r4)
        horiz_4_4.addWidget(self.vCustBtn)
        horiz_4_r5 = Box("white")
        # add itemsExpBtn
        self.itemsExpBtn = QPushButton("Add Expense Items")
        self.itemsExpBtn.setStyleSheet("color: black")
        self.itemsExpBtn.clicked.connect(self.add_ExpItem)
        horiz_4_5 = QHBoxLayout(horiz_4_r5)
        horiz_4_5.addWidget(self.itemsExpBtn)
        horiz_4_r6 = Box("white")
        # view Items Exp Btn
        self.vItemsExpBtn = QPushButton("View Expense Items")
        self.vItemsExpBtn.setStyleSheet("color: black")
        self.vItemsExpBtn.clicked.connect(self.show_ExpItem)
        horiz_4_6 = QHBoxLayout(horiz_4_r6)
        horiz_4_6.addWidget(self.vItemsExpBtn)
        horiz_4_r7 = Box("white")
        # backup
        self.backupBtn = QPushButton("Backup")
        self.backupBtn.setStyleSheet("color: black")
        backupfunct = BackupApp()
        self.backupBtn.clicked.connect(lambda: backupfunct.show())
        horiz_4_7 = QHBoxLayout(horiz_4_r7)
        horiz_4_7.addWidget(self.backupBtn)
        horiz_4_r8 = Box("white")
        # backup
        self.settingsBtn = QPushButton("Settings")
        self.settingsBtn.setStyleSheet("color: black")
        settingfunct = Settings()
        self.settingsBtn.clicked.connect(lambda: settingfunct.show())
        horiz_4_8 = QHBoxLayout(horiz_4_r8)
        horiz_4_8.addWidget(self.settingsBtn)
        
        
        # putting the widgets in
        # horiz_4.addWidget(horiz_4_r1)
        # horiz_4.addWidget(horiz_4_r2)
        horiz_4.addWidget(horiz_4_r3)
        horiz_4.addWidget(horiz_4_r4)
        # horiz_4.addWidget(horiz_4_r5)
        # horiz_4.addWidget(horiz_4_r6)
        # horiz_4.addWidget(horiz_4_r7)
        # horiz_4.addWidget(horiz_4_r8)
        row8 = Box("white")

        mainBox = Box("white")
        mainLayout = QVBoxLayout(mainBox)
        mainLayout.addWidget(row1)
        mainLayout.addWidget(row2)
        mainLayout.addWidget(row3)
        mainLayout.addWidget(row4)
        mainLayout.addWidget(row5)
        mainLayout.addWidget(row6)
        mainLayout.addWidget(row7)
        mainLayout.addWidget(row8)
        

        # Add the backup button to your layout
        

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
        self.toggle_translate()
        
        

    
    def toggle_translate(self):
        workbook = openpyxl.load_workbook('settings.xlsx')
        worksheet = workbook.active
        if (worksheet["B2"].value == "arabic"):
            translator = Translator()

            self.name.setText(str(translator.translate(self.name.text(), dest="ar").text))
            
            self.salesBtn.setText(str(translator.translate(self.salesBtn.text(), dest="ar").text))
            self.salesRetBtn.setText(str(translator.translate(self.salesRetBtn.text(), dest="ar").text))
            self.recieveBtn.setText(str(translator.translate(self.recieveBtn.text(), dest="ar").text))
            self.payBtn.setText(str(translator.translate(self.payBtn.text(), dest="ar").text))
            self.purchBtn.setText(str(translator.translate(self.purchBtn.text(), dest="ar").text))
            self.purchRetBtn.setText(str(translator.translate(self.purchRetBtn.text(), dest="ar").text))
            
            self.grandTotBtn.setText(str(translator.translate(self.grandTotBtn.text(), dest="ar").text))
            self.custBalBtn.setText(str(translator.translate(self.custBalBtn.text(), dest="ar").text))
            self.manCustBtn.setText(str(translator.translate(self.manCustBtn.text(), dest="ar").text))
            
            self.itemsBtn.setText(str(translator.translate(self.itemsBtn.text(), dest="ar").text))
            self.vItemsBtn.setText(str(translator.translate(self.vItemsBtn.text(), dest="ar").text))
            self.custBtn.setText(str(translator.translate(self.custBtn.text(), dest="ar").text))
            self.vCustBtn.setText(str(translator.translate(self.vCustBtn.text(), dest="ar").text))
            self.backupBtn.setText(str(translator.translate(self.backupBtn.text(), dest="ar").text))
            self.settingsBtn.setText(str(translator.translate(self.settingsBtn.text(), dest="ar").text))
        
        
        
    

    def ad_backup(self):
       self.backup_data()
       
    def add_ExpItem(self):
        self.add_ExpItem()
        
    def add_Cust(self):

        self.w = addClients.addClient()
        self.w.show()

    def add_Item(self):

        # self.w = addItems.addItems()
        # self.w.show()
        pass

    def show_Cust(self):
        self.w = getClients.getClients()
        self.w.show()

    def show_Item(self):
        # self.w = getItems.viewItems()
        # self.w.show()
        pass

    def open_sales(self):

        self.w = Sales_Invoice.SalesInv()
        self.w.show()

    def open_return(self):

        # self.w = Recieving_Invoice_New.RecieveInv()
        # self.w.show()
        pass

    def open_pay(self):
        # self.w = paybleInvoice.payableInv()
        # self.w.show()
        pass

    def open_salesRet(self):
        # self.w = Sales_Ret_Invoice.SalesRetInv()
        # self.w.show()
        pass

    def open_total(self):
        self.w = TotalBalance.totalBalance()
        self.w.show()

    def open_custBal(self):
        # self.w = SpecificCustBal.customerBalance()
        # self.w.show()
        pass

    def open_Bill(self):
        # self.w = SpecificBillBalance.billBalance()
        # self.w.show()
        pass

    def open_expense(self):
        # self.w = Expenses.Expenses()
        # self.w.show()
        pass

    def open_expenseTotal(self):
        # self.w = TotalExpBalance.totalWindow()
        # self.w.show()
        pass

    def open_expenseSp(self):
        # self.w = expenseSpecs.specBalance()
        # self.w.show()
        pass

    def open_purch(self):
        # self.w = Purchase_Invoice.PurchaseInv()
        # self.w.show()
        pass

    def open_purchRet(self):
        # self.w = Purchase_Ret_Invoice.PurchaseRetInv()
        # self.w.show()
        pass
    def add_ExpItem(self):

        # self.w = addExpItem.addExpItems()
        # self.w.show()
        pass

    def show_ExpItem(self):
        # self.w = getExpItems.viewExpItems()
        # self.w.show()
        pass


    def makeFolders(self):

        path = ['TotalBalance', 'SpecificCustTotal', 'SpecificBillTotal', 'bills', 'payBills',
                'recieveBills', 'retBills','purchBills', 'purchRetBills','TotalBills', 'Spec',
                'Total-Break']

        for i in range(len(path)):
            try:
                os.makedirs(path[i], mode=0o777, exist_ok=False)
            except OSError as error:
                self.dialog = errPopup("Folder Creation error")
                self.dialog.show()


app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()

