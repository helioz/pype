import gi
import Resources._globals as GLOBAL
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)
    def LaunchWindow(self, *args):
        args[0].show_all()

def loadHomeScreen():


    builder = Gtk.Builder()
    builder.add_from_file("lib/UXLib/ui.glade")
    
    builder.connect_signals(Handler())

    HomeScreen = builder.get_object("HomeScreen")
    AddContactScreen = builder.get_object("AddContactScreen")
    CallingScreen = builder.get_object("CallingScreen")
    IncomingCallScreen = builder.get_object("IncomingCallScreen")

    HomeScreen.set_title(GLOBAL.name+" "+GLOBAL.version_no)
    AddContactButton = builder.get_object("AddContact")
    ##AddContactScreen.show_all()
    

#    CallingScreen.show_all()


    HomeScreen.show_all()
    

#   IncomingCallScreen.show_all()


    Gtk.main()



