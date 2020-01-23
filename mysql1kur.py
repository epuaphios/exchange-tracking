import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import re
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from time import sleep
from inscriptis import get_text
from urllib.request import Request, urlopen
import string
import time
import random

def random_char(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))

try:
    connection = mysql.connector.connect(host='X',
                                         database='X',
                                         user='X',
                                         password='X')
    while True:
    # code goes here
     
        sql_select_Query = "select * from kodekur"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        i = random_char(10)
        ql_select_Query1 = "select gup_id from ogun.kurovski order by gup_id desc LIMIT 1"
        cursor = connection.cursor(buffered=True)
        cursor.execute(ql_select_Query1)
        record = cursor.fetchone()
        i = record[0] + 1
        print (record)

        for row in records:
            print("id = ", row[0])
            print("kimden = ", row[1])
            print("kime  = ", row[2])
        
            print(i)
            url = 'https://www.cepteteb.com.tr/services/DovizCevir?tutar=1.00&fromCurrency={}&toCurrency={}&islemTip={}'.format(row[1],row[2],row[3])  
            print (url)
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            web_byte = urlopen(req).read()
            webpage = web_byte.decode('utf-8')
            text = get_text(webpage)
            text2 = text.replace('}',' ')
            text3 = text2[47:]
            print(text3)

            mySql_insert_query = """INSERT INTO kurovski (kur, timem, kodekur_id,gup_id) 
                               VALUES 
                               ({},CURRENT_TIMESTAMP,{},'{}') """.format (text3,row[0],i)
            print("Record inserted successfully into Laptop table")
            connection.commit()
            cursor = connection.cursor()
            result = cursor.execute(mySql_insert_query)
            cursor.close()
        connection.commit()
        cursor.close()
        time.sleep(15)   
except mysql.connector.Error as error:
    print("Failed to insert record into Laptop table {}".format(error))

finally:
    if (connection.is_connected()):
        connection.close()
        print("MySQL connection is closed")