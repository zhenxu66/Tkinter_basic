import PySimpleGUI as sg
import pandas as pd

import mysql.connector

cnx = mysql.connector.connect(user='root', password='gmw6504192658',
                              host='127.0.0.1',
                              database='ctcal_db')

cursor = cnx.cursor()

test = "INSERT INTO customer_info " \
       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

result = (44,'GMW_Code','GMW Associates','955 Industrial','San Carlos','CA','94563','USA')

cursor.execute(test,result)

cnx.commit()

cursor.close()
cnx.close()
