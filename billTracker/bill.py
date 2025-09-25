from datetime import date

class Bill:
    def __init__(self, name:str, amount:float, due_date:date, frequency:str):
        self.name = name
        self.amount = amount
        self.due_date = due_date
        self.paid = False
        self.frequency = frequency
        self.payment_date = None
        self.note = ""
    
    def to_dict(self):
        return {"name" : self.name,
                "amount" : self.amount,
                "due date" : self.due_date.isoformat(),
                "paid" : self.paid,
                "frequency" : self.frequency,
                "payment date" : self.payment_date.isoformat() if self.payment_date != None else None,
                "note" : self.note}
    
    @classmethod
    def from_dict(cls, data):
        bill = cls(
            name=data["name"],
            amount=data["amount"],
            due_date=date.fromisoformat(data["due date"]),
            frequency=data["frequency"]
        )
        bill.paid = data["paid"]
        bill.payment_date = date.fromisoformat(data["payment date"]) if data["payment date"] else None
        bill.note = data.get("note", "")
        return bill
    
