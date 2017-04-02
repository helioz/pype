import gi
import Resources._globals as GLOBAL
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import lib.DataStructures.Structures as dataS

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)


        

class UI():
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("lib/UXLib/ui.glade")
    
        self.builder.connect_signals(Handler())

        self.HomeScreen = self.builder.get_object("HomeScreen")
        self.AddContactScreen = self.builder.get_object("AddContactScreen")
        self.CallingScreen = self.builder.get_object("CallingScreen")
        self.IncomingCallScreen = self.builder.get_object("IncomingCallScreen")
        self.ErrorWindow = self.builder.get_object("ErrorWindow")



        self.errorMessage = self.builder.get_object("errorLabel")
        self.AddContactButton = self.builder.get_object("addContact")
        self.pubKeyeEntry = self.builder.get_object("pubKeyeEntry")
        self.pubKeynEntry = self.builder.get_object("pubKeynEntry")
        self.nameEntry = self.builder.get_object("nameEntry")
        self.AddContactButton.connect("clicked", self.AddContactToList)
        self.AddContactWindowLaunchButton = self.builder.get_object("AddContact")
        self.AddContactWindowLaunchButton.connect("clicked", self.LaunchWindow, self.AddContactScreen)
        self.dialogOK = self.builder.get_object("button2")
        self.dialogOK.connect("clicked",self.CloseErrorWindow)


        self.HomeScreen.set_title(GLOBAL.name+" "+GLOBAL.version_no)
       
        #AddContactScreen.show_all()
        #CallingScreen.show_all()
        #IncomingCallScreen.show_all()
        self.HomeScreen.show_all()
        Gtk.main()

    def CloseErrorWindow(self, button):
        self.ErrorWindow.hide()

    def AddContactToList(self, button):
        c = dataS.Contact(self.nameEntry.get_text(), self.pubKeyeEntry.get_text(), self.pubKeynEntry.get_text() )
        self.AddContactScreen.hide()
        self.ShowMessage("Success","Contact successfully added")

        return

    def ShowMessage(self, WindowTitle, message):
        self.ErrorWindow.set_title(WindowTitle)
        self.errorMessage.set_label(message)
        self.ErrorWindow.show_all()

    def LaunchWindow(self, button, window):
        window.show_all()
