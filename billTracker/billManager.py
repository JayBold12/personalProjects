import json
import os
from bill import Bill
from datetime import date
from datetime import timedelta


class BillManager:
    def __init__(self):
        self.bills = []

    def add_bill(self, new_bill):
        for bill in self.bills:
            if bill.name == new_bill.name and bill.due_date == new_bill.due_date:
                return
        self.bills.append(new_bill)


    def remove_bill(self, bill_name:str, due_date: date):
        tmp = []
        for b in self.bills:
            if not (b.name == bill_name and b.due_date == due_date):
                tmp.append(b)
        self.bills = tmp
    
    def remove_all_bills(self):
        self.bills = []

    def get_upcoming_bill(self):
        today = date.today()
        tmp = []
        for b in self.bills:
            if not b.paid and b.due_date >= today:
                tmp.append(b)
        return tmp
    
    def list_all_bills(self):
        return self.bills
    
    def save_to_file(self, file_path):
        with open(file_path, "w") as f:
            data = [bill.to_dict() for bill in self.bills]
            json.dump(data, f, indent=4)
    
    def load_from_file(self, file_path):
        if not os.path.exists(file_path):
            return  # Nothing to load

        with open(file_path, "r") as f:
            data = json.load(f)
            self.bills = [Bill.from_dict(b) for b in data]

    def get_overdue_bills(self):
        today = date.today()
        tmp = []
        for b in self.bills:
            if b.due_date < today and not b.paid:
                tmp.append(b)
        return tmp
    
    def mark_bill_as_paid(self, bill_name:str, due_date: date):
        for b in self.bills:
            if b.name == bill_name and b.due_date == due_date:
                b.paid =  True
                b.payment_date = date.today()
                return
    
    def get_due_soon_bills(self, days_ahead=3):
        today = date.today()
        upcoming = []
        for b in self.bills:
            if not b.paid and today <= b.due_date <= today + timedelta(days=days_ahead):
                upcoming.append(b)
        return upcoming