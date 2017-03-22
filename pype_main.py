from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = "pype v0.0.1")
        self.grid = Gtk.Grid()
        self.add(self.grid)
        
        #Button
        # self.button = Gtk.Button(label = "Click here")
        # self.button.connect("clicked",self.buttonClicked)
        # self.add(self.button)
        self.box = Gtk.Box(spacing=10)
        self.add(self.box)
        self.bacon_button = Gtk.Button(label="Bacon")
        self.bacon_button.connect("clicked",self.buttonClicked)
        self.grid.add(self.bacon_button)
        self.tuna_button = Gtk.Button(label="Tuna")
        self.tuna_button.connect("clicked",self.buttonClicked)
        self.grid.attach(self.tuna_button,1,0,2,1)
       
    def buttonClicked(self, widget):
        print "Clicked "+widget.get_label()
    
# label = Gtk.Label()
# label.set_label("Hello")
# label.set_angle(30)
# label.set_halign(Gtk.Align.END)


window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
#window.add(label)
window.show_all()
Gtk.main()
