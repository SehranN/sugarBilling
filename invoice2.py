import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QTableWidget, QTableWidgetItem, QGroupBox, QFormLayout, QHeaderView, QPushButton
from fpdf import FPDF
import mysql.connector
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel, QGridLayout

class SalesInvoiceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Invoice")
        self.setGeometry(100, 100, 900, 600)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)

        self.create_header()
        self.create_table()
        self.create_summary()
        self.create_footer()
        self.create_buttons()

        self.current_record = None  # To keep track of the current record index

        self.connect_db()

    def connect_db(self):
     self.conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Daddy@123",
        port=3306,
        database='billing'
    )
     self.c = self.conn.cursor()

     self.c.execute('''CREATE TABLE IF NOT EXISTS invoices (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        acc_no VARCHAR(255),
                        state_name VARCHAR(255),
                        date DATE,
                        name VARCHAR(255),
                        code VARCHAR(255),
                        time TIME,
                        gstin VARCHAR(255),
                        bill_no VARCHAR(255),
                        items TEXT,
                        total_before_tax FLOAT,
                        sgst FLOAT,
                        cgst FLOAT,
                        igst FLOAT,
                        total_after_tax FLOAT
                    )''')
     self.conn.commit()

    def create_header(self):
        header_layout = QGridLayout()

        header_layout.addWidget(QLabel("Acc No"), 0, 0)
        self.acc_no_input = QLineEdit()
        header_layout.addWidget(self.acc_no_input, 0, 1)

        header_layout.addWidget(QLabel("State Name"), 0, 2)
        self.state_name_input = QLineEdit()
        header_layout.addWidget(self.state_name_input, 0, 3)

        header_layout.addWidget(QLabel("Date"), 0, 4)
        self.date_input = QLineEdit()
        header_layout.addWidget(self.date_input, 0, 5)

        header_layout.addWidget(QLabel("Name"), 1, 0)
        self.name_input = QLineEdit()
        header_layout.addWidget(self.name_input, 1, 1)

        header_layout.addWidget(QLabel("Code"), 1, 2)
        self.code_input = QLineEdit()
        header_layout.addWidget(self.code_input, 1, 3)

        header_layout.addWidget(QLabel("Time"), 1, 4)
        self.time_input = QLineEdit()
        header_layout.addWidget(self.time_input, 1, 5)

        header_layout.addWidget(QLabel("GSTIN"), 2, 0)
        self.gstin_input = QLineEdit()
        header_layout.addWidget(self.gstin_input, 2, 1)

        header_layout.addWidget(QLabel("Bill No"), 2, 2)
        self.bill_no_input = QLineEdit()
        header_layout.addWidget(self.bill_no_input, 2, 3)

        self.layout.addLayout(header_layout)

    def create_table(self):
        table_layout = QVBoxLayout()

        self.table = QTableWidget(5, 7)
        self.table.setHorizontalHeaderLabels(
            ["Description of goods", "HSN Code", "Quantity", "Rate", "Total", "Discount", "Discounted price"])

        # Stretch columns to fit the available space
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Connect Quantity, Rate, and Discount cells to the calculation function
        for row in range(self.table.rowCount()):
            quantity_item = QLineEdit()
            quantity_item.setPlaceholderText("0")
            self.table.setCellWidget(row, 2, quantity_item)

            rate_item = QLineEdit()
            rate_item.setPlaceholderText("0")
            self.table.setCellWidget(row, 3, rate_item)

            discount_item = QLineEdit()
            discount_item.setPlaceholderText("0")
            self.table.setCellWidget(row, 5, discount_item)

            quantity_item.editingFinished.connect(self.update_totals)
            rate_item.editingFinished.connect(self.update_totals)
            discount_item.editingFinished.connect(self.update_totals)

        table_layout.addWidget(self.table)
        self.layout.addLayout(table_layout)

    def update_totals(self):
        for row in range(self.table.rowCount()):
            quantity_widget = self.table.cellWidget(row, 2)
            rate_widget = self.table.cellWidget(row, 3)
            discount_widget = self.table.cellWidget(row, 5)

            if quantity_widget and rate_widget and discount_widget:
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

    def create_summary(self):
        summary_layout = QGridLayout()

        summary_layout.addWidget(QLabel("Discount"), 0, 0)
        self.discount_input = QLineEdit()
        summary_layout.addWidget(self.discount_input, 0, 1)

        summary_layout.addWidget(QLabel("Total before tax"), 1, 0)
        self.total_before_tax_input = QLineEdit()
        summary_layout.addWidget(self.total_before_tax_input, 1, 1)

        summary_layout.addWidget(QLabel("Add SGST"), 2, 0)
        self.sgst_input = QLineEdit()
        summary_layout.addWidget(self.sgst_input, 2, 1)

        summary_layout.addWidget(QLabel("Add CGST"), 3, 0)
        self.cgst_input = QLineEdit()
        summary_layout.addWidget(self.cgst_input, 3, 1)

        summary_layout.addWidget(QLabel("Add IGST"), 4, 0)
        self.igst_input = QLineEdit()
        summary_layout.addWidget(self.igst_input, 4, 1)

        summary_layout.addWidget(QLabel("Total after tax"), 5, 0)
        self.total_after_tax_input = QLineEdit()
        summary_layout.addWidget(self.total_after_tax_input, 5, 1)

        self.layout.addLayout(summary_layout)

    def create_footer(self):
     footer_layout = QVBoxLayout()

    
     self.footer_table = QTableWidget(1, 4)
    
    # Set the headers for the table
     self.footer_table.setHorizontalHeaderLabels(["Acc No", "Name", "Debit", "Credit"])
    
    # Make sure the table stretches across the entire window width
     self.footer_table.horizontalHeader().setStretchLastSection(True)
     self.footer_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    
    
    # Add the table to the layout
     footer_layout.addWidget(self.footer_table)
    
    # Add the footer layout to the main layout
     self.layout.addLayout(footer_layout)

    def create_buttons(self):
        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_invoice)
        button_layout.addWidget(self.save_button)

        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.load_previous)
        button_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.load_next)
        button_layout.addWidget(self.next_button)

        self.pdf_button = QPushButton("PDF")
        self.pdf_button.clicked.connect(self.generate_pdf)
        button_layout.addWidget(self.pdf_button)

        self.layout.addLayout(button_layout)

    def save_invoice(self, data):
     try:
        query = '''INSERT INTO invoices 
                   (acc_no, state_name, date, name, code, time, gstin, bill_no, items, total_before_tax, sgst, cgst, igst, total_after_tax) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        
        self.c.execute(query, data)
        self.conn.commit()
        self.current_record = self.c.lastrowid
        print("Invoice saved!")
     except mysql.connector.Error as err:
        print(f"Error: {err}")

    def load_invoice(self, invoice_id):
        self.c.execute("SELECT * FROM invoices WHERE id=%s", (invoice_id,))
        record = self.c.fetchone()

        if record:
            self.acc_no_input.setText(record[1])
            self.state_name_input.setText(record[2])
            self.date_input.setText(record[3])
            self.name_input.setText(record[4])
            self.code_input.setText(record[5])
            self.time_input.setText(record[6])
            self.gstin_input.setText(record[7])
            self.bill_no_input.setText(record[8])
            items = eval(record[9])

            for row in range(len(items)):
                self.table.setItem(row, 0, QTableWidgetItem(items[row]["description"]))
                self.table.setItem(row, 1, QTableWidgetItem(items[row]["hsn_code"]))
                self.table.cellWidget(row, 2).setText(items[row]["quantity"])
                self.table.cellWidget(row, 3).setText(items[row]["rate"])
                self.table.setItem(row, 4, QTableWidgetItem(items[row]["total"]))
                self.table.cellWidget(row, 5).setText(items[row]["discount"])
                self.table.setItem(row, 6, QTableWidgetItem(items[row]["discounted_price"]))

            self.total_before_tax_input.setText(str(record[10]))
            self.sgst_input.setText(str(record[11]))
            self.cgst_input.setText(str(record[12]))
            self.igst_input.setText(str(record[13]))
            self.total_after_tax_input.setText(str(record[14]))

    def load_next(self):
        if self.current_record is None:
            self.c.execute("SELECT id FROM invoices ORDER BY id ASC LIMIT 1")
        else:
            self.c.execute("SELECT id FROM invoices WHERE id > %s ORDER BY id ASC LIMIT 1", (self.current_record,))
        
        result = self.c.fetchone()
        if result:
            self.current_record = result[0]
            self.load_invoice(self.current_record)

    def load_previous(self):
        if self.current_record is None:
            self.c.execute("SELECT id FROM invoices ORDER BY id DESC LIMIT 1")
        else:
            self.c.execute("SELECT id FROM invoices WHERE id < %s ORDER BY id DESC LIMIT 1", (self.current_record,))

        result = self.c.fetchone()
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = SalesInvoiceApp()
    mainWindow.show()
    sys.exit(app.exec_())