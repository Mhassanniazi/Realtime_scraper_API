from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from scraper import Scraper

# creating data model which act as a request body
class Quotes(BaseModel):
    quote: str
    author: str
    tags: Optional[str]

app = FastAPI()

# database connection 
spider_call = Scraper()

@app.get("/{city}")
def Show_software_houses(city):
    return spider_call.scraped(city)
    
@app.get("/record/{city}")
def Show_results(city):
    resultData = spider_call.cursor.execute("""SELECT SOFTWARE_HOUSES.ID, CITIES.NAME, SOFTWARE_HOUSES.NAME, SOFTWARE_HOUSES.LINK FROM CITIES 
    INNER JOIN SOFTWARE_HOUSES ON CITIES.ID = SOFTWARE_HOUSES.CITY_ID
    WHERE CITIES.NAME = ?""",(city,)).fetchall()
    for i,j in enumerate(resultData):
        jsonData = {}
        jsonData['id'] = j[0]
        jsonData['city'] = j[1]
        jsonData['software_house'] = j[2]
        jsonData['url'] = j[3]

        resultData[i] = jsonData
    return resultData
    
# @app.post("/add")
# def add_quotes(item: Quotes):
#     print("Checking return data:",item," and type ",type(item))
#     a=item.dict()
#     print("HELLO:",a,"and type is: ",type(a))
#     # must use "," after var inside tuple for single value
#     dbCon.cursor.execute("""INSERT INTO QUOTES VALUES(null,?)""",(item.quote,))
#     allData = dbCon.cursor.execute("""SELECT * FROM RESULTS""").fetchall()
#     dbCon.cursor.execute("""INSERT INTO RESULTS VALUES(null,?,?,?)""",(int(allData[-1][1])+1,item.author,item.tags))
#     dbCon.conn.commit()

#     return {"Succes":"Succesfully Inserted"}

