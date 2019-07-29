import PySimpleGUI as sg
import pandas as pd

import mysql.connector

cnx = mysql.connector.connect(user='root', password='gmw6504192658',
                              host='127.0.0.1',
                              database='ctcal_db')

cursor = cnx.cursor()


sql_Cust_Code_Name = ("SELECT idCustomer_Info, Customer_Code, Customer_CompanyName FROM customer_info")

sql_Cust_DUT = ("SELECT Customer_DUT_SN, Customer_Code, Customer_CompanyName FROM customer_dut "
                "JOIN customer_info ON Customer_Info_idCustomer_Info = idCustomer_Info;")

cursor.execute(sql_Cust_Code_Name)


# Customer_Code_List = []
# Customer_CompanyName_List = []

# for (Customer_Code, Customer_CompanyName) in cursor:
#     Customer_Code_List.append(Customer_Code)
#     Customer_CompanyName_List.append(Customer_CompanyName)

# https://pbpython.com/pandas-list-dict.html
df_customer = pd.DataFrame.from_records(list(cursor.fetchall()), columns=['idCustomer_Info', 'Customer_Code', 'Customer_CompanyName'])


cursor.execute(sql_Cust_DUT)




df_dut_customer = pd.DataFrame.from_records(list(cursor.fetchall()),
                                            columns=['DUT_SN', 'Customer_Code', 'Customer_CompanyName'])
customer_num = len(df_customer.index)

customer_dut_num = len(df_dut_customer.index)


sql_ct_danisense = ("SELECT idCT_Danisense, CT_Danisense_Model FROM ct_danisense")
cursor.execute(sql_ct_danisense)
df_ct_danisense = pd.DataFrame.from_records(list(cursor.fetchall()), columns=['idCT_Danisense', 'CT_Danisense_Model'])

Danisense_Models = df_ct_danisense['CT_Danisense_Model'].tolist()
Customer_Code_list = df_customer['Customer_Code'].tolist()


layout1 = [[sg.Text('Check Customer Name with Code', font='Helvetica 15')],
           [sg.Text('Customer Code: '), sg.InputText(default_text='YOKGA1', size=(12, 1), key='Customer_Code')],
           [sg.Text('Customer Name: '), sg.Text('', size=(80, 1), key='Customer_Name')],
           [sg.Text('')],
           [sg.ReadButton('Search'), sg.Button('Show all Customer')],
           [sg.Text('Check DUT', font='Helvetica 15')],
           [sg.Text('DUT SN: '), sg.InputText(default_text='9113250015', size=(12, 1), key='DUT_SN')],
           [sg.Text('Customer Name: '), sg.Text('', size=(80, 1), key='Customer_Name_DUT')],
           [sg.Text('')],
           [sg.ReadButton('Search_DUT')],
           [sg.Text('Add New Customer (Code/Name/Street/City/State/Zip/Country', font='Helvetica 15')],
           [sg.InputText(default_text='GMW_Code', size=(12, 1), key='Cust_Code'),
            sg.InputText(default_text='GMW Associates', size=(18, 1), key='Cust_Name'),
            sg.InputText(default_text='955 Industrial', size=(15, 1), key='Cust_Street')],
           [sg.InputText(default_text='San Carlos', size=(10, 1), key='Cust_City'),
            sg.InputText(default_text='CA', size=(8, 1), key='Cust_State'),
            sg.InputText(default_text='94563', size=(8, 1), key='Cust_Zipcode'),
            sg.InputText(default_text='USA', size=(10, 1), key='Cust_Country')],
           [sg.ReadButton('Add_New_Customer')],
           [sg.Text('')],
           [sg.Text('Add New DUT (SN/Manufacturer/Model/Controller/Control_SN/Control_Chan/ExpDate/Cust_Code',
                    font='Helvetica 15')],
           [sg.Button('Show all DUT Model in the database')],
           [sg.InputText(default_text='add_dut_sn', size=(12, 1), key='add_dut_sn'),
            sg.InputText(default_text='add_dut_manufacturer', size=(12, 1), key='add_dut_manufacturer'),
            sg.Listbox(Danisense_Models, default_values='DS200IDSA', size=(20,1), enable_events=True, key='_LIST_')],
           [sg.InputText(default_text='add_dut_controller', size=(10, 1), key='add_dut_controller'),
            sg.InputText(default_text='add_dut_controller_sn', size=(8, 1), key='add_dut_controller_sn'),
            sg.InputText(default_text='controller_chan', size=(8, 1), key='add_dut_controller_chan'),
            sg.InputText(default_text='add_exp_date', size=(10, 1), key='add_exp_date'),
            sg.Listbox(Customer_Code_list, default_values='GMWI1', size=(20,1), enable_events=True, key='_LIST2_')],
           [sg.ReadButton('Add_New_DUT')],
           [sg.Button('Exit')]]   # Button close the window

window1 = sg.Window(title='check customer name', size=(1200, 800), grab_anywhere=False).Layout(layout1)

win2_active = False

win3_active = False

while True:
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
    if SN in list(df_dut_customer['DUT_SN'].tolist()):
        Cust_Name_DUT = df_dut_customer.loc[df_dut_customer['DUT_SN'] == SN].get('Customer_CompanyName').item()
    else:
        Cust_Name_DUT = 'DUT SN Not in the database'

    if button == 'Search_DUT':
        window1.FindElement('Customer_Name_DUT').Update(Cust_Name_DUT)  # output with key and Update

    if not win2_active and button == 'Show all Customer':
        win2_active = True
        layout2 = [[sg.Text('Show all Customer Name')],
                   [sg.Table(values=df_customer.values.tolist(), headings=['idCustomer_Info','Code', 'Name'], display_row_numbers=True,
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
    DUT_id = df_ct_danisense.loc[df_ct_danisense['CT_Danisense_Model'] == values['_LIST_'][0]].get('idCT_Danisense').item()
    cust_id = df_customer.loc[df_customer['Customer_Code'] == values['_LIST2_'][0]].get('idCustomer_Info').item()

    sql_Add_DUT = ("INSERT INTO customer_dut VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    data_dut = (customer_dut_num + 2, values['add_dut_sn'], values['add_dut_manufacturer'], values['_LIST_'][0],
                 values['add_dut_controller'], values['add_dut_controller_sn'], values['add_dut_controller_chan'],
                 values['add_exp_date'], cust_id, DUT_id, 0,0,0)

    if button == 'Add_New_Customer':
        cursor.execute(sql_Add_DUT, data_dut)
        sg.Popup('New DUT "{}" with id number "({})" is added'.format(data_cust[2], data_cust[0]))

cnx.commit()
cursor.close()
cnx.close()



