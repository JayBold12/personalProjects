from datetime import datetime

class Item:
    def __init__(self, name:str, category:str, location:str, acquired_date: datetime = None,
                 last_used: datetime = None, notes:str = None):
        self.name = name
        self.category = category
        self.location = location
        self.acquired_date = acquired_date
        self.last_used = last_used
        self.notes = notes

    def mark_used(self):
        self.last_used = datetime.today()
    
    def days_since_last_used(self):
        if not self.last_used:
            return -1
        return (datetime.now() - self.last_used).days
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
        name = data["name"],
        category = data["category"],
        location = data["location"],
        acquired_date = datetime.strptime(data["acquired date"], '%Y-%m-%d') if data["acquired date"] else None,
        last_used = datetime.strptime(data["last used"], '%Y-%m-%d') if data["last used"] else None,
        notes = data.get("notes")
        )
    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "location": self.location,
            "acquired date": self.acquired_date.strftime('%Y-%m-%d') if self.acquired_date else None,
            "last used": self.last_used.strftime('%Y-%m-%d') if self.last_used else None,
            "notes": self.notes
        }
    
    def update(self, name=None, category=None, location=None, acquired_date=None, last_used=None, notes=None):
        if name is not None:
            self.name = name
        if category is not None:
            self.category = category
        if location is not None:
            self.location = location
        if acquired_date is not None:
            self.acquired_date = acquired_date
        if last_used is not None:
            self.last_used = last_used
        if notes is not None:
            self.notes = notes
