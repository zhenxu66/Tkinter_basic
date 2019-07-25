import mysql.connector

cnx = mysql.connector.connect(user='root', password='gmw6504192658',
                              host='127.0.0.1',
                              database='ctcal_db')

cursor = cnx.cursor()

query = ("SELECT Customer_Code, Customer_CompanyName FROM customer_info")

cursor.execute(query)

print(dict(cursor.fetchall()).get('YOKGA1'))

for (Customer_Code, Customer_CompanyName) in cursor:
    print("{} is the Code for {} ".format(Customer_Code, Customer_CompanyName))

cursor.close()

cnx.close()

