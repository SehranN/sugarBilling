import os
import xlsxwriter
import utils

# Define the file name
file_name = "oilBiller.xlsx"

# Check if the file exists and remove it if it does
if os.path.exists(file_name):
    os.remove(file_name)

# Initialize the workbook
workbook = xlsxwriter.Workbook(file_name)

# Add worksheets
CustBal = workbook.add_worksheet("CustBal")
Customer = workbook.add_worksheet("Customer")
ExpenseBalance = workbook.add_worksheet("ExpenseBalance")
Items = workbook.add_worksheet("Items")
ExpItems = workbook.add_worksheet("Expense Items")
Purchase_bills=workbook.add_worksheet("Purchase_bills")
Purchase_items=workbook.add_worksheet("Purchase_items")
PurchaseRet_bills=workbook.add_worksheet("PurchaseRet_bills")
PurchaseRet_items=workbook.add_worksheet("PurchaseRet_items")
Sales_bills=workbook.add_worksheet("Sales_bills")
Sales_item=workbook.add_worksheet("Sales_items")
SalesRet_bills=workbook.add_worksheet("SalesRet_bills")
SalesRet_item=workbook.add_worksheet("SalesRet_items")
# Connect to the database
mydb = utils.connection
mycursor = mydb.cursor()

# Helper function to write data to a worksheet
def write_data_to_worksheet(worksheet, headers, query):
    worksheet.write_row(0, 0, headers)
    mycursor.execute(query)
    data = mycursor.fetchall()
    for row_index, row_data in enumerate(data, start=1):
        worksheet.write_row(row_index, 0, row_data)

# Writing data to worksheets
write_data_to_worksheet(CustBal, [ "date", "accNo", "cashDebit", "cashCredit", "billType", "billNo", "sNo"], "SELECT * FROM cust_bal")
write_data_to_worksheet(Customer, [ "accNo", "name", "phno", "email", "Company", "address", "Oldcash"], "SELECT * FROM customer")
write_data_to_worksheet(ExpenseBalance, [ "ID", "Date", "Item_Name", "Amount", "Notes"], "SELECT * FROM expensebalance")
write_data_to_worksheet(Items, ["Item_No", "Item_Name", "Rate", "type"], "SELECT * FROM items")
write_data_to_worksheet(ExpItems, ["Item_No", "Item_Name"], "SELECT * FROM exp_items")
write_data_to_worksheet(Purchase_bills, [ "date", "accNo", "name", "totalQuantity", "totalAount", "totalTransport", "grandTotal", "billNo", "sNo"], "SELECT * FROM purchase_bills")
write_data_to_worksheet(Purchase_items, [ "date", "accNo", "name", "itemName", "notes", "rate", "quantity", "total", "transport", "gTotal", "billNo", "sNo"], "SELECT * FROM purchase_items")
write_data_to_worksheet(PurchaseRet_bills, [ "date", "accNo", "name", "totalQuantity", "totalAount", "totalTransport", "grandTotal", "billNo", "sNo"], "SELECT * FROM purchaseRet_bills")
write_data_to_worksheet(PurchaseRet_items, [ "date", "accNo", "name", "itemName", "notes", "rate", "quantity", "total", "transport", "gTotal", "billNo", "sNo"], "SELECT * FROM purchaseRet_items")
write_data_to_worksheet(Sales_bills, [ "date", "accNo", "name", "totalQuantity", "totalAount", "totalTransport", "grandTotal", "billNo", "sNo"], "SELECT * FROM sales_bills")
write_data_to_worksheet(Sales_item,  [ "date", "accNo", "name", "itemName", "notes", "rate", "quantity", "total", "transport", "gTotal", "billNo", "sNo"],"SELECT * FROM sales_items")
write_data_to_worksheet(SalesRet_bills, [ "date", "accNo", "name", "totalQuantity", "totalAount", "totalTransport", "grandTotal", "billNo", "sNo"], "SELECT * FROM salesRet_bills")
write_data_to_worksheet(SalesRet_item,  [ "date", "accNo", "name", "itemName", "notes", "rate", "quantity", "total", "transport", "gTotal", "billNo", "sNo"],"SELECT * FROM salesRet_items")

workbook.close()
mydb.close()
