from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import sqlite3

class Scraper:
    db_con = sqlite3.connect("scraperData.db",check_same_thread=False)
    cursor = db_con.cursor()
    def __init__(self):
        self.create_connection()
    def create_connection(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS CITIES (ID INTEGER PRIMARY KEY, NAME TEXT UNIQUE)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS SOFTWARE_HOUSES (ID INTEGER PRIMARY KEY, CITY_ID INTEGER, NAME TEXT, LINK TEXT, FOREIGN KEY (CITY_ID) REFERENCES CITIES (ID))""")

    def scraped(self,name):
        # inserting city name to db
        try:
            self.cursor.execute("""INSERT INTO CITIES VALUES(null,?)""",(name,))
        except:
            pass
        a = self.cursor.execute("""SELECT ID FROM CITIES WHERE NAME=?""",(name,)).fetchall()
        print("QUERY RESULT CHECKING",a)
        ################################
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get("https://www.google.com/maps")
        time.sleep(3)
        input_box = driver.find_element_by_css_selector("input#searchboxinput")
        input_box.send_keys(f"software houses in {name}")
        input_box.send_keys(Keys.ENTER)
        time.sleep(10)
        # have to scroll to the end of the sidebar
        for i in range(3):
            driver.execute_script("var a = document.getElementsByClassName('section-scrollbox');a[1].scrollTo(0,a[1].scrollHeight)")
            time.sleep(2)
        # side_bar = driver.find_elements_by_css_selector("div.section-scrollbox")
        # print("SIDE BAR IS: ",side_bar)
        # side_bar[0].send_keys(Keys.CONTROL+Keys.END)
        time.sleep(3)
        # now have to get page01 dynamic loaded data
        allData = driver.find_elements_by_css_selector("a.a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd")
        output_data = []
        for i in allData:
            temp_data = {}
            # print("OVERALL IS: ",i.get_attribute('href'))
            temp_data['name']=i.get_attribute('aria-label')  
            temp_data['link']=i.get_attribute('href')

            output_data.append(temp_data)
            # INSERTING DATA
            self.cursor.execute("""INSERT INTO SOFTWARE_HOUSES VALUES(null,?,?,?)""",(a[0][0],temp_data['name'],temp_data['link']))
        
        self.db_con.commit()
        return output_data
        # print("At the end data is: ",output_data)
# o1= Scraper()
# o1.scraped('islamabad')


# var a = document.getElementsByClassName("section-scrollbox")
# a[1].scrollTo(0,a[1].scrollHeight)