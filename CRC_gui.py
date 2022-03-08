# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 14:19:42 2022

@author: Main Floor
"""


from tkinter import *
from tkinter.messagebox import *
import tkinter.ttk as ttk
from tkinter.filedialog import *
from remove_Char.remove_Char import remove_Char
from CRC_Generator.CRC_Generator import crc_Generator
import os

debugging = False

class crc_GUI(Frame):
    def __init__(self, parent = None, Root = None):

        Frame.__init__(self, parent)
        #self.pack(expand = YES, fill = BOTH)

        self.Root = Root

        #self.master.title("CRC Generator")
        #self.master.iconbitmap("file.ico") #figure this out

        self.createWidgets()


    def createWidgets(self):
        self.menuBar()
        #self.toolBar()
        #self.upperCRC()
        #self.lowerCRC()


    def menuBar(self):
        self.menuBar = Menu(self.master)
        self.Root.config(menu = self.menuBar)
        self.fileMenu()
        self.formattingMenu()
        self.codesMenu()
        self.helpMenu()
        self.aboutMenu()


    def fileMenu(self):
        file_pulldown = Menu(self.menuBar, tearoff = False)                               # initialize menu dropdown
        file_pulldown.add_command(label = "Save to folder", command = self.saveto_menu)   # add pulldown options
        file_pulldown.add_command(label = "Exit", command = sys.exit)
        self.menuBar.add_cascade(label = "File", menu = file_pulldown)                    # tie menu drop down to menu

    def saveto_menu(self):
        showerror("Not Implemented", "Option Not Available")


    def formattingMenu(self):
        formatting_pulldown = Menu(self.menuBar, tearoff = False)
        try:
            location = os.getcwd() + os.sep + "SupportFiles" + os.sep + "formatting.txt"
            file = open(location, 'r')
        except:
            print("No formatting text file")
            #shutdown program?
        options = file.readlines()
        file.close()

        print(options)
        index = []
        title = []
        formatting = []
        i = 0
        for option in options:
            index = option.index(",")

            temp_Title = option[0:index]
            temp_Title = remove_Char(temp_Title, " ")
            temp_Title = remove_Char(temp_Title, "\n")
            title.append(temp_Title)

            temp_formatting = option[index+1:]
            #temp_formatting = remove_Char(temp_formatting, " ")
            temp_formatting = remove_Char(temp_formatting, "\n")
            formatting.append(temp_formatting)

            if debugging == True: print(title[i])
            if debugging == True: print(formatting[i])
            formatting_pulldown.add_command( label = title[i], command = lambda i = i, title = title[i], formatting = formatting[i]: self.formatting_output_menu( i, title, formatting ) )
            i = i + 1
        self.menuBar.add_cascade(label = "Formatting", menu = formatting_pulldown)




    def formatting_output_menu(self, index, title, formatting):
        showerror("Not Implemented", "Option Not Availabe")

    def codesMenu(self):
        codes_pulldown = Menu(self.menuBar, tearoff = False)
        try:
            location = os.getcwd() + os.sep + "SupportFiles" + os.sep + "crc_codes.txt"
            file = open(location, 'r')
        except:
            print("No crc Codes text file")
        options = file.readlines()
        file.close()

        index = []
        title = []
        code = []
        i = 0
        for option in options:

            line = option.split(":")

            line = option.split(":")
            if len(line) != 2: continue


            line[0] = line[0].strip("\n")
            line[0] = line[0].strip()
            if line[0] == "": continue

            line[1] = line[1].strip("\n")
            line[1] = line[1].strip()
            if line[1] == "": continue


            temp_Title = line[0]
            temp_Title = remove_Char(temp_Title, "\n")
            temp_Title = temp_Title.strip()

            title.append(temp_Title)
            #print("Title:", title)


            temp_Code = line[1]
            temp_Code = remove_Char(temp_Code, "\n")
            temp_Code = temp_Code.strip()

            code.append(temp_Code)
            #print("Code:", temp_Code)

            if debugging == True: print(title[i])
            if debugging == True: print(code[i])

            codes_pulldown.add_command( label = title[i] + ": " + code[i], command = lambda i = i: self.crc_codes_menu(i, title, code))
            i = i + 1
        self.menuBar.add_cascade(label = "Codes", menu = codes_pulldown)



    def crc_codes_menu(self, i, title, code):
        pass




    def helpMenu(self):
        help_pulldown = Menu(self.menuBar, tearoff = False)
        help_pulldown.add_command(label = "CRC PDF", command = self.helpMenu_CRC)
        help_pulldown.add_command(label = "Help Files", command = self.helpMenu_Help)
        self.menuBar.add_cascade(label = "Help", menu = help_pulldown)

    def helpMenu_CRC(self):
        pass

    def helpMenu_Help(self):
        pass


    def aboutMenu(self):
        about_pulldown = Menubutton(self.menuBar)
        self.menuBar.add_cascade(label = "About", menu = about_pulldown, command = self.about)

    def about(self, event = None):
        pass








if __name__ == "__main__":
    debugging = True
    Root = Tk()

    testFrame = Frame(Root)
    testFrame.pack()

    Gui = crc_GUI(parent = testFrame, Root = Root)

    Root.mainloop()
