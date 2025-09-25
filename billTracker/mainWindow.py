from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox
)
from billManager import BillManager
from addBillDialog import AddBillDialog
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bill Tracker")
        self.setMinimumSize(600, 400)

        self.manager = BillManager()
        self.manager.load_from_file("bills.json")
        self.check_for_upcoming_bills()

        self.setup_ui()
        self.load_table()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Amount", "Due Date", "Paid", "Frequency"])

        add_button = QPushButton("Add Bill")
        add_button.clicked.connect(self.add_bill)
        layout.addWidget(add_button)

        self.mark_paid_button = QPushButton("Mark as Paid")
        self.mark_paid_button.clicked.connect(self.mark_selected_bill_as_paid)
        layout.addWidget(self.mark_paid_button)

    def load_table(self):
        bills = self.manager.list_all_bills()
        self.table.setRowCount(len(bills))
        for row, bill in enumerate(bills):
            self.table.setItem(row, 0, QTableWidgetItem(bill.name))
            self.table.setItem(row, 1, QTableWidgetItem(f"{bill.amount:.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(str(bill.due_date)))
            self.table.setItem(row, 3, QTableWidgetItem("Yes" if bill.paid else "No"))
            self.table.setItem(row, 4, QTableWidgetItem(bill.frequency))


    def check_for_upcoming_bills(self):
        upcoming_bills = self.manager.get_due_soon_bills(days_ahead=3)

        if not upcoming_bills:
            return

        message = "The following bills are due soon:\n\n"
        for bill in upcoming_bills:
            message += f"• {bill.name} — Due {bill.due_date.strftime('%Y-%m-%d')}\n"

        QMessageBox.information(self, "Upcoming Bills", message)

    def add_bill(self):
        dialog = AddBillDialog(self)
        if dialog.exec():
            bill = dialog.get_bill()
            self.manager.add_bill(bill)
            self.manager.save_to_file("bills.json")
            self.load_table()

    def mark_selected_bill_as_paid(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a bill to mark as paid.")
            return

        name_item = self.table.item(selected_row, 0)
        due_date_item = self.table.item(selected_row, 2)
        paid_item = self.table.item(selected_row, 3)

        if paid_item.text() == "Yes":
            QMessageBox.information(self, "Already Paid", "This bill is already marked as paid.")
            return

        try:
            bill_name = name_item.text()
            due_date = datetime.strptime(due_date_item.text(), "%Y-%m-%d").date()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not parse bill data: {e}")
            return

        self.manager.mark_bill_as_paid(bill_name, due_date)
        self.manager.save_to_file("bills.json")
        self.load_table()
        

