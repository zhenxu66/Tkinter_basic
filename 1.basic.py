import tkinter as tk

root = tk.Tk()
root.title("Test Window")
root.geometry('200x700')



# ------------Label-----------------
# object first capitalized, width & height by char
# label1 = tk.Label(root, text='Trial', bg='red', font=('Arial', 12), width=15, height=3)
text_var = tk.StringVar()

label1 = tk.Label(root, textvariable=text_var, bg='red', font=('Arial', 12), width=15, height=3)
label1.pack()  # put in next place or place

# ------------Button-----------------
on_hit = False
def func_hit():
    global on_hit
    if on_hit == False:
        on_hit = True
        text_var.set('Hit the button')
    else:
        on_hit = False
        text_var.set('')

botton1 = tk.Button(root, text='hit me', width=15, height=2, command=func_hit)
botton1.pack()

# ------------Entry--Text--------
entry1 = tk.Entry(root, show='*')
entry1.pack()
text1 = tk.Text(root, height=2)
text1.pack()

def insert_point():
    var = entry1.get()
    text1.insert('insert', var)

def insert_end():
    var = entry1.get()
    text1.insert('end', var)


button2_1 = tk.Button(root, text='insert point', width=15, height=2, command=insert_point)
button2_1.pack()

button2_2 = tk.Button(root, text='insert end', width=15, height=2, command=insert_end)
button2_2.pack()

button2_3 = tk.Button(root, text='clear', width=15, height=2, command=lambda: text1.delete(1.0, tk.END))
button2_3.pack()

# ------------Listbox--------

text_var2 = tk.StringVar()

label2 = tk.Label(root, textvariable=text_var2, bg='yellow', font=('Arial', 12), width=6, height=3)
label2.pack()


var2 = tk.StringVar()
var2.set((11, 22, 33, 'last'))  # 为变量设置值
listbox1 = tk.Listbox(root, height=6, listvariable=var2)  #将var2的值赋给Listbox

# 创建一个list并将值循环添加到Listbox控件中
# list_items = [1,2,3,4]
# for item in list_items:
#     listbox1.insert('end', item)  #从最后一个位置开始加入值
listbox1.insert(0, 'first')       #在第一个位置加入'first'字符
listbox1.insert(1, 'second')      #在第二个位置加入'second'字符
listbox1.delete(1)                #删除第二个位置的字符
listbox1.pack()


def print_from_list():
    value = listbox1.get(listbox1.curselection())   # 获取当前选中的文本 curselection
    text_var2.set(value)     # 为label设置值

button3 = tk.Button(root, text='print selection', width=15, height=2, command=print_from_list)
button3.pack()


# ------------Radiobutton--------

var_label = tk.StringVar()
label3 = tk.Label(root, bg='green', width=20, text='empty')  # label can be config with new text
label3.pack()

def print_rd_selection():
    label3.config(text='you have selected ' + var_label.get())   # Label.config(text = ) update text file inside a Label


# use value into same variable,which will be passed into label config updated text
radiobutton1 = tk.Radiobutton(root, text='Option A',  variable=var_label, value='A', command=print_rd_selection)
radiobutton2 = tk.Radiobutton(root, text='Option B',  variable=var_label, value='B', command=print_rd_selection)
radiobutton1.pack()
radiobutton2.pack()

# ------------Scale--------

# scale1 = tk.Scale(root, label='Value_slide', from_=0, to=0.08, orient=tk.HORIZONTAL, length=200, showvalue=0,
#                   tickinterval=)



# like while to refresh window

root.mainloop()