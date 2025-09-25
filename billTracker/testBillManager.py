import unittest
from datetime import date, timedelta
from bill import Bill
from billManager import BillManager

class TestBillManager(unittest.TestCase):

    def setUp(self):
        self.manager = BillManager()
        self.today = date.today()
        self.past_date = self.today - timedelta(days=10)
        self.future_date = self.today + timedelta(days=10)

        self.bill1 = Bill(name="Electricity", amount=100.0, due_date=self.future_date, frequency="monthly")
        self.bill2 = Bill(name="Internet", amount=50.0, due_date=self.past_date, frequency="monthly")

    def test_add_bill(self):
        self.manager.add_bill(self.bill1)
        self.assertEqual(len(self.manager.bills), 1)
        self.assertEqual(self.manager.bills[0].name, "Electricity")

    def test_add_duplicate_bill(self):
        self.manager.add_bill(self.bill1)
        duplicate = Bill(name="Electricity", amount=100.0, due_date=self.future_date, frequency="monthly")
        self.manager.add_bill(duplicate)
        self.assertEqual(len(self.manager.bills), 1, "Duplicate bill should not be added")

    def test_remove_bill(self):
        self.manager.add_bill(self.bill1)
        self.manager.remove_bill("Electricity", self.future_date)
        self.assertEqual(len(self.manager.bills), 0)

    def test_get_upcoming_bill(self):
        self.manager.add_bill(self.bill1)
        self.manager.add_bill(self.bill2)
        upcoming = self.manager.get_upcoming_bill()
        self.assertIn(self.bill1, upcoming)
        self.assertNotIn(self.bill2, upcoming)

    def test_get_overdue_bills(self):
        self.manager.add_bill(self.bill1)
        self.manager.add_bill(self.bill2)
        overdue = self.manager.get_overdue_bills()
        self.assertIn(self.bill2, overdue)
        self.assertNotIn(self.bill1, overdue)

    def test_mark_bill_as_paid(self):
        self.manager.add_bill(self.bill1)
        self.manager.mark_bill_as_paid("Electricity", self.future_date)
        self.assertTrue(self.bill1.paid)
        self.assertEqual(self.bill1.payment_date, self.today)

    def test_remove_all_bills(self):
        self.manager.add_bill(self.bill1)
        self.manager.add_bill(self.bill2)
        self.manager.remove_all_bills()
        self.assertEqual(len(self.manager.bills), 0)

    def test_list_all_bills(self):
        self.manager.add_bill(self.bill1)
        self.manager.add_bill(self.bill2)
        all_bills = self.manager.list_all_bills()
        self.assertEqual(len(all_bills), 2)
        self.assertIn(self.bill1, all_bills)
        self.assertIn(self.bill2, all_bills)

if __name__ == "__main__":
    unittest.main()
