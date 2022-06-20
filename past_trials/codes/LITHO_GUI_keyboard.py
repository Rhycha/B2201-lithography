from pj_litho_codes.codes.LITHO_GUI_ButtonFactory import *
key = tk.Tk()

key.title('On Screen Keyboard')


key.geometry('800x480')  # Window size
key.maxsize(width=800, height=480)
key.minsize(width=800, height=480)

style = ttk.Style()
key.configure(bg='gray27')
style.configure('TButton', background='gray21')
style.configure('TButton', foreground='white')

theme = "light"


# entry box
equation = tk.StringVar()
Dis_entry = ttk.Entry(key, state='readonly', textvariable=equation)
Dis_entry.grid(rowspan=1, columnspan=100, ipadx=999, ipady=20)


# showing all data in display
exp = " "

# Necessary functions


def press(num):
    global exp
    exp = exp + str(num)
    equation.set(exp)


def Backspace():
    global exp
    exp = exp[:-1]
    equation.set(exp)



def Clear():
    global exp
    exp = " "
    equation.set(exp)


def Theme():
    global theme
    if theme == "dark":
        key.configure(bg='gray27')
        style.configure('TButton', background='gray21')
        style.configure('TButton', foreground='white')
        theme = "light"
    elif theme == "light":
        key.configure(bg='gray99')
        style.configure('TButton', background='azure')
        style.configure('TButton', foreground='black')
        theme = "dark"


def display():


    # First Line Button
    # Adding keys line wise
    tick = ttk.Button(key, text='`', width=6, command=lambda: press('`'))
    tick.grid(row=1, column=0, ipadx=6, ipady=10)

    num1 = ttk.Button(key, text='1', width=6, command=lambda: press('1'))
    num1.grid(row=1, column=1, ipadx=6, ipady=10)

    num2 = ttk.Button(key, text='2', width=6, command=lambda: press('2'))
    num2.grid(row=1, column=2, ipadx=6, ipady=10)

    num3 = ttk.Button(key, text='3', width=6, command=lambda: press('3'))
    num3.grid(row=1, column=3, ipadx=6, ipady=10)

    num4 = ttk.Button(key, text='4', width=6, command=lambda: press('4'))
    num4.grid(row=1, column=4, ipadx=6, ipady=10)

    num5 = ttk.Button(key, text='5', width=6, command=lambda: press('5'))
    num5.grid(row=1, column=5, ipadx=6, ipady=10)

    num6 = ttk.Button(key, text='6', width=6, command=lambda: press('6'))
    num6.grid(row=2, column=1, ipadx=6, ipady=10)

    num7 = ttk.Button(key, text='7', width=6, command=lambda: press('7'))
    num7.grid(row=2, column=2, ipadx=6, ipady=10)

    num8 = ttk.Button(key, text='8', width=6, command=lambda: press('8'))
    num8.grid(row=2, column=3, ipadx=6, ipady=10)

    num9 = ttk.Button(key, text='9', width=6, command=lambda: press('9'))
    num9.grid(row=2, column=4, ipadx=6, ipady=10)

    num0 = ttk.Button(key, text='0', width=6, command=lambda: press('0'))
    num0.grid(row=2, column=5, ipadx=6, ipady=10)

    minus = ttk.Button(key, text='-', width=6, command=lambda: press('-'))
    minus.grid(row=1, column=11, ipadx=6, ipady=10)

    equal = ttk.Button(key, text='=', width=6, command=lambda: press('='))
    equal.grid(row=1, column=12, ipadx=6, ipady=10)

    backspace = ttk.Button(
        key, text='<---', width=6, command=Backspace)
    backspace.grid(row=1, column=13, ipadx=6, ipady=10)

    # Second Line Buttons


    enter = ttk.Button(key, text='Enter', width=6,
                       command=lambda: press('\n'))
    enter.grid(row=3, column=12, columnspan=2, ipadx=55, ipady=10)

    # Fourth line Buttons


    dot = ttk.Button(key, text='.', width=6, command=lambda: press('.'))
    dot.grid(row=4, column=10, ipadx=6, ipady=10)

    clear = ttk.Button(key, text='Clear', width=6, command=Clear)
    clear.grid(row=4, column=12, columnspan=2, ipadx=55, ipady=10)

    # Fifth Line Buttons

    theme = ttk.Button(key, text='Theme', width=6, command=Theme)
    theme.grid(row=5, column=12, columnspan=2, ipadx=55, ipady=10)

    key.mainloop()


display()