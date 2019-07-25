import PySimpleGUI as sg
import pandas as pd

import mysql.connector

cnx = mysql.connector.connect(user='root', password='gmw6504192658',
                              host='127.0.0.1',
                              database='ctcal_db')

cursor = cnx.cursor()


sql_Cust_Code_Name = ("SELECT Customer_Code, Customer_CompanyName FROM customer_info")

sql_Cust_DUT = ("SELECT Customer_DUT_SN, Customer_Code, Customer_CompanyName FROM customer_dut "
                "JOIN customer_info ON Customer_Info_idCustomer_Info = idCustomer_Info;")

cursor.execute(sql_Cust_Code_Name)


# Customer_Code_List = []
# Customer_CompanyName_List = []

# for (Customer_Code, Customer_CompanyName) in cursor:
#     Customer_Code_List.append(Customer_Code)
#     Customer_CompanyName_List.append(Customer_CompanyName)

# https://pbpython.com/pandas-list-dict.html
df_customer = pd.DataFrame.from_records(list(cursor.fetchall()), columns=['Customer_Code', 'Customer_CompanyName'])


cursor.execute(sql_Cust_DUT)
df_dut_customer = pd.DataFrame.from_records(list(cursor.fetchall()),
                                            columns=['DUT_SN', 'Customer_Code', 'Customer_CompanyName'])

cursor.close()
cnx.close()


layout1 = [[sg.Text('Check Customer Name with Code', font='Helvetica 15')],
           [sg.Text('Customer Code: '), sg.InputText(default_text='YOKGA1', size=(12, 1), key='Customer_Code')],
           [sg.Text('Customer Name: '), sg.Text('', size=(80, 1), key='Customer_Name')],
           [sg.Text('')],
           [sg.ReadButton('Search')],
           [sg.Text('Check DUT', font='Helvetica 15')],
           [sg.Text('DUT SN: '), sg.InputText(default_text='9113250015', size=(12, 1), key='DUT_SN')],
           [sg.Text('Customer Name: '), sg.Text('', size=(80, 1), key='Customer_Name_DUT')],
           [sg.Text('')],
           [sg.ReadButton('Search_DUT')],
           [sg.Button('Show all DUT'), sg.Button('Exit')]]   # Button close the window

window1 = sg.Window(title='check customer name', size=(800, 600), grab_anywhere=False).Layout(layout1)

win2_active = False

while True:
    button, values = window1.Read()

    if button is None or button == 'Exit':
        break  # close the window and quit the while

    code = values['Customer_Code']

    if code in list(df_customer['Customer_Code'].tolist()):
        Cust_Name = df_customer.loc[df_customer['Customer_Code'] == code].get('Customer_CompanyName').item()
    else:
        Cust_Name = 'Customer Code Not in the database'

    window1.FindElement('Customer_Name').Update(Cust_Name)  # output with key and Update

    SN = values['DUT_SN']
    if SN in list(df_dut_customer['DUT_SN'].tolist()):
        Cust_Name_DUT = df_dut_customer.loc[df_dut_customer['DUT_SN'] == SN].get('Customer_CompanyName').item()
    else:
        Cust_Name_DUT = 'DUT SN Not in the database'

    window1.FindElement('Customer_Name_DUT').Update(Cust_Name_DUT)  # output with key and Update

    if not win2_active and button == 'Show all Customer':
        win2_active = True
        layout2 = [[sg.Text('Show all Customer Name')],
                   [sg.Table(values=df_customer.values.tolist(), headings=['Code', 'Name'], display_row_numbers=True,
                             col_widths=40, auto_size_columns=True)],
                   [sg.Button('Exit')]]

        # Table must have predefine headings

        win2 = sg.Window('Show all Customer').Layout(layout2)

    if win2_active:
        print(win2_active)
        ev2, vals2 = win2.Read()  # parameter timeout=100
        if ev2 is None or ev2 == 'Exit':
            print(vals2)
            win2_active  = False
            win2.Close()


