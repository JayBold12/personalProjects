from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys as K
from time import sleep
import xlsxwriter
import random

#GLOBAL
cityState = input("What place to search in? (city, state): ")
filename = input("Name of Output file: ")
priceCeiling = input("Max price to search for: ")
driver = wd.Chrome("C:\Program Files (x86)\chromedriver.exe")
workbook = xlsxwriter.Workbook(filename + '.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(0,0,"Price")
worksheet.write(0,1, "SQ. FT")
worksheet.write(0,2, "Address")


def webSurf(location, maxPrice):

    #go to the website with location and max price threshold 
    url = "https://www.zillow.com/homes/" + location
    driver.get(url)
    driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/section/div[1]/div/div[2]/button").click()
    sleep(1)
    priceCap = driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/section/div[1]/div/div[2]/div/div/form/fieldset/div/label[2]/div/input")
    priceCap.click()
    priceCap.send_keys(maxPrice)
    driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/section/div[1]/div/div[2]/div/div/div/button").click()
    sleep(1)
       
def gatherAndWrite():
    #gather housing info and write to excel file
    sleep(1)
    findings = driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div[1]/div/span[1]")
    totalHouses = convertToNumber(findings.text)
    row = 1
    while(totalHouses != 0):
        housePrices = driver.find_elements_by_class_name("list-card-price")
        houseArea = driver.find_elements_by_class_name("list-card-details")
        houseAddress = driver.find_elements_by_class_name("list-card-addr")
        for i in range(len(housePrices)):
            worksheet.write_string(row, 0, housePrices[i].text)
            worksheet.write_string(row, 1, houseArea[i].text)
            worksheet.write_string(row, 2, houseAddress[i].text)
            row += 1
        totalHouses -= len(housePrices)
        housePrices.clear
        houseArea.clear()
        houseAddress.clear()
        if(totalHouses > 0):
            goToNextPage()
            sleep(random.randint(1,10))
        else: break
    workbook.close()
    driver.quit()

def goToNextPage():
    nextButton = driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/div[1]/div/div[1]/div[2]/nav/ul/li[3]/a")
    wd.ActionChains(driver).move_to_element(nextButton).perform()
    nextButton.click()

def convertToNumber(numberText):
    makeNumber = str(numberText)
    number = ""
    for letter in makeNumber:
        if(letter.isdigit()):
            number += letter
        else:
            pass
    return int(number)

def main():
    webSurf(cityState, priceCeiling)
    gatherAndWrite()

if __name__ == "__main__":
    main()