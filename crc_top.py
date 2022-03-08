# -*- coding: utf-8 -*-

from tkinter import *
import tkinter.ttk as ttk
#from tkinter.ttk import *
from remove_Char.remove_Char import remove_Char
from CRC_Generator.CRC_Generator import crc_Generator

from ToolTip.ToolTip import ToolTip as TTip

debugging = False

tooltip_time = 50000

class topCRC(Frame):

    def __init__(self, parent = None, crc_selection_presets = ["CCIT XMODEM: 0x11021"], log_name = "Empty.txt"):
        Frame.__init__(self, parent)
        #self.master = Frame(parent)
        #self.master.pack()

        self.log_name = log_name
        self.crc_selection_presets = crc_selection_presets
        self.crc = None
        self.Error = 0
        self.createWidgets()


    def createWidgets(self):

        self.widg1 = Label( self.master, text = "Calculate single CRC Remainder", font = ('Times', '16', 'underline') )
        self.widg1.grid(row = 0, column = 0, columnspan = 3, sticky = W)

        self.widg1.ToolTip = TTip(self.widg1, text = "Calculate the CRC remainder for a specific chunk of data.")

        self.widg2 = Label(self.master, text = "Enter Data: ")
        self.widg2.grid(row = 1, column = 0, sticky = W)

        self.widg2.ToolTip = TTip(self.widg2, text = """The data you want to generate a CRC remainder for.\nNeeds to be in hex formax\n0x### where 0 is zero""", time = tooltip_time)

        self.data = StringVar()
        #self.widg3 = Entry( self.master, textvariable = self.data, width = 20 )
        self.widg3 = Text( self.master, width = 20, height = 1 )
        self.widg3.insert(str(0+1)+".0", "0x####" )
        self.widg3.grid( row = 1, column = 1 )

        self.widg3.ToolTip = TTip(self.widg3, text = """The data you want to generate a CRC remainder for.\nNeeds to be in hex formax\n0x### where 0 is zero""", time = tooltip_time)

        self.widg4 = Label( self.master, text = "Data Length: " )
        self.widg4.grid( row = 2, column = 0, sticky =  W )

        self.widg4.ToolTip = TTip(self.widg4, text = "Length of an integer when represented in binary\nSo 9 => 1001 would be 4 bits long",  time = tooltip_time)

        self.data_length = StringVar()
        #self.widg5 = Entry( self.master, textvariable = self.data_length, width = 20 )
        self.widg5 = Text( self.master, width = 20, height = 1 )
        self.widg5.insert (1.0, "# of bits")
        self.widg5.grid( row = 2, column = 1)

        self.widg5.ToolTip = TTip(self.widg5, text = "Length of an integer when represented in binary\nSo 9 => 1001 would be 4 bits long", time = tooltip_time)

        self.widg6 = Label( self.master, text = "CRC Code:         " )
        self.widg6.grid( row = 3, column = 0, sticky = W )

        self.widg6.ToolTip = TTip(self.widg6, text = "Length of an integer when represented in binary\nSo 9 => 1001 would be 4 bits long", time = tooltip_time)



        self.crc_selection = StringVar()
        self.widg7 = ttk.Combobox(self.master, textvariable = self.crc_selection, width = 20 )
        string = []
        string.append(" ")
        for element in self.crc_selection_presets:
            string.append(element)
        string.append("Manual")
        self.widg7["values"] = string
        self.widg7.current(0)
        self.widg7.grid( row = 3, column = 1, sticky = W  )
        self.widg7.bind("<<ComboboxSelected>>", ( lambda inputs = 0: self.dropdown_selection() ) )
        self.widg7.config( state = 'readonly' )

        self.widg7.ToolTip = TTip(self.widg7, text = """Blank to Reset the selection.\nManual to Enter your own custom CRC Code.\nNote most CRC codes are pre-trimmed.\nSo Xmodem 0x11021 is usually listed as 0x1021 in textbooks.\nEnsure you provide a non-trimmed CRC """, time = tooltip_time)

        self.crc_code = StringVar()
        #self.widg8 = Entry( self.master, textvariable = self.crc_code, width = 20)
        self.widg8 = Text(self.master, width = 20, height = 1)
        self.widg8.insert(1.0, "0x####")
        self.widg8.config( state = DISABLED )
        self.widg8.grid(row = 3, column = 2)
        self.widg8.config( bg = 'light gray' )
        self.widg8.ToolTip = TTip(self.widg8, text = "Editable only when you select \"Manual\" mode", time = tooltip_time)

        self.widg9 = Label(self.master, text = "Result: ")
        self.widg9.grid(row = 4, column = 0, sticky = W )

        self.widg9.ToolTIp = TTip(self.widg9, text = "Result given in hexademical", time = tooltip_time)

        self.result = StringVar()
        #self.widg10 = Entry( self.master, textvariable = self.result, width = 20 )
        self.widg10 = Text( self.master, width = 20, height = 1 )
        self.widg10.insert( 1.0, "0x####" )

        self.widg10.config( state = DISABLED )
        self.widg10.grid( row = 4, column = 1 )
        self.widg10.config( bg = "light gray" )

        self.widg10.ToolTIp = TTip(self.widg10, text = "Result given in hexademical", time = tooltip_time)

        self.widg11 = Button(self.master, text = "Calculate", command = self.calculate_button)
        #self.widg11.config( bd = 5 )
        self.widg11.grid(row = 5, column = 3, sticky = E)
        #self.widg11.bind("<Button 1>", self.calculate_button())

        self.widg11.ToolTip = TTip(self.widg11, text = "3...2...1...Liftoff", time = tooltip_time)

    def dropdown_selection(self):


        temp = self.crc_selection.get()                                        # Return Current Selection
        options = self.widg7['values']                                         # Return array of all possible selections
        #print("options")
        #print(options)
        #print("selection:", temp, "!")

        ## Update the Adjacent Text Entry
        for element in options:

            ## If selection is the blank option, reset the textbox
            if temp == " ":
                #print("empty")
                self.widg8.config( state = NORMAL )                            # Convert text box to Enabled mode to update
                self.widg8.delete(1.0, END)                                      # Clear the text box
                self.widg8.insert(1.0, "0x####")                                 # Reset to default message
                self.widg8.config( state = DISABLED )                        # Reset textbox to read only
                self.widg8.config( bg = 'light gray' )
                break

            ## If selection is Manual, then enable textbox to be edited
            elif temp == "Manual":
                #print("manual")
                self.widg8.focus_set()
                self.widg8.config( state = NORMAL )                            # Convert Text Box to Enabled mode
                self.widg8.delete(1.0, END)                                      # Clear the text box
                self.widg8.insert(1.0, "0x")                                     # Number should be in hex form
                self.widg8.mark_set("insert", 'end')
                self.widg8.config( bg = "white")
                #print("Cursor: "  )
                #self.widg8.mark_set(END)
                break

            ## If selection is a preset CRC value, then extract the CRC Value and write it to the textbox
            elif temp == element:
                ## Strip out the CRC string
                i = 0
                for letter in element:                                         # Check letter by letter
                    if i + 1 < len(element):                                   # Shy of the last element
                        if element[i] + element[i+1] == "0x":                  # Check for the hex "0x" signifier
                            self.crc = element[i:]                                  # Grab the String
                            self.crc = remove_Char(self.crc, " ")                        # Remove any spaces or empty space
                    i = i + 1
                self.widg8.config( state = NORMAL )                            # Text Box needs to be editable to be updated
                self.widg8.delete(1.0, END)                                      # Clear Text Box
                self.widg8.insert(1.0, str(self.crc))                                      # Write Anew to text box
                self.widg8.config( state = DISABLED)                          # Reset textbox to read only
                self.widg8.config( bg = 'light gray' )
                break


    def calculate_button(self):
        ## obtain inputs
        ## check inputs are correct
        ## invoke crc calculator
        ## print results to screen

        ## Obtain Inputs
        data = self.widg3.get(1.0, 'end')
        data_length = self.widg5.get(1.0, 'end')
        crc = self.widg8.get(1.0, 'end')

        ## Preprocess Inputs, Remove Empty Space
        data = remove_Char( data, " ")
        data_length = remove_Char( data_length, " ")
        crc = remove_Char( crc, " ")

        ## Check Inputs
        try:
            data = int(data, 16)
        except:
            self.error_notification = "Input Error: Improper User Entry in \"Enter Data\" Data"
            self.userNotification(self.error_notification)
            return None

        try:
            data_length = int(data_length, 10)
        except:
            self.error_notification = "Input Error: Improper User Entry in \"Data Length\""
            self.userNotification(self.error_notification)
            return None

        try:
            crc = int(crc, 16)
            self.Error = 0

        except:
            self.error_notification = "Input Error: Improper User Entry in \"CRC Code\""
            self.userNotification(self.error_notification)
            return None


        if self.Error == 0:
            crc_calculation = crc_Generator(data_length = data_length, crc_code = crc)
            crc_calculation.generate_Remainder(data = data)
            Remainder = crc_calculation.return_Remainder()
            Error = crc_calculation.return_Error()
            if Error != 0:
                self.Error = 1
                self.error_notification = "CRC Calculation Error: Problem with underlying mathematical CRC operations"
                self.userNotification(self.error_notification)
                return None

        if self.Error != 0:
            self.widg10.config( state = NORMAL )
            self.widg10.delete( 1.0, 'end' )
            self.widg10.insert( 1.0, "Error" )
            self.widg10.config( state = DISABLED )
        else:
            self.widg10.config( state = NORMAL )
            self.widg10.delete( 1.0, 'end' )
            self.widg10.insert( 1.0, hex(Remainder) )
            self.widg10.config( state = DISABLED )


        self.userNotification()


    def userNotification(self, error_input = 0):
        print(error_input)






















if __name__ == "__main__":
    debugging = True

    Root = Tk()

    test1 = Label(Root, text = "test")
    test1.pack()

    Frame_test = Frame(Root)
    Frame_test.pack()


    test = topCRC(Frame_test)

    Root.mainloop()






