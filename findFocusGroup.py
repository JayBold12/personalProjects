from bs4 import BeautifulSoup
import requests
import sqlite3
from datetime import datetime
from datetime import timedelta
#import csv #use this for a csv/excel file output instead of a txt file
from timeit import default_timer as timer
import os
'''This function goes through the all the findfocusgroups.com and pulls the urls on all 5 webpages, 
adds the founnd urls to a list and returns that list'''
def scrape() -> list:
    #list of urls to scrape the surveys from
    webpages = ["https://findfocusgroups.com/",
            "https://findfocusgroups.com/more-focus-groups-2/",
            "https://findfocusgroups.com/more-focus-groups-3/",
            "https://findfocusgroups.com/more-focus-groups-4/",
            "https://findfocusgroups.com/more-focus-groups-5/"]
    #use a set to  not have dupiculate urls
    links = set()
    #iterate through the list of webpages
    for page in webpages:
        #use BeautifulSoap library to web scrape the data
        result = requests.get(page)
        doc = BeautifulSoup(result.text, "html.parser")
        #all the urls needed contain an a html tag
        urls = doc.find_all("a")
        #iterate through the found urls on the current webpage
        for url in urls:
            href = url.get('href')
            #add survey links to set (survey link are distingusted in the webpage ending with html for their urls)
            if href not in links and str(href).endswith('html'):
                links.add(href)
    #type cast the finalized set to a regular list and returns it
    links = list(links)
    return links
'''This fucntion passes in a list of urls. From this list the program will then filter from the list
urls depending on where they take place. The original list should only have survey links that are taking place online/nationwide'''
def filterByLocation(surveys: list) -> None:
    #copy the set that was passed in because we are iterating and manipulating its contents
    copies = set(surveys)
    #iterate over the copied set
    for copy in copies:
        #use beautiful soap to find data that is needed on the urls that are being iterated through
        result = requests.get(copy)
        doc = BeautifulSoup(result.text, "html.parser")
        #locate on the webpages the location of where the surveys are taking place
        location = doc.find("p", class_="font-size-lg text-gray-700 mb-5 mb-md-0")
        #filter from the original list surveys that are not taking place nationwide
        if "Nationwide" not in location.text:
            surveys.remove(copy)
'''This function passes in a list of urls and a string. For each url in the list the program finds data depending on the
correspodning string indictor. This data is added to a list and returned'''
def moreInfo(surveys: list, indicator: str) -> list[str]:
    #initalize the list that is going to be returned
    info = []
    #loop through the list of surverys
    for survey in surveys:
        result = requests.get(survey)
        doc = BeautifulSoup(result.text, "html.parser")
        #pull the title of the survey based on the indicator passed into the function
        if indicator == 'T':
            title = doc.find('h1', class_="display-4 mb-2")
            info.append(title.text[1:])
        #pull the date of the survey based on the indicator passed into the function
        else:
           date = doc.find('p', class_="font-size-lg text-gray-700 mb-5 mb-md-0")
           info.append(date.text[-11:-1])
    #return the created list
    return info
'''This function arrange the infomation in the format to later place into the database'''
def formatInfo(titles, dates, links) -> list[set]:
    #initalize the list that is going to be returned
    sqlData = []
    #loop through all the lists
    for i in range(len(links)):
        #place the info into the list with the preferred format
        sqlData.append((titles[i], dates[i], links[i]))
    #return the created list
    return sqlData
'''This function initilizes a SQL database if it is not created and then places the previeously gathered data
into the database in the specified format'''
def enterDatabase(data: list) -> None:
    #initilze the database connection
    conn = sqlite3.connect('findFocusGroup.db')
    cursor = conn.cursor()
    #initilze the database table if it is not created before
    cursor.execute("""CREATE TABLE IF NOT EXISTS focusgroups (title text, date text, link text PRIMARY KEY)""")
    #insert the data into the database
    cursor.executemany("INSERT OR IGNORE INTO focusgroups VALUES (?,?,?)", data)
    #save the changes to the database
    conn.commit()
'''This function in goes into the SQL database and eliminates survey entries if the date of those entries
are from a month ago (30 days) in real time'''
def cleanUpDatabase(db):
    #find the threshold date from today's date
    today = datetime.today()
    monthAgo = today - timedelta(days=30)
    #format the date for the SQL to understand
    dateThreshold = str(monthAgo)[5:7] + '/' + str(monthAgo)[8:10] + '/' + str(monthAgo)[:4]
    #make a query statment for SQL database
    query = "DELETE FROM focusgroups WHERE date = " + dateThreshold
    #initilze the database connection
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    #delete month old enteries from the database
    cursor.execute(query)
    #save the changes to the database
    conn.commit()
'''This function goes into the SQL database and writes the entries from the database
and exports the data to a simple text file to email out for other people to read'''
def exportData(db):
    #initilze the database connection
    conn = sqlite3.connect('findFocusGroup.db')
    cursor = conn.cursor()
    #initilze text file to write to
    with open('focusgroup.txt', 'w') as write_file:
        #write to the text file for exporting
        for row in cursor.execute("SELECT * FROM focusgroups"):
          writeRow = " ".join(row) + "\n"
          write_file.write(writeRow)
        write_file.close()
    #move the  created file to the deaktop directory of the computer
    os.rename("C:/current/location/of/the/file", "C:/desired/location/of/the/file")
def main():
    #run the program and time the process of each function and the entire program
    inital = timer()
    start = timer()
    links = scrape()
    end = timer()
    print("Scrape time: " + str(end - start))
    start = timer()
    filterByLocation(links)
    end = timer()
    print("Filter time: " + str(end - start))
    start = timer()
    titles = moreInfo(links, 'T')
    dates = moreInfo(links, 'D')
    end = timer()
    print("Info time: " + str(end - start))
    start = timer()
    entries = formatInfo(titles, dates, links)
    end = timer()
    print("Format time: " + str(end - start))
    start = timer()
    enterDatabase(entries)
    end = timer()
    print("Enter time: " + str(end - start))
    start = timer()
    cleanUpDatabase('findFocusGroup.db')
    end = timer()
    print("Clean time: " + str(end - start))
    start = timer()
    exportData('findFocusGroup.db')
    end = timer()
    print("Export time: " + str(end - start))
    bigFinish = timer()
    print("Total time to finish: " + str(bigFinish - inital))
if __name__ == '__main__':
    main()