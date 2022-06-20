from LITHO_package import *
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu



class ButtonFactory():
    def createButton(self, type_):
        return buttonTypes[type_]()


class ButtonBase():
    def __init__(self):

        self.kwarg = {}
        self.kwarg['relief'] = 'flat'
        self.kwarg['foreground'] = 'white'
        self.kwarg['background'] = colorGray
        self.kwarg['activeforeground'] = 'white'
        self.kwarg['activebackground'] = colorGray
        self.kwarg['highlightthickness'] = 0
        self.kwarg['width'] = 1
        self.kwarg['font'] = fontMiddleLabel

    def getButtonConfig(self):
        return self.kwarg


class ButtonRidge(ButtonBase):

    def __init__(self):
        # super().__init__() # same
        super(ButtonRidge,self).__init__()
        self.kwarg['foreground'] = 'red'
        self.kwarg['background'] = colorRed
        self.kwarg['activebackground'] = colorRed


buttonTypes = [ButtonRidge]
#
#
# class ButtonSunken(ButtonBase):
#     relief = 'sunken'
#     foreground = 'blue'
#
#
# class ButtonGroove(ButtonBase):
#     relief = 'groove'
#     foreground = 'green'

#
# key.title('On Screen Keyboard')
#
#
# key.geometry('800x480')  # Window size
# key.minsize(width=800, height=480)
# key.maxsize(width=800, height=480)
#
# style = ttk.Style()
# key.configure(bg='gray27')
# style.configure('TButton', background='gray21')
# style.configure('TButton', foreground='white')
#
# theme = "light"





# showing all data in display


# Necessary functions



class ButtonFactory():

    def __init__(self):
        self.win = tk.Tk()
        self.style = ttk.Style()
        self.createWidgets()
        self.exp = ""
        self.win_init_config()

    def win_init_config(self):
        self.win.overrideredirect(True) #rm window bar
        self.menuBar.delete(0, tk.END) #rm menu bar
        self.style.layout('TNotebook.Tab', []) #rm tab bar
        # self.win.geometry('800x480')  # Window size
        # self.win.minsize(width=800, height=480)
        # self.win.maxsize(width=800, height=480)

    def Backspace(self):
        self.exp = self.exp[:-1]
        self.equation.set(self.exp)

    def press(self, num):
        self.exp = self.exp + str(num)
        self.equation.set(self.exp)

    def Clear(self):
        self.exp = ""
        self.equation.set(self.exp)

    def Submit(self):
        submit = self.exp
        if submit == "1111":
            print("Right")
            self._quit()
        else :
            self.Clear()

    def _quit(self):
        self.win.quit()
        self.win.destroy()
        exit()

    def createWidgets(self):
        tabControl = ttk.Notebook(self.win)
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text='Tab 1')
        tabControl.pack(expand=1, fill="both")
        self.monty = ttk.LabelFrame(tab1, text=' Monty Python ')
        self.monty.grid(column=0, row=0, padx=8, pady=4)

        scr = scrolledtext.ScrolledText(self.monty, width=30, height=3, wrap=tk.WORD)
        scr.grid(column=0, row=3, sticky='WE', columnspan=3)

        self.menuBar = Menu(tab1)
        self.win.config(menu=self.menuBar)
        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)
        self.helpMenu = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)

        self.createButtons()
        self.createEntry()

    def createEntry(self):
        self.equation = tk.StringVar()
        Dis_entry = ttk.Entry(self.monty, state='readonly', textvariable=self.equation)
        Dis_entry.grid(row=4, column=0, rowspan=1, columnspan=100, ipadx=999, ipady=20)

    def createButtons(self):
        factory = ButtonFactory()

        # 계산기 grid 만들어보자.
        cal_grid = [(i, j) for i in range(2) for j in range(5)]
        cal_grid_kwarg = [{"row": grid[0], "column": grid[1]} for grid in cal_grid]

        # 계산기 Text 만들어보자
        numlist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        numlist = [str(num) for num in numlist]
        print(numlist)

        # # Button 0
        kwarg_button0 = factory.createButton(0).getButtonConfig()
        button0 = tk.Button(self.monty, **kwarg_button0)
        button0.grid(column=8, row=8)

        for i in range(10):
            # btn = ttk.Button(self.monty, text = numlist[i], command=lambda s=numlist[i]: self.press(s), **cal_grid_kwarg[i], **kwarg_button0)
            btn = tk.Button(self.monty, text = numlist[i], command=lambda s=numlist[i]: self.press(s), **kwarg_button0)
            btn.grid(**cal_grid_kwarg[i])

        buttonEnter = tk.Button(self.monty, text = "Submit", command=lambda:self.Submit(), **kwarg_button0)
        buttonEnter.grid(column=10,row=10)

        buttonQuit = tk.Button(self.monty, text="Quit", command=lambda:self._quit(), **kwarg_button0)
        buttonEnter.grid(column=20,row=20)

        # # Button 1
        # rel = factory.createButton(0).getButtonConfig()[0]
        # fg = factory.createButton(0).getButtonConfig()[1]
        # action = tk.Button(self.monty, text="Button " + str(0 + 1), relief=rel, foreground=fg)
        # action.grid(column=0, row=1)
        #
        # # Button 2
        # rel = factory.createButton(1).getButtonConfig()[0]
        # fg = factory.createButton(1).getButtonConfig()[1]
        # action = tk.Button(self.monty, text="Button " + str(1 + 1), relief=rel, foreground=fg)
        # action.grid(column=1, row=1)
        #
        # # Button 3
        # rel = factory.createButton(2).getButtonConfig()[0]
        # fg = factory.createButton(2).getButtonConfig()[1]
        # action = tk.Button(self.monty, text="Button " + str(2 + 1), relief=rel, foreground=fg)
        # action.grid(column=2, row=1)

    #         # using a loop to do the above


#         for idx in range(len(buttonTypes)):
#             rel = factory.createButton(idx).getButtonConfig()[0]
#             fg  = factory.createButton(idx).getButtonConfig()[1]
#
#             action = tk.Button(self.monty, text="Button "+str(idx+1), relief=rel, foreground=fg)
#             action.grid(column=idx, row=1)




# ==========================

ButtonFactory = ButtonFactory()
ButtonFactory.win.mainloop()