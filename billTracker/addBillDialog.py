from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QDateEdit, QComboBox
)
from PyQt6.QtCore import QDate
from bill import Bill
from datetime import date

class AddBillDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Bill")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.name_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())

        self.freq_input = QComboBox()
        self.freq_input.addItems(["monthly", "weekly", "yearly", "one-time"])

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(self.amount_input)

        layout.addWidget(QLabel("Due Date:"))
        layout.addWidget(self.date_input)

        layout.addWidget(QLabel("Frequency:"))
        layout.addWidget(self.freq_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def get_bill(self):
        name = self.name_input.text()
        amount = float(self.amount_input.text())
        due = self.date_input.date().toPyDate()
        frequency = self.freq_input.currentText()

        return Bill(name, amount, due, frequency)
