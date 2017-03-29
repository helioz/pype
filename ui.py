import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)




builder = Gtk.Builder()
builder.add_from_file("lib/UXLib/ui.glade")

builder.connect_signals(Handler())

AddContactScreen = builder.get_object("AddContactScreen")
AddContactScreen.show_all()

CallingScreen = builder.get_object("CallingScreen")
CallingScreen.show_all()

HomeScreen = builder.get_object("HomeScreen")
HomeScreen.show_all()

IncomingCallScreen = builder.get_object("IncomingCallScreen")
IncomingCallScreen.show_all()


Gtk.main()



