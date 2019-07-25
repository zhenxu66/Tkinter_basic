import PySimpleGUI as sg
import PySimpleGUIQt as sg_qt



# PySimpleGUI is a wrapper for Tkinter and Qt
# Text
# Input Text
# Checkbox
# Radio Button
# Slider


# layout

layout = [ [sg.Text('Wghat is your name?')],
           [sg.InputText()],
           [sg.Button('OK')]]


layout2 = [ [sg.Text('Hello what is your name?')],
           [sg.Input()],
           [sg.Text('Do you like:')],
           [sg.Checkbox('Ice cream'), sg.Checkbox('Hot dogs'), sg.Checkbox('Beer')],
           [sg.Text('What is your favorite ice cream flavor')],
           [sg.Radio('Vanilla', 'icecream'), sg.Radio('Chocolate', 'icecream'), sg.Radio('Strawberry', 'icecream')],
           [sg.Text('How much do you like Python')],
           [sg.Slider((0, 100), orientation='h', size=(15, 20))],  # size in pixel
           [sg.OK(), sg.Cancel()]]

# keys to link parts inside UI

layout3 = [[sg.Text('Add 2 Numbers', font='Helvetica 15')],
          [sg.InputText(size=(8,1) ,key='in1'), sg.Text(' + '), sg.Input(size=(8,1), key='in2'),sg.Text('', size=(8,1), key='answer')],
          [sg.Text('')],
          [sg.ReadButton('Add')]]   # Button close the window

# window create
window = sg.Window('Window').Layout(layout)

window2 = sg.Window('Quiz of what you like').Layout(layout2)

window3 = sg.Window('Add 2 numbers').Layout(layout3)

# read window


button, values = window.Read()

sg.Popup('Hello {} welcome'.format(values[0]))

button2, values2 = window2.Read()

sg.Popup(button2, values2)

# event loop
# while True:
#     button, values = window3.Read()
#
#     if button is None:
#         break  # close the window and quit the while
#
#     num1 = int(values['in1'])  # convert text to num
#     num2 = int(values['in2'])
#
#     answer = num1+num2
#
#     window3.FindElement('answer').Update(answer)  # output with key and Update

# pyinstaller.exe --onefile --windowed --icon=app.ico app.py