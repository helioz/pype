from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = "pype v0.0.1")

        #Button
        self.button = Gtk.Button(label = "Click here")
        self.button.connect("clicked",self.buttonClicked)
        self.add(self.button)
    def buttonClicked(self, widget):
        print "Clicked"
    

window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
