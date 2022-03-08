# -*- coding: utf-8 -*-
from crc_top import *
from crc_bottom import *
from CRC_gui import *
from tkinter import *
import tkinter.ttk as ttk
from datetime import datetime
from ToolTip.ToolTip import ToolTip as TTip

from PopupMenu.PopupMenu import PopupMenu as Popup

from tkinter.filedialog import *
import os

debugging = False


logFile = "log.txt"
outputFile1 = "crc_codeword_bytes.txt"
outputFile2 = "crc_remainder_whole.txt"


class crc_TopBottom(crc_GUI, Frame):

    def __init__(self, parent = None, Root = None):
        self.TopBottom_Frame = Frame.__init__(self, parent)                                           # Creates a master Frame if one does not already exist
        self.parent = parent
        self.root = Root


        crc_GUI.__init__(self, self.master, Root)

        self.bottom_NotificationBar()

        ## Create Error Log File
        log_name = self.createFiles()

        ## Create and pack top CRC GUI, the one at a time one
        self.topCRC_Frame = Frame(self.TopBottom_Frame)                                      # Creates a sub-frame
        self.topCRC_Frame.pack(expand = YES, fill = X)                                                    # Packs the sub-frame in the master frame
        self.topCRC_chunk = topCRC(self.topCRC_Frame, log_name = log_name)                                    # Gives the sub-frame to the parent-Class
        self.topCRC_chunk.userNotification = self.userNotification

        ## Create and pack bottom CRC Gui, the save to file one
        self.bottomCRC_Frame = Frame(self.TopBottom_Frame)
        self.bottomCRC_Frame.pack(expand = YES, fill = X)
        self.bottomCRC_chunk = bottomCRC(self.bottomCRC_Frame, log_name = log_name)
        self.bottomCRC_chunk.userNotification = self.userNotification

        ## Pack notification bar under the Top and Bottom CRC Gui
        self.pack_bottom_NotificationBar() #Pack after the Top and Bottom CRC chunks, but before the crcCodes are updated

        ## Up
        self.crcCodes_update()  #this needs to occur after the topCRC_chunk and bottomCRC_chunk are initialized

        self.root.resizable(False, False)

        ## Trying to get a popup Menu Working
        self.PopupMenu()     #Initiate Popup Menu
        self.give_Popup()    #Bind it to the desired widgets


    def createFiles(self):

        ## Create Appropriate Log Folder
        try:
            self.current_dir = os.getcwd()
            if ( os.path.exists(self.current_dir + os.sep + "log") == False ):              # Make an error and log output directory
                os.mkdir(self.current_dir + os.sep + "log")
        except:
            self.userNotification("Folder Error: Problem with \"Log\" folder")

        ## Create appropriate log file name (absolute referencing)
        self.current_dir = os.getcwd()
        log = logFile
        date_time = datetime.now()                                             # Obtain Current Date and Time
        timestamp = date_time.strftime("%G %b %d %I-%M%p")
        log = self.current_dir + os.sep +  "log" + os.sep + timestamp + log


        ## Create Log File
        try:
            file = open(log, 'w')                                        # Opening or creating log file
        except:
            self.userNotification("File Error: Problem with log file")
            #print("Log file failed to open")                                   # If log file fails to create

        ## Preamble Text when file is first created
        date_time = datetime.now()                                             # Obtain Current Date and Time
        file.write( date_time.strftime("%G %b %d %I:%M%p") + " " + "log.txt" )
        file.write("\n")
        file.write( "CRC begins" )
        file.write("\n")
        file.close()

        return log                                                             # Return Absolute File Location




    def userNotification(self, inputs = "Operation Complete"):

        ## Get current time
        date_time = datetime.now()                                             # Obtain Current Date and Time
        log = date_time.strftime("%G %b %d %I_%M%p") + " "                     # Something that shows the Time, Edit Required

        inputs_temp = inputs.split(":")
        if debugging == True: print(inputs_temp)

        ## Change Colour indicator
        if inputs_temp[0] == "Input Error":
            self.bottomBar_Frame.widg2.config( bg = "yellow" )
        else:
            self.bottomBar_Frame.widg2.config( bg = "red" )

        if inputs_temp[0] == "Operation Complete":
            self.bottomBar_Frame.widg2.config( bg = 'green' )

        inputs = date_time.strftime("%I:%M%p ") + inputs

        ## Write Text to Screen
        self.bottomBar_Frame.widg1.config( state = NORMAL )
        self.bottomBar_Frame.widg1.delete(0, END)
        self.bottomBar_Frame.widg1.insert(0, inputs)
        self.bottomBar_Frame.widg1.config( state = "readonly" )




        ## Update Error and Log Directory
        try:
            self.current_dir = os.getcwd()
            if ( os.path.exists(self.current_dir + os.sep + "log") == False ):              # Make an error and log output directory
                os.mkdir(self.current_dir + os.sep + "log")
        except:
            inputs = "Folder Error: Problem with \"Output\" folder"
            inputs = date_time.strftime("%I_%M%p") + inputs

        log = date_time.strftime("%G %b %d %I%p") + " " + "log.txt"
        log = self.current_dir + os.sep + "log" + os.sep + log

        try:
            file = open(log, 'a')
            file.write(inputs)
            file.close()
        except:
            return None




    def saveto_menu(self):

        ## Find or Create Directory
        current_dir = os.getcwd()
        if ( os.path.exists( current_dir + os.sep + "output" ) == False ):
            os.mkdir( current_dir + os.sep + "output" )
        self.filepath = current_dir + os.sep + "output" + os.sep

        ## Update Output Folder selection
        self.output_dir = askdirectory(parent = self.master, title = "CRC Generator output path", initialdir = self.filepath)
        if type(self.output_dir) == str:
            if self.output_dir != "":
                self.bottomCRC_chunk.widg8.config ( state = NORMAL )
                self.bottomCRC_chunk.widg8.delete(0, END)
                self.bottomCRC_chunk.widg8.insert(0, self.output_dir)
                self.bottomCRC_chunk.widg8.xview( END )
                self.bottomCRC_chunk.widg8.config( state = DISABLED )

    def crcCodes_update(self):

        ## Try to open file that CRC codes are read from
        try:
            location = os.getcwd() + os.sep + "SupportFiles" + os.sep + "crc_codes.txt"
            file = open(location, 'r')                                  # Read CRC codes from Text file
        except:
           self.userNotifications("No CRC Codes text file")

        ## Read text file
        options = file.readlines()


        title = []
        code = []
        ## Separate the CRC code name from the code itself, then remove string formatting
        for option in options:

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

        crc_options = []

        temp_length = len(title)

        ## Formatted CRC codes
        for i in range(temp_length):
            crc_options.append(title[i] + ": " + code[i])

        ## Reset default selection to empty selection
        crc_options.insert(0, " ")
        temp_length = len(crc_options)
        crc_options.insert(temp_length, "Manual")

        ## Update CRC Options in Widgets
        self.topCRC_chunk.widg7["values"] = crc_options
        self.bottomCRC_chunk.widg5["values"] = crc_options



    def crc_codes_menu(self, i, title, code):

        self.topCRC_chunk.widg7.current(i+1)                                   # Unclear, I think this is due to the empty entry taking up the 0th spot
        self.bottomCRC_chunk.widg5.current(i+1)

        ## Check if option changes text box behavior
        temp = title[i] + ": " + code[i]
        options = self.topCRC_chunk.widg7['values']                            # Return array of all possible selections

        ## Update the Adjacent Text Entry
        crc = ''
        for element in options:

             ## If selection is Manual, then enable textbox to be edited
            if temp == "Manual":                                               # Did user select "manual" input mode?
                self.topCRC_chunk.widg8.config( state = NORMAL )               # Convert Text Box to Enabled mode
                self.topCRC_chunk.widg8.delete(1.0, 'end')                     # Clear the text box
                self.topCRC_chunk.widg8.insert(1.0, "0x")                      # Number should be in hex form
                self.topCRC_chunk.widg8.mark_set("insert", "end")

                self.bottomCRC_chunk.widg6.config( state = NORMAL )            # Convet Text Box to Enabled mode
                self.bottomCRC_chunk.widg6.delete(1.0, 'end')                  # Clear the text box
                self.bottomCRC_chunk.widg6.insert(1.0, "0x")                   # Number should be in hex form
                self.bottomCRC_chunk.widg6.mark_set("insert", "end")

            ## If selection is the blank option, reset the textbox
            elif temp == " ":                                                  # Blank option?
                self.topCRC_chunk.widg8.config( state = NORMAL )               # Convert text box to Enabled mode to update
                self.topCRC_chunk.widg8.delete(1.0, 'end')                     # Clear the text box
                self.topCRC_chunk.widg8.insert(1.0, "0x####")                  # Reset to default message
                self.topCRC_chunk.widg8.config( state = DISABLED )             # Reset textbox to read only
                self.topCRC_chunk.widg8.config( bg = 'light gray' )

                self.bottomCRC_chunk.widg6.config( state = NORMAL )            # Convert text box to Enabled mode to update
                self.bottomCRC_chunk.widg6.delete( 1.0, END )                  # Clear the text box
                self.bottomCRC_chunk.widg6.insert( 1.0, "0x####" )             # Reset to default message
                self.bottomCRC_chunk.widg6.config( state = DISABLED )          # Reset textbox to read only
                self.bottomCRC_chunk.widg6.config( bg = "light gray" )



            ## If selection is a preset CRC value, then extract the CRC Value and write it to the textbox
            if temp == element:
                ## Strip out the CRC string
                i = 0
                for letter in element:                                         # Check letter by letter
                    if i + 1 < len(element):                                   # Shy of the last element
                        if element[i] + element[i+1] == "0x":                  # Check for the hex "0x" signifier
                            crc = element[i:]                                  # Grab the String
                            crc = remove_Char(crc, " ")                        # Remove any spaces or empty space
                            break
                    i = i + 1
                self.topCRC_chunk.widg8.config( state = NORMAL )               # Text Box needs to be editable to be updated
                self.topCRC_chunk.widg8.delete(1.0, 'end')                     # Clear Text Box
                self.topCRC_chunk.widg8.insert(1.0, crc)                       # Write Anew to text box
                self.topCRC_chunk.widg8.config( state = DISABLED)              # Reset textbox to read only
                self.topCRC_chunk.widg8.config( bg = 'light gray' )

                self.bottomCRC_chunk.widg6.config( state = NORMAL )            # Text Box needs to be editable to be updated
                self.bottomCRC_chunk.widg6.delete(1.0, END)                    # Clear Text Box
                self.bottomCRC_chunk.widg6.insert(1.0, crc)                    # Write Anew to text box
                self.bottomCRC_chunk.widg6.config( state = DISABLED )          # Reset textbox to read only
                self.bottomCRC_chunk.widg6.config( bg = 'light gray')


    def formatting_output_menu(self, index, title, formatting):


        ## Extract out the formatting
        formatting = formatting.strip()                                        # Remove Whitespace on either end
        formatting_array = formatting.split(",")

        ## Format the pre-array variable type formatting
        self.bottomCRC_chunk.widg11.config( state = NORMAL)
        self.bottomCRC_chunk.widg11.delete(1.0, 'end')
        self.bottomCRC_chunk.widg11.insert(1.0, formatting_array[0] )

        ## Format the pre-array syntax
        self.bottomCRC_chunk.widg13.config( state = NORMAL)
        self.bottomCRC_chunk.widg13.delete(1.0, 'end')
        self.bottomCRC_chunk.widg13.insert(1.0, formatting_array[1] )

        ## Format the post-array syntax
        self.bottomCRC_chunk.widg15.config( state = NORMAL)
        self.bottomCRC_chunk.widg15.delete(1.0, 'end')
        self.bottomCRC_chunk.widg15.insert(1.0, formatting_array[2] )

        ## Format the after array syntax
        self.bottomCRC_chunk.widg16.config( state = NORMAL)
        self.bottomCRC_chunk.widg16.delete(1.0, 'end')
        self.bottomCRC_chunk.widg16.insert(1.0, formatting_array[3] )

    def helpMenu_CRC(self):
        os.startfile("SupportFiles" + os.sep + "CRC_PDF.pdf")                  # Start Whitepaper

    def helpMenu_Help(self):
        os.startfile("SupportFiles" + os.sep + "Help.pdf")                     # Start Help file

    def about(self, event = None):

        if debugging == True: print( "About Popup Information" )

        ## Obtain Parent window handle
        parentName = self.master.winfo_parent()
        parent     = self.master._nametowidget(parentName)                 # event.widget is your widget

        text = "Chad Unterschultz \nBsc in Electrical Engineering\nMeng in Control Systems"

        ## Create window dependent on parent window
        self.about_window = Toplevel(parent)
        self.about_window.focus_set()
        self.about_window.title("About the author")
        self.about_window.widg1 = Label(self.about_window, text = text)
        self.about_window.widg1.grid(row = 0, column = 0, sticky = W)
        self.about_window.widg2 = Button(self.about_window, text = "Okay", command = self.about_window.destroy)
        self.about_window.widg2.grid(row = 1, column = 0, sticky = E)
        self.about_window.resizable(False, False)
        self.about_window.update()

        ## Parent window location, top left corner
        gui_x_location = parent.winfo_rootx()
        gui_y_location = parent.winfo_rooty()

        if debugging == True: print("gui Location: ", gui_x_location, gui_y_location)

        ## Parent window dimensions
        gui_height = parent.winfo_height()
        gui_width =  parent.winfo_width()

        if debugging == True: print("gui size: ", gui_height, gui_width)

        ## Dependent window dimensions
        popup_height = self.about_window.winfo_height()
        popup_width  = self.about_window.winfo_width()

        if debugging == True: print("popup size: ", popup_height, popup_width)

        ## Place dependent window in center of parent window, find the buffer space
        Top_space = (gui_height - popup_height) / 2                            # Space above and below widget
        Top_space = int(Top_space)                                             # Round down
        Side_space = (gui_width - popup_width) / 2                             # Space to either side of widget
        Side_space = int(Side_space)                                           # Round down

        if debugging == True: print("Space: ", Top_space, Side_space)

        ## Place dependent window in center of parent window, factor in buffer space
        new_x = gui_x_location + Side_space
        new_y = gui_y_location + Top_space                                     # This Doesn't seem to be perfectly centered on the window
                                                                               # Horizontally centered, but not vertically
        self.about_window.wm_geometry("+%d+%d" % (new_x, new_y))
        self.about_window.update()                                             # Force GUI program to update

        if debugging == True: print("Location: ", new_x, new_y)

    def bottom_NotificationBar(self) :

        ## A frame for the bottom notifications bar
        self.bottomBar_Frame = Frame(self.TopBottom_Frame)

        ## Text widget
        self.bottomBar_Frame.string = StringVar()
        self.bottomBar_Frame.widg1 = Entry( self.bottomBar_Frame, textvariable = self.bottomBar_Frame.string )
        self.bottomBar_Frame.widg1.pack( side = LEFT, expand = YES, fill = 'x', anchor = W )
        self.bottomBar_Frame.widg1.ToolTip = TTip(self.bottomBar_Frame.widg1, text = "Displays Error Messages, and tells you when an operation is complete", time = 15000)

        ## Button widget acting as a colour notification
        self.bottomBar_Frame.widg2 = Button( self.bottomBar_Frame,  width = 2, height = 1, bd = 0, pady = 0) #bg = 'red',
        self.bottomBar_Frame.widg2.config( state = DISABLED )
        self.bottomBar_Frame.widg2.pack( side = RIGHT )
        self.bottomBar_Frame.widg2.ToolTop = TTip(self.bottomBar_Frame.widg2, text = "Red = Error\nYellow = Entry Missing\nGreen = Good\nGray = Nothing has happened yet", time = 15000)


    def pack_bottom_NotificationBar(self):
        ## Make sure to pack last
        self.bottomBar_Frame.pack(expand = YES, fill = 'x')


    def PopupMenu(self, event = None):

        ## Popup Menu options
        self.Menu = Menu(self.master, tearoff = 0)
        self.Menu.add_command(label  = "Cut",   command = self.popupCut )
        self.Menu.add_command(label  = "Copy",  command = self.popupCopy)
        self.Menu.add_command(label  = "Clear", command = self.popupClear )
        self.Menu.add_command(label  = "Paste", command = self.popupPaste )




    def PopupMenu_feature(self, Widget, event = None):
        ## When right click, popup menu appears
        Widget.bind("<Button-3>", self.showMenu, add = "+")

    def showMenu(self, event = None):
        ## Menu 'posts' to the screen at the x-y location of the button click
        self.Menu.post(event.x_root, event.y_root)


    def give_Popup(self):

        ## Give all widgets in the top frame a copy/paste popup window
        for widget in self.topCRC_Frame.winfo_children():                      # List of all widgets in frame
            if isinstance(widget, Entry) | isinstance(widget, Text):           # Check if any widgets are Entry or Text
                self.PopupMenu_feature(widget)                                 # Give popup features to Entry or Text widgets

        ## Give all widgets in the Bottom frame a copy/paste popup window
        for widget in self.bottomCRC_Frame.winfo_children():                   # List of all widgets in frame
            if isinstance(widget, Entry) | isinstance(widget, Text):           # Check if any widgets are Entry or Text
                self.PopupMenu_feature(widget)                                 # Give popup features to Entry or Text Widgets

        ## Give all widgets in bottom notification bar a copy/paste popup window
        for widget in self.bottomBar_Frame.winfo_children():                   # List all widgets in frame
            if isinstance(widget, Entry) | isinstance(widget, Text):           # Check if any widgets are Entry or Text
                self.PopupMenu_feature(widget)                                 # Give popup features to Entry or Text widgets



    def popupClear(self):

        ## Gets the handle for the currently selected widget
        widget = self.master.focus_get() #Current Widget of interest
        text = "Empty"


        ## Cannot Clear an Entry widget, read only
        if isinstance(widget, Entry):                                          #entry type widget
            self.master.bell
            self.userNotification("Cannot Clear")

        ## Clear Text widget
        if isinstance(widget, Text):                                           # Test if widget is a Text widget
            state = widget.cget('state')                                       # Save current widget state
            widget.config( state = NORMAL )                                    # Convert state to NORMAL, so that the widget can be interacted with
            index = widget.delete(1.0, 'end')                                  # Delete all widget contents
            widget.config( state = state )                                     # Return widget to its prior state

        if debugging == True: print("Clear complete")

    def popupPaste(self):

        ## Obtain handle to the Entry of Text widget currently selected
        widget = self.master.focus_get() #Current Widget of interest
        text = "Empty"

        ## Cannot Paste to an Entry widget as those are readonly
        if isinstance(widget, Entry):                                          # Check if Entry type widget
            self.master.bell
            self.userNotification("Cannot Paste")

        ## Paste to a Text widget
        if isinstance(widget, Text):                                           # Check if Text type widget
            state = widget.cget('state')                                       # Get current  state, hold for later
            widget.config( state = NORMAL )                                    # Convert to NORMAL mode so that we know it is editable
            index = widget.index(INSERT)                                       # Looks for current cursor location
            if debugging == True: print("index", index)
            text = self.selection_get(selection = 'CLIPBOARD')                 # Gets text from Clipboard
            widget.insert(index, text)                                         # Insert text from clipboard to cursor location
            widget.config( state = state )                                     # Return widget to the state it was before we touched it



        print("Paste complete")
        print("Text: ", text)

    def popupCopy(self):

        ## Obtain handle to the Entry of Text widget currently selected
        widget = self.master.focus_get() #Current Widget of interest
        text = "Empty"

        ## Copy from Entry widget means to copy everything
        if isinstance(widget, Entry):                                          # Check if entry type widget
            state = widget.cget('state')                                       # Get Current Widget  State
            widget.config( state = NORMAL )                                    # Make widget NORMAL so that it can be interacted with
            text = widget.get()                                                # Get all of the current text
            widget.config( state = state )                                     # Restore State to the way it was before
            self.clipboard_clear()                                             # Clear Clipboard to copy to it
            self.clipboard_append(text)                                        # Append to empty clipboard, equivalent to a copy

        if isinstance(widget, Text):                                           # Check if Text type widget
            state = widget.cget('state')                                       # Get current Widget State
            widget.config( state = NORMAL )                                    # Make widget NORMAL so that it can be interacted with

            ## Check if text is selected
            inrange = widget.tag_ranges("sel")                                 # Check if Text is selected
            if inrange == True:                                                # Text Selected
                text = widget.get('sel.first', 'sel.last')                     # Get the selected text

            else:                                                              # Text not selected
                self.userNotification("No Text Selected")

            widget.config( state = state )                                     # Return widget state to the way is was before

            ## Copy text to the clipboard
            self.clipboard_clear()                                             # Clear clipboard to copy to it
            self.clipboard_append(text)                                        # Append to the empty clipboard


        if debugging == True: print("copy complete")
        if debugging == True: print("Text: ", text)
        pass



    def popupCut(self):

        ## Obtain handle to the Entry or Text widget currently selected
        widget = self.master.focus_get() #Current Widget of interest
        text = "Empty"

        ## Cannot Cut from Entry widget, editing disabled
        if isinstance(widget, Entry):                                          # Check if widget is an "Entry" type
            self.master.bell
            self.userNotification("Cannot Cut")

        ## Cut from Text widget
        if isinstance(widget, Text):                                           # Check if widget is a "Text" type
            state = widget.cget('state')                                       # Obtain current state of widget, NORMAL or DISABLED
            widget.config( state = NORMAL )                                    # Change widget to NORMAL so that it can be edited
            inrange = widget.tag_ranges("sel")                                 # Check the Current Widget Highlighting
            if inrange == True:                                                # If something is highlighted, then true
                text = widget.get('sel.first', 'sel.last')                     # Copy what is highlighted
                widget.delete('sel.first', 'sel.last')                         # Delete what is highlighted (effectively a cut)
            else:                                                              # Nothing is highlighted
                self.userNotification("No Text Selected")                      # Inform the user that nothing was highlighted
            widget.config( state = state )                                     # Restore state back to normal

            self.clipboard_clear()                                             # Ensure Clipboard is empty before copying to it
            self.clipboard_append(text)                                        # Append to an empty clipboard

        if debugging == True: print("cut complete")                            # To help aid debugging
        if debugging == True: print("Text: ", text)













if __name__ == "__main__":
    debugging = True


    Root = Tk()

    test_Frame = Frame(Root)
    test_Frame.pack()

    test = crc_TopBottom(test_Frame, Root = Root)

    Root.mainloop()



