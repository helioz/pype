import gi
import Resources._globals as GLOBAL
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import lib.DataStructures.common as common

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)


        

class UI():
    def __init__(self, core):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("lib/UXLib/ui.glade")
        self.pype = core
        
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
        self.numOfContacts = 1
        
        self.contactCBox = self.builder.get_object("contactsCBox")
        self.contactStore = Gtk.ListStore(str)
        self.contactCell = Gtk.CellRendererText()
        self.contactCBox.pack_start(self.contactCell, 0)
        self.contactCBox.add_attribute(self.contactCell, 'text', 0)
        self.contactCBox.set_model(self.contactStore)
        self.contactCBox.connect('changed', self.on_chaned)
        self.fillContactCBox()
        
        self.dialogOK = self.builder.get_object("button2")
        self.dialogOK.connect("clicked",self.CloseErrorWindow)
        self.genNewKeys = self.builder.get_object("GenNewKeys")
        self.genNewKeys.connect("clicked", self.GenNewKeys)
        #common.fillContactCBox(self.contactCBox, self.cell)


        self.loadKeyCB = self.builder.get_object("loadKeyCB")
        self.loadKeyStore = Gtk.ListStore(str)
        self.loadKeyCell = Gtk.CellRendererText()
        self.loadKeyCB.pack_start(self.loadKeyCell, 0)
        self.loadKeyCB.add_attribute(self.loadKeyCell, 'text', 0)
        self.loadKeyCB.set_model(self.loadKeyStore)
        self.loadKeyCB.connect("changed", self.setKeyCBHandler)
        self.fillkeyCB()

        self.HomeScreen.set_title(GLOBAL.name+" "+GLOBAL.version_no)
        
        #AddContactScreen.show_all()
        #CallingScreen.show_all()
        #IncomingCallScreen.show_all()
        self.HomeScreen.show_all()
        Gtk.main()
        
        #self.pype.runPype()

    def fillContactCBox(self):
        contacts = common.loadContacts()
        
        for contact in contacts:
            if contact.name == "none":
                continue
            self.contactStore.insert(self.numOfContacts, [contact.name])
            self.numOfContacts = self.numOfContacts + 1
        self.contactCBox.set_active(0)
        
    def on_chaned(self, widget):
        return

        
    def GenNewKeys(self, button):
        if self.pype.crypto.generateNewKeys():
            self.ShowMessage("Pype","Key pair generated successfully")
            self.numKeys = self.numKeys + 1
            self.loadKeyStore.append(["Key Pair "+str(self.numKeys)])
            #self.loadKeyCB.destroy()
            #self.HomeScreen.hide()
            #self.HomeScreen.show_all()
        else:
            self.ShowMessage("Pype","Key generation failed")


    def fillkeyCB(self):
        self.numKeys = 0
        for key in self.pype.crypto.key_ring:
            #self.key_store.append(["key pair "+str(i)])
            self.numKeys = self.numKeys + 1
            self.loadKeyStore.insert(self.numKeys - 1,["Key Pair "+str(self.numKeys)])
        self.loadKeyCB.set_active(0)
        #self.loadKeyCB.set_entry_text_column(1)

    def setKeyCBHandler(self, box):
        #print self.loadKeyCB.get_active()
        keyIndex = int(self.loadKeyCB.get_active())
        self.pype.crypto.setCurKey(keyIndex)
            
    def CloseErrorWindow(self, button):
        self.ErrorWindow.hide()

    def AddContactToList(self, button):
        c = common.Contact(self.nameEntry.get_text(), self.pubKeyeEntry.get_text(), self.pubKeynEntry.get_text() )
        self.AddContactScreen.hide()
        self.contactStore.append([c.name])
        self.numOfContacts = self.numOfContacts + 1
        self.ShowMessage("Success","Contact successfully added")
        common.saveContact(c)
        

        return

    def ShowMessage(self, WindowTitle, message):
        self.ErrorWindow.set_title(WindowTitle)
        self.errorMessage.set_label(message)
        self.ErrorWindow.show_all()

    def LaunchWindow(self, button, window):
        window.show_all()

