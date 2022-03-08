# -*- coding: utf-8 -*-

from tkinter import *
import tkinter.ttk as ttk
from tkinter.filedialog import *
from remove_Char.remove_Char import remove_Char
from CRC_Generator.CRC_Generator import crc_Generator
import os
from CRC_print.CRC_print_V2 import crc_FileWrite

from ToolTip.ToolTip import ToolTip as TTip

debugging = False

tooltip_time = 5000

class bottomCRC(Frame):

    def __init__(self, parent = None, crc_selection_presets = ["CCIT XMODEM: 0x11021"], log_name = "Empty.txt"):
        Frame.__init__(self, parent)
        if debugging == True: print("Bottom CRC Begins")

        self.log_name = log_name
        self.crc_selection_presets = crc_selection_presets
        self.crc = None
        self.output_dir = None
        self.Error = 0
        self.createWidgets()


    def createWidgets(self):

        self.widg1 = Label( self.master, text = "Bulk Calculate CRC Remainder", font = ('Times', '16', 'underline') )
        self.widg1.grid(row = 0, column = 0, columnspan = 3, sticky = W)
        self.widg1.ToolTip = TTip(self.widg1, text = "Calculates and outputs an entire table of CRC remainders.\nPuts the result into a text file\nFor any possible input data of a given length.\nFor instance, given 4 bit data it will calculate the CRC's for 0000 -> 1111" , time = tooltip_time)

        self.widg2 = Label( self.master, text = "Data Length: " )
        self.widg2.grid( row = 1, column = 0, sticky =  W )
        self.widg2.ToolTip = TTip(self.widg2, text = "How many bits long is your data frame?", time = tooltip_time)

        self.data_length = StringVar()
        #self.widg3 = Entry( self.master, textvariable = self.data_length, width = 20 )
        self.widg3 = Text( self.master, width = 20, height = 1 )
        self.widg3.insert (1.0, "# of bits")
        self.widg3.grid( row = 1, column = 1, sticky = W)
        self.widg3.ToolTip = TTip(self.widg3, text = "How many bits long is your data frame?", time = tooltip_time)

        self.widg4 = Label( self.master, text = "CRC Code:         " )
        self.widg4.grid( row = 2, column = 0, sticky = W )
        self.widg4.ToolTip = TTip(self.widg4, text = """Blank to Reset the selection.\nManual to Enter your own custom CRC Code.\nNote most CRC codes are pre-trimmed.\nSo Xmodem 0x11021 is usually listed as 0x1021.\nEnsure you provide a non-trimmed CRC """, time = tooltip_time)

        self.crc_selection = StringVar()
        self.widg5 = ttk.Combobox(self.master, textvariable = self.crc_selection, width = 17 )
        string = []
        string.append(" ")
        for element in self.crc_selection_presets:
            string.append(element)
        string.append("Manual")
        self.widg5["values"] = string
        self.widg5.current(0)
        self.widg5.grid( row = 2, column = 1, sticky = W  )
        self.widg5.bind("<<ComboboxSelected>>", ( lambda inputs = 0: self.dropdown_selection() ) )
        self.widg5.config( state = 'readonly' )
        self.widg5.ToolTip = TTip(self.widg5, text = """Blank to Reset the selection.\nManual to Enter your own custom CRC Code.\nNote most CRC codes are pre-trimmed.\nSo Xmodem 0x11021 is usually listed as 0x1021 in textbooks.\nEnsure you provide a non-trimmed CRC """, time = tooltip_time)

        self.crc_code = StringVar()
        #self.widg6 = Entry( self.master, textvariable = self.crc_code, width = 20)
        self.widg6 = Text( self.master, width = 20, height = 1)
        self.widg6.insert(1.0, "0x####")
        self.widg6.config( state = DISABLED )
        self.widg6.config( bg = "light gray" )
        self.widg6.grid( row = 2, column = 2 )
        self.widg6.ToolTip = TTip(self.widg6, text = "Editable only when you select \"Manual\" mode", time = tooltip_time)

        self.widg7 = Label( self.master, text = "File Location: " )
        self.widg7.grid( row = 3, column = 0, sticky = W )
        self.widg7.ToolTip = TTip(self.widg7, text = "Select the folder where you want the output to be saved", time = tooltip_time)

        ## Find or Create Directory
        current_dir = os.getcwd()
        if ( os.path.exists( current_dir + os.sep + "output" ) == False ):
            os.mkdir( current_dir + os.sep + "output" )
        self.filepath = current_dir + os.sep + "output" + os.sep

        self.file_dir = StringVar()
        self.widg8 = Entry( self.master, textvariable = self.file_dir, width = 40, font = "TkFixedFont" )
        #self.widg8 = Text(self.master, width = 40, height = 1)
        self.widg8.insert(0, self.filepath)
        self.widg8.xview( END )
        #self.widg8.mark_set( "insert", 'end' )
        self.widg8.config( state = 'readonly')
        self.widg8.config( bg = "light gray" )
        self.widg8.grid( row = 3, column = 1, columnspan = 2, sticky = W)
        self.widg8.ToolTip = TTip(self.widg8, text = "Select the folder where you want the output to be saved", time = tooltip_time)

        self.widg9 = Button(self.master, text = "Browse", command = self.browse_directory)
        self.widg9.grid( row = 3, column = 3, sticky = W )
        self.widg9.ToolTip = TTip(self.widg9, text = "Select the folder", time = tooltip_time)

        self.widg10 = Label( self.master, text = "Output Formatting", font = ('Times', '12', 'underline'))
        self.widg10.grid( row = 4, column = 0, columnspan = 2, sticky = W)
        self.widg10.ToolTip = TTip(self.widg10, text = "How the CRC remainders are formatting in the output text file", time = tooltip_time)

        self.formatting_Frame = Frame(self.master)
        self.formatting_Frame.grid( row = 5, column = 0, columnspan = 3)

        self.formatting_var_type = StringVar()
        #self.widg11 = Entry( self.formatting_Frame, textvariable = self.formatting_var_type, width = 5)
        self.widg11 = Text( self.formatting_Frame, width = 5, height = 1)
        self.widg11.pack( side = LEFT )
        self.widg11.insert(1.0, "int")
        self.widg11.ToolTip = TTip(self.widg11, text = "Formatting: variable type", time = tooltip_time)

        self.widg12 = Label( self.formatting_Frame, text = "CRC_Remainder = ")
        self.widg12.pack( side = LEFT, expand = YES, fill = "x")
        self.widg12.ToolTip = TTip(self.widg12, text = "Formatting: variable name (not editable)", time = tooltip_time)

        self.formatting_pre_array_syntax = StringVar()
        #self.widg13 = Entry( self.formatting_Frame, textvariable = self.formatting_pre_array_syntax, width = 2)
        self.widg13 = Text(self.formatting_Frame, width = 2, height = 1)
        self.widg13.pack( side = LEFT )
        self.widg13.insert(1.0, "{")
        self.widg13.ToolTip = TTip(self.widg13, text = "Formatting: Pre-array formatting", time = tooltip_time)

        self.widg14 = Label( self.formatting_Frame, text = "0x####" )
        self.widg14.pack( side = LEFT )
        self.widg14.ToolTip = TTip(self.widg14, text = "CRC Remainders are listed in hexadecimal format", time = tooltip_time)

        self.formatting_post_array_syntax = StringVar()
        #self.widg15 = Entry( self.formatting_Frame, textvariable = self.formatting_post_array_syntax, width = 2 )
        self.widg15 = Text(self.formatting_Frame, width = 2, height = 1)
        self.widg15.pack( side = LEFT )
        self.widg15.insert(1.0, "}")

        self.widg15.ToolTip = TTip(self.widg15, text = "Formatting: Post-array formatting", time = tooltip_time)

        self.formatting_after_syntax = StringVar()
        #self.widg16 = Entry( self.formatting_Frame, textvariable = self.formatting_after_syntax, width = 2 )
        self.widg16 = Text( self.formatting_Frame, width = 2, height = 1)
        self.widg16.pack( side = LEFT )
        self.widg16.insert(1.0, ";")
        self.widg16.ToolTip = TTip(self.widg16, text = "Formatting: After-array formatting", time = tooltip_time)

        self.widg17 = Button(self.master, text = "Calculate", command = self.calculate_button)
        #self.widg17.config( bd = 5 )
        self.widg17.grid( row = 6, column = 3, sticky = E )
        self.widg17.ToolTip = TTip(self.widg17, text = "3...2...1...Liftoff", time = tooltip_time)





    def browse_directory(self):

        self.output_dir = askdirectory(parent = self.master, title = "CRC Generator output path", initialdir = self.filepath)
        #print(self.output_dir)
        if type(self.output_dir) == str:
            if self.output_dir != "":
                self.widg8.config ( state = NORMAL )
                self.widg8.delete(0, END)
                self.widg8.insert(0, self.output_dir)
                self.widg8.xview( END )
                self.widg8.config( state = "readonly" )




            """
            f_picked = tkFileDialog.askopenfilename()
            test = type(f_picked)
            print (test)
            Results:
                <type 'unicode'> # Nothing selected, Cancel clicked
                <type 'tuple'> # File selected, Cancel clicked
                <type 'str'> # File selected, OK clicked
                <type 'tuple'> # Multiple files selected, OK clicked
            """

    def dropdown_selection(self):

        temp = self.crc_selection.get()                                        # Return Current Selection
        options = self.widg5['values']                                         # Return array of all possible selections

        ## Update the Adjacent Text Entry
        for element in options:
            ## If selection is a preset CRC value, then extract the CRC Value and write it to the textbox
            if temp == " ":
                self.widg6.config( state = NORMAL )                            # Convert text box to Enabled mode to update
                self.widg6.delete(1.0, END)                                      # Clear the text box
                self.widg6.insert(1.0, "0x####")                                 # Reset to default message
                self.widg6.config( state = DISABLED )                        # Reset textbox to read only
                self.widg6.config( bg = 'light gray' )
                break
            elif temp == "Manual":
                #print("manual")
                self.widg6.focus_set()
                self.widg6.config( state = NORMAL )                            # Convert Text Box to Enabled mode
                self.widg6.delete(1.0, END)                                      # Clear the text box
                self.widg6.insert(1.0, "0x")                                     # Number should be in hex form
                self.widg6.mark_set("insert", 'end')
                self.widg6.config( bg = "white")
                #print("Cursor: "  )
                #self.widg8.mark_set(END)
                break


            elif temp == element:
                ## Strip out the CRC string
                i = 0
                for letter in element:                                         # Check letter by letter
                    if i + 1 < len(element):                                   # Shy of the last element
                        if element[i] + element[i+1] == "0x":                  # Check for the hex "0x" signifier
                            self.crc = element[i:]                                  # Grab the String
                            self.crc = remove_Char(self.crc, " ")                        # Remove any spaces or empty space
                    i = i + 1
                self.widg6.config( state = NORMAL )                            # Text Box needs to be editable to be updated
                self.widg6.delete(1.0, END)                                      # Clear Text Box
                self.widg6.insert(1.0, str(self.crc))                                      # Write Anew to text box
                self.widg6.config( state = DISABLED)                          # Reset textbox to read only
                self.widg6.config( bg = 'light gray' )
                break


    def calculate_button(self):
        ## obtain inputs
        ## check inputs are correct
        ## invoke crc calculator
        ## print results to screen



        ## Obtain Inputs (if Entry Widgets)
        #data_length = self.data_length.get()
        #crc = self.crc_code.get()
        file_dir = self.file_dir.get()

        #variable_type = self.formatting_var_type.get()
        #pre_array_syntax = self.formatting_pre_array_syntax.get()
        #post_array_syntax = self.formatting_post_array_syntax.get()
        #after_array_syntax = self.formatting_after_syntax.get()

        ## Obtain Inputs (if Text Widgets)
        data_length = self.widg3.get(1.0, 'end')
        crc = self.widg6.get(1.0, 'end')
        #file_dir = self.widg8.get(1.0, 'end')


        variable_type = self.widg11.get(1.0, 'end')
        pre_array_syntax = self.widg13.get(1.0, 'end')
        post_array_syntax = self.widg15.get(1.0, 'end')
        after_array_syntax = self.widg16.get(1.0, 'end')

        ## Preprocess Inputs
        data_length = remove_Char( data_length, " ")
        crc = remove_Char( crc, " ")
        variable_type = remove_Char(variable_type, " ")
        pre_array_syntax = remove_Char( pre_array_syntax, " ")
        post_array_syntax = remove_Char( post_array_syntax, " ")
        after_array_syntax = remove_Char( after_array_syntax, " ")


        if debugging == True: print(file_dir)



        ## Check Inputs
        try:
            data_length = int(data_length, 10)
        except:
            self.error_notification = "Input Error: Improper User Entry in \"Data Length\" Data"
            self.userNotification(self.error_notification)
            return None

        try:
            crc = int(crc, 16)
        except:
            self.error_notification = "Input Error: Improper User Entry in \"CRC Code\""
            self.userNotification(self.error_notification)
            return None

        try:
            variable_type = str(variable_type)
        except:
            self.error_notification = "Input Error: Formatting option 1"
            self.userNotification(self.error_notification)
            return None

        try:
            pre_array_syntax = str(pre_array_syntax)
        except:
            self.error_notification = "Input Error: Formatting option \"Pre Array syntax\""
            self.userNotification(self.error_notification)

        try:
            post_array_syntax = str(post_array_syntax)
        except:
            self.error_notification = "Input Error: Formatting Option \"Post Array syntax\""
            self.userNotification(self.error_notification)
            return None

        try:
            after_array_syntax = str(after_array_syntax)
        except:
            self.error_notification = "Input Error: Formatting Option \"After Array syntax\""
            self.userNotification(self.error_notification)
            return None



        if debugging == True: print(self.Error)

        if self.Error == 0:
            crc_calculation = crc_FileWrite(current_dir = file_dir,
                                            data_length = data_length,
                                            crc_code = crc,
                                            variable_type = variable_type,
                                            pre_array_syntax = pre_array_syntax,
                                            post_array_syntax = post_array_syntax,
                                            after_array_syntax = after_array_syntax,
                                            log_name = self.log_name)
            crc_calculation.print_to_file()
            Error = crc_calculation.return_Error()

            if Error != 0:
                if Error == 0x01:
                    self.error_notification = "Folder Error: Problem with \"Output\" folder"
                if Error == 0x02:
                    self.error_notification = "File Error: Problem with output file"
                if Error == 0x04:
                    self.error_notification = "Folder Error: Problem with \"Log\" folder"
                if Error == 0x08:
                    self.error_notification = "File Error: Problem with log file"
                if Error == 0x10:
                    self.error_notification = "CRC Calculation Error"
                self.userNotification(self.error_notification)
                if debugging == True: print("Bottom CRC Ends")
                return None
        self.userNotification()




    def userNotification(self, error_text = "test"):
        if debugging == True: print("User Notifications: ")
        print(error_text)



























if __name__ == "__main__":
    debugging = True

    Root = Tk()


    test1 = Label(Root, text = "test")
    test1.pack()

    Frame_test = Frame(Root)
    Frame_test.pack()


    test = bottomCRC(Frame_test)

    Root.mainloop()






