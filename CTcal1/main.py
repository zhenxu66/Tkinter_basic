

import PySimpleGUI as sg
import pandas as pd
import numpy as np
import datetime
now = datetime.datetime.now()

# pip install mysql-connector-python
import mysql.connector


layout0 = [[sg.Text('What is the server you want to connect?')],
           [sg.Radio('127.0.0.1', 'IP', default=True, enable_events=True, key='local'),
            sg.Radio('192.168.10.138', 'IP', enable_events=True, key='testbench'),
            sg.Radio('216.70.84.56', 'IP', enable_events=True, key='server')],
           [sg.Button('OK')]]

window0 = sg.Window('Window').Layout(layout0)
button, values = window0.Read()
print(button)
print(values)


if values['local'] is True:
    cnx = mysql.connector.connect(user='root', password='gmw6504192658',
                                  host='127.0.0.1',
                                  database='ctcal_db')
    sg.Popup('Database local is connected')

if values['testbench'] is True:
    cnx = mysql.connector.connect(user='zhenxu', password='gmw6504192658',
                                  host='192.168.10.138',
                                  database='ctcal_db')
    sg.Popup('Database testbench is connected')
if values['server'] is True:
    cnx = mysql.connector.connect(user='zhenxu', password='gmw6504192658',
                                  host='216.70.84.56',
                                  database='ctcal_db')
    sg.Popup('Database server is connected')



cursor = cnx.cursor()

sql_allCert = ("SELECT DISTINCT Cert_number, Customer_DUT_Model, Customer_DUT_SN, Customer_CompanyName, " 
               "Cert_Test_EndTime, Callab_Order_SO_Number, Labpeople_Firstname, " 
               "Labpeople_Lastname, TestTypeDCAC, Testfreq, PowerAnalyzer_config_DUT_Port, " 
               "Cert_TestTurns, PowerAnalyzer_model, PowerAnalyzer_Manufacturer " 
               "FROM flatstoretable_danisense_bk_id"
               " ORDER BY Cert_number DESC; ")
cursor.execute(sql_allCert)

df_allCert = pd.DataFrame.from_records(list(cursor.fetchall()),
                                       columns=[
                                            'Cert_number', 'Customer_DUT_Model', 'Customer_DUT_SN',
                                            'Customer_CompanyName', 'Cert_Test_EndTime',
                                            'Callab_Order_SO_Number', 'Labpeople_Firstname', 'Labpeople_Lastname',
                                            'TestTypeDCAC', 'Testfreq', 'PowerAnalyzer_config_DUT_Port',
                                            'Cert_TestTurns', 'PowerAnalyzer_model', 'PowerAnalyzer_Manufacturer'
                                        ])


sql_Cust_Code_Name = ("SELECT idCustomer_Info, Customer_Code, Customer_CompanyName FROM customer_info"
                      " ORDER BY idCustomer_Info DESC")

sql_Cust_DUT = ("SELECT idCustomer_DUT, Customer_DUT_SN, Customer_DUT_Model, Customer_Code, Customer_CompanyName, "
                "Customer_Info_idCustomer_Info FROM customer_dut "
                "JOIN customer_info ON Customer_Info_idCustomer_Info = idCustomer_Info"
                " ORDER BY idCustomer_DUT DESC")

cursor.execute(sql_Cust_Code_Name)


# Customer_Code_List = []
# Customer_CompanyName_List = []

# for (Customer_Code, Customer_CompanyName) in cursor:
#     Customer_Code_List.append(Customer_Code)
#     Customer_CompanyName_List.append(Customer_CompanyName)

# https://pbpython.com/pandas-list-dict.html


df_customer = pd.DataFrame.from_records(list(cursor.fetchall()),
                                        columns=['idCustomer_Info', 'Customer_Code',
                                                 'Customer_CompanyName'])


cursor.execute(sql_Cust_DUT)




df_dut_customer = pd.DataFrame.from_records(list(cursor.fetchall()),
                                            columns=['idCustomer_DUT', 'DUT_SN', 'Customer_DUT_Model', 'Customer_Code',
                                                     'Customer_CompanyName', 'Customer_Info_idCustomer_Info'])
customer_num = len(df_customer.index)

customer_dut_num = len(df_dut_customer.index)


sql_ct_danisense = ("SELECT idCT_Danisense, CT_Danisense_Model FROM ct_danisense")
cursor.execute(sql_ct_danisense)
df_ct_danisense = pd.DataFrame.from_records(list(cursor.fetchall()), columns=['idCT_Danisense', 'CT_Danisense_Model'])

Danisense_Models = df_ct_danisense['CT_Danisense_Model'].tolist()
Customer_Code_list = df_customer['Customer_Code'].tolist()
DUT_customer_SN_list = df_dut_customer['DUT_SN'].tolist()
print(DUT_customer_SN_list)

layout1 = [[sg.Button('Show all Cert')],
           [sg.Text('Check Customer Name with Code', font='Helvetica 15')],
           [sg.Text('Customer Code: '), sg.InputText(default_text='YOKGA1', size=(12, 1), key='Customer_Code')],
           [sg.Text('Customer Name: '), sg.Text('', size=(80, 1), key='Customer_Name')],
           [sg.Text('')],
           [sg.ReadButton('Search'), sg.Button('Show all Customer')],
           [sg.Text('Check DUT', font='Helvetica 15')],
           [sg.Text('DUT SN: '), sg.InputText(default_text='9113250015', size=(12, 1), key='DUT_SN')],
           [sg.Text('Customer Name (Show multiple with id): '), sg.Text('', size=(80, 3), key='Customer_Name_DUT')],
           [sg.ReadButton('Search_DUT'), sg.Button('Show all DUT')],
           [sg.Text('')],
           [sg.Text('Add New Customer (Code/Name/Street', font='Helvetica 15')],
           [sg.Text('(/City/State/Zip/Country)', font='Helvetica 15')],
           [sg.InputText(default_text='GMW_Code', size=(12, 1), key='Cust_Code'),
            sg.InputText(default_text='GMW Associates', size=(20, 1), key='Cust_Name'),
            sg.InputText(default_text='955 Industrial', size=(25, 1), key='Cust_Street')],
           [sg.InputText(default_text='San Carlos', size=(15, 1), key='Cust_City'),
            sg.InputText(default_text='CA', size=(8, 1), key='Cust_State'),
            sg.InputText(default_text='94563', size=(8, 1), key='Cust_Zipcode'),
            sg.InputText(default_text='USA', size=(15, 1), key='Cust_Country')],
           [sg.ReadButton('Add_New_Customer')],
           [sg.Text('')],
           [sg.Text('Add New DUT (SN/Manufacturer/Model)', font='Helvetica 15')],
           [sg.Text('(/Controller/Control_SN/Control_Chan/ExpDate/Cust_Code)', font='Helvetica 15')],
           [sg.InputText(default_text='add_dut_sn', size=(12, 1), key='add_dut_sn'),
            sg.InputText(default_text='Danisense', size=(12, 1), key='add_dut_manufacturer'),
            sg.InputCombo(Danisense_Models, default_value='DS200IDSA', size=(20, 4), enable_events=True, key='_LIST_')],
           [sg.InputText(default_text='add_dut_controller', size=(18, 1), key='add_dut_controller'),
            sg.InputText(default_text='add_dut_controller_sn', size=(18, 1), key='add_dut_controller_sn'),
            sg.InputText(default_text='controller_chan', size=(12, 1), key='add_dut_controller_chan'),
            sg.InputText(default_text='2020-05-06', size=(10, 1), key='add_exp_date'),
            sg.InputCombo(Customer_Code_list, default_value='GMWI1', size=(20, 4), enable_events=True, key='_LIST2_')],
           [sg.ReadButton('Add_New_DUT')],
           [sg.Text('')],
           [sg.Text('Add New Test Order(RMA/Callab_Order_ReceiveDate/Customer_DUT_SN/id_DUT(Duplicated SN))/idTestType)',
                    font='Helvetica 12')],
           [sg.InputText(default_text='add_order_RMA', size=(14, 1), key='add_order_RMA'),
            sg.InputText(default_text='2020-12-16', size=(12, 1), key='add_order_ReceiveDate'),
            sg.InputCombo(DUT_customer_SN_list, default_value='19287210001', size=(20, 4), enable_events=True,
                          key='_LIST3_'),
            sg.InputText(default_text='165', size=(12, 1), key='DuplicatedDUTID')
            ],
           [sg.Checkbox('DC', key='DC'), sg.Checkbox('AC60Hz', key='AC60Hz'),
            sg.Checkbox('AC400Hz', key='AC400Hz'), sg.Checkbox('AC50Hz', key='AC50Hz')],
           [sg.ReadButton('Add_New_Order')],
           [sg.Button('Exit')]]   # Button close the window

window1 = sg.Window(title='check customer name', size=(1200, 1000), grab_anywhere=False).Layout(layout1)

win2_active = False

win3_active = False

while True:
    # repeat previous sql inside to update
    sql_Cust_Code_Name = ("SELECT idCustomer_Info, Customer_Code, Customer_CompanyName FROM customer_info"
                          " ORDER BY idCustomer_Info DESC")
    cursor.execute(sql_Cust_Code_Name)

    df_customer = pd.DataFrame.from_records(list(cursor.fetchall()),
                                            columns=['idCustomer_Info', 'Customer_Code',
                                                     'Customer_CompanyName'])


    # Main function

    button, values = window1.Read()
    print(button)

    if button is None or button == 'Exit':
        break  # close the window and quit the while

    code = values['Customer_Code']

    if code in list(df_customer['Customer_Code'].tolist()):
        Cust_Name = df_customer.loc[df_customer['Customer_Code'] == code].get('Customer_CompanyName').item()
    else:
        Cust_Name = 'Customer Code Not in the database'

    if button == 'Search':
        window1.FindElement('Customer_Name').Update(Cust_Name)  # output with key and Update

    SN = values['DUT_SN']
    if SN in list(DUT_customer_SN_list):
        if len(df_dut_customer.loc[df_dut_customer['DUT_SN'] == SN].get('Customer_CompanyName')) == 1:
            Cust_Name_DUT = df_dut_customer.loc[df_dut_customer['DUT_SN'] == SN].get('Customer_CompanyName').item()
        else:
            Multiple_Customer_Series = df_dut_customer.loc[df_dut_customer['DUT_SN'] == SN].get('Customer_CompanyName')
            Multiple_Customer_Model_Series = df_dut_customer.loc[df_dut_customer['DUT_SN'] == SN].\
                get('Customer_DUT_Model')
            Multiple_Customer_id_Series = df_dut_customer.loc[df_dut_customer['DUT_SN'] == SN]. \
                get('idCustomer_DUT')

            s0 = ' | '.join(Multiple_Customer_id_Series.apply(str).tolist())
            s1 = ' | '.join(Multiple_Customer_Series.tolist())
            s2 = ' | '.join(Multiple_Customer_Model_Series.tolist())
            Cust_Name_DUT = s0 + '\n' + s1 + '\n' + s2
    else:
        Cust_Name_DUT = 'DUT SN Not in the database'

    if button == 'Search_DUT':
        window1.FindElement('Customer_Name_DUT').Update(Cust_Name_DUT)  # output with key and Update

    if not win2_active and button == 'Show all Customer':
        win2_active = True
        layout2 = [[sg.Text('Show all Customer Name')],
                   [sg.Table(values=df_customer.drop(columns=['idCustomer_Info']).values.tolist(),
                             headings=['Code', 'Name'],
                             display_row_numbers=True,
                             col_widths=40, auto_size_columns=True)],
                   [sg.Button('Exit')]]

        # Table must have predefine headings

        win2 = sg.Window('Show all Customer').Layout(layout2)

    if not win2_active and button == 'Show all DUT':
        win2_active = True
        layout2 = [[sg.Text('Show all DUT')],
                   [sg.Table(values=df_dut_customer.drop(columns=['Customer_Info_idCustomer_Info', 'idCustomer_DUT'])
                             .values.tolist(),
                             headings=['DUT_SN', 'Customer_Code', 'Customer_CompanyName'],
                             display_row_numbers=True,
                             col_widths=40, auto_size_columns=True)],
                   [sg.Button('Exit')]]

        # Table must have predefine headings

        win2 = sg.Window('Show all DUT').Layout(layout2)

    if win2_active:
        print(win2_active)
        ev2, vals2 = win2.Read()  # parameter timeout=100
        if ev2 is None or ev2 == 'Exit':
            print(vals2)
            win2_active  = False
            win2.Close()

    if not win2_active and button == 'Show all Cert':
        win2_active = True
        layout2 = [[sg.Text('Show all Cert (Columns will be trimmed')],
                   [sg.Table(values=df_allCert.values.tolist(),
                             headings=[
                                 'Cert_number', 'Customer_DUT_Model', 'Customer_DUT_SN', 'Customer_CompanyName',
                                 'Cert_Test_EndTime', 'Callab_Order_SO_Number',
                                 'Labpeople_Firstname', 'Labpeople_Lastname', 'TestTypeDCAC', 'Testfreq',
                                 'PowerAnalyzer_config_DUT_Port', 'Cert_TestTurns', 'PowerAnalyzer_model',
                                 'PowerAnalyzer_Manufacturer'
                             ],
                             display_row_numbers=False,
                             col_widths=10, auto_size_columns=True)],
                   [sg.Button('Exit')]]

        # Table must have predefine headings

        win2 = sg.Window('Show all Cert').Layout(layout2)

    if win2_active:
        print(win2_active)
        ev2, vals2 = win2.Read()  # parameter timeout=100
        if ev2 is None or ev2 == 'Exit':
            print(vals2)
            win2_active  = False
            win2.Close()


    Cust_Code= values['Cust_Code']
    Cust_Name = values['Cust_Name']
    Cust_Street = values['Cust_Street']
    Cust_City = values['Cust_City']
    Cust_State = values['Cust_State']
    Cust_Zipcode = values['Cust_Zipcode']
    Cust_Country = values['Cust_Country']


    sql_Add_Cust = ("INSERT INTO customer_info VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    data_cust = (customer_num + 10, Cust_Code, Cust_Name, Cust_Street,
                 Cust_City, Cust_State, Cust_Zipcode, Cust_Country)

    if button == 'Add_New_Customer':
        cursor.execute(sql_Add_Cust, data_cust)
        sg.Popup('New Customer "{}" with id number "({})" is added'.format(data_cust[2], data_cust[0]))

    print(values['_LIST_'])
    print(values['_LIST2_'])
    DUT_id = df_ct_danisense.loc[df_ct_danisense['CT_Danisense_Model'] == values['_LIST_']].get('idCT_Danisense').item()
    cust_id = df_customer.loc[df_customer['Customer_Code'] == values['_LIST2_']].get('idCustomer_Info').item()

    sql_Add_DUT = ("INSERT INTO customer_dut VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    data_dut = (customer_dut_num + 2, values['add_dut_sn'], values['add_dut_manufacturer'], values['_LIST_'],
                 values['add_dut_controller'], values['add_dut_controller_sn'], values['add_dut_controller_chan'],
                 values['add_exp_date'], cust_id, DUT_id, 0,0,0)


    if button == 'Add_New_DUT':
        cursor.execute(sql_Add_DUT, data_dut)
        sg.Popup('New DUT "{}" with SN number "({})" belong to "({})"  is added'.format(data_dut[3], data_dut[1],
                                                                                        values['_LIST2_']))

    print(values['_LIST3_'])

    if len(df_dut_customer.loc[df_dut_customer['DUT_SN'] == values['_LIST3_']].get('Customer_CompanyName')) == 1:
        DUT_id_SN = df_dut_customer.loc[df_dut_customer['DUT_SN'] == values['_LIST3_']].get('idCustomer_DUT').item()
        cust_id_SN = df_dut_customer.loc[df_dut_customer['DUT_SN'] == values['_LIST3_']] \
            .get('Customer_Info_idCustomer_Info').item()
        print(type(DUT_id_SN))
        print(type(cust_id_SN))
    else:
        # Here is numpy int64, need to convert to int then into database
        sg.Popup('Multiple DUT id assigned for this SN, check DUT above and enter id_DUT in the box')
        DUT_id_SN = int(values['DuplicatedDUTID'])
        print(DUT_id_SN)
        print(df_dut_customer.loc[df_dut_customer['idCustomer_DUT'] == DUT_id_SN].get('Customer_Info_idCustomer_Info'))
        cust_id_SN = int(df_dut_customer.loc[df_dut_customer['idCustomer_DUT'] == DUT_id_SN] \
            .get('Customer_Info_idCustomer_Info').tolist()[0])
        print(type(DUT_id_SN))
        print(type(cust_id_SN))

    sql_Add_Order = ("INSERT INTO callab_order VALUES (%s, %s, %s, %s, %s, %s, %s)")

    orderid = 0





    if button == 'Add_New_Order' and values['DC'] is True:
        cursor.execute("SELECT max(idCallab_Order) FROM callab_order")
        orderid = cursor.fetchone()[0] + 1
        data_order_DC = (orderid, values['add_order_RMA'], values['add_order_ReceiveDate'],
                         DUT_id_SN, cust_id_SN, 1, now.strftime('%Y-%m-%d %H:%M:%S'))
        print(data_order_DC)
        cursor.execute(sql_Add_Order, data_order_DC)
        sg.Popup('New Test Order with with SN number "({})" will be tested at DC"  is added'.format(values['_LIST3_']))
    if button == 'Add_New_Order' and values['AC60Hz'] is True:

        cursor.execute("SELECT max(idCallab_Order) FROM callab_order")
        orderid = cursor.fetchone()[0] + 1
        data_order_AC60Hz = (orderid, values['add_order_RMA'], values['add_order_ReceiveDate'],
                             DUT_id_SN, cust_id_SN, 2, now.strftime('%Y-%m-%d %H:%M:%S'))
        print(data_order_AC60Hz)
        cursor.execute(sql_Add_Order, data_order_AC60Hz)
        sg.Popup('New Test Order with with SN number "({})" will be tested at AC60Hz"  is added'.
                 format(values['_LIST3_']))
    if button == 'Add_New_Order' and values['AC400Hz'] is True:

        cursor.execute("SELECT max(idCallab_Order) FROM callab_order")
        orderid = cursor.fetchone()[0] + 1
        data_order_AC400Hz = (orderid, values['add_order_RMA'], values['add_order_ReceiveDate'],
                              DUT_id_SN, cust_id_SN, 3, now.strftime('%Y-%m-%d %H:%M:%S'))
        print(data_order_AC400Hz)
        cursor.execute(sql_Add_Order, data_order_AC400Hz)
        sg.Popup('New Test Order with with SN number "({})" will be tested at AC400Hz"  is added'.
                 format(values['_LIST3_']))
    if button == 'Add_New_Order' and values['AC50Hz'] is True:

        cursor.execute("SELECT max(idCallab_Order) FROM callab_order")
        orderid = cursor.fetchone()[0] + 1
        data_order_AC50Hz = (orderid, values['add_order_RMA'], values['add_order_ReceiveDate'],
                             DUT_id_SN, cust_id_SN, 4, now.strftime('%Y-%m-%d %H:%M:%S'))
        print(data_order_AC50Hz)
        cursor.execute(sql_Add_Order, data_order_AC50Hz)
        sg.Popup('New Test Order with with SN number "({})" will be tested at AC50Hz"  is added'.
                 format(values['_LIST3_']))


cnx.commit()
cursor.close()
cnx.close()



