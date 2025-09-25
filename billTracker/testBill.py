import unittest
from datetime import date
from bill import Bill


class TestBill(unittest.TestCase):

    def setUp(self):
        self.bill = Bill(
            name="Water",
            amount=30.5,
            due_date=date(2025, 10, 10),
            frequency="monthly"
        )

    def test_initialization_defaults(self):
        self.assertEqual(self.bill.name, "Water")
        self.assertEqual(self.bill.amount, 30.5)
        self.assertEqual(self.bill.due_date, date(2025, 10, 10))
        self.assertEqual(self.bill.frequency, "monthly")
        self.assertFalse(self.bill.paid)
        self.assertIsNone(self.bill.payment_date)
        self.assertEqual(self.bill.note, "")

    def test_to_dict(self):
        self.bill.paid = True
        self.bill.payment_date = date(2025, 10, 12)
        self.bill.note = "Paid early"

        bill_dict = self.bill.to_dict()

        expected = {
            "name": "Water",
            "amount": 30.5,
            "due date": "2025-10-10",
            "paid": True,
            "frequency": "monthly",
            "payment date": "2025-10-12",
            "note": "Paid early"
        }

        self.assertEqual(bill_dict, expected)

    def test_from_dict(self):
        data = {
            "name": "Water",
            "amount": 30.5,
            "due date": "2025-10-10",
            "paid": True,
            "frequency": "monthly",
            "payment date": "2025-10-12",
            "note": "Paid early"
        }

        new_bill = Bill.from_dict(data)

        self.assertEqual(new_bill.name, "Water")
        self.assertEqual(new_bill.amount, 30.5)
        self.assertEqual(new_bill.due_date, date(2025, 10, 10))
        self.assertTrue(new_bill.paid)
        self.assertEqual(new_bill.payment_date, date(2025, 10, 12))
        self.assertEqual(new_bill.note, "Paid early")

    def test_round_trip_serialization(self):
        self.bill.paid = True
        self.bill.payment_date = date(2025, 10, 12)
        self.bill.note = "Paid early"

        serialized = self.bill.to_dict()
        deserialized = Bill.from_dict(serialized)

        self.assertEqual(deserialized.name, self.bill.name)
        self.assertEqual(deserialized.amount, self.bill.amount)
        self.assertEqual(deserialized.due_date, self.bill.due_date)
        self.assertEqual(deserialized.paid, self.bill.paid)
        self.assertEqual(deserialized.payment_date, self.bill.payment_date)
        self.assertEqual(deserialized.note, self.bill.note)


if __name__ == "__main__":
    unittest.main()
