"""use selenium to go to the subreddit page r/findfocusgroups
extract links to the focus groups up to a month back
add links to a database
email links if the database is updated
run on a timer daily
gui???"""
from selenium import webdriver
import time
class Crawler:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
    def goToSite(self):
        self.driver.get("https://www.reddit.com/user/findfocusgroups/")
        time.sleep(1)
    def jumpDown(self):
        driver = self.driver
        timeframe = driver.find_element_by_class_name("_3jOxDPIQ0KaOWpzvSQo-1s")
        while timeframe.text != "10 days ago":
            print(timeframe.text)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            timeframe = timeframe

def main():
    crawly = Crawler()
    crawly.goToSite()
    crawly.jumpDown()
if __name__ == "__main__":
    main()