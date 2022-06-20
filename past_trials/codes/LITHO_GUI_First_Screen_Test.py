from LITHO_FUNC import *

########################################
############# UI Section ##############
######################################

#================================
# Root
#===============================
global root
root = tk.Tk()
root.wm_geometry("800x480")
root.resizable(False, False)
root.attributes('-fullscreen', True)


#================================
# Root - All Frames
#=================================

#UI Component
frameTop = tk.Frame(root, height=480, width=800, bg=LITHO_Design.colorDarkGray)
frameButton = tk.Frame(root, height=290, width=800, bg=LITHO_Design.colorDarkGray)
framePaused = tk.Frame(root, height=310, width=634, bg=LITHO_Design.colorIvory, highlightthickness=2,
                       highlightbackground="gray")
tabSetting = ttk.Notebook(root, width=800, height=480)
frameSplash = tk.Frame(root, height=480, width=800, bg=LITHO_Design.colorDarkGray)


# Positioning
frameTop.place(x=0, y=0)
frameButton.place(x=1, y=190)  ## to hide 1 pixel vertical line by tabSetting notebook widget

tabSetting.place(x=0, y=0)
frameSplash.place(x=0, y=0)

#Binding
tabSetting.bind("<<NotebookTabChanged>>", tabChanged)

#==============================
# Root-frameSplash
#================================
# variable
tempImage3 = PhotoImage(file="../images/cella_logo.png")
tempImage3 = tempImage3.subsample(2, 2) #이미지 작게 만들기
# UI component
Splash_Logo = tk.Label(frameSplash, image=tempImage3, bg="black")
labelForLogo = tk.Label(frameSplash, text="Please touch the screen", bg="black", fg="white", font=LITHO_Design.fontSmallLabel)

# Positioning
Splash_Logo.place(in_=frameSplash, x=0, y=0, width=800, height=480)
labelForLogo.place(in_=frameSplash, x=300, y=390, width=220, height=20)

# Binding
Splash_Logo.bind("<Button-1>", lambda event: OpStatusChange("FIRST_TOUCH"))



frameSplash.lift()
#======================
# Start GUI
#=======================
root.mainloop()

######## references
##       btnFrame.place_forget()