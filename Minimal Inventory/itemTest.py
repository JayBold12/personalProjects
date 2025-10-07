from item import Item
import datetime

def test_mark_used():
    item = Item("Marker", "School", "Desk", None, None, None)
    assert item.last_used != datetime.date.today()
    item.mark_used()
    assert item.last_used == datetime.date.today()
    print("mark_used() tests results: PASSED")

def test_days_since_last_used():
    item = Item("Marker", "School", "Desk", None, None, None)
    last_used = item.days_since_last_used()
    assert last_used == -1, "0"

    assert last_used == -1, "NOT USED"
    print("days_since_last_used() tests results: PASSED")

def test_from_dict():
    pass
def test_to_dict():
    pass
def test_update():
    pass

def main():
    test_mark_used()
    test_days_since_last_used()

if __name__ == "__main__":
    main()
