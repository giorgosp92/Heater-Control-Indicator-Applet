import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


class ConfigWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Configuration")
        # self.set_size(400, 400)
        self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.entry = Gtk.Entry()
        # self.entry.set_text()
        vbox.pack_start(self.entry, True, True, 0)

        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox, True, True, 0)

        submit_button = Gtk.Button.new_with_label("Save Configuration")
        submit_button.connect("clicked", self.on_save_button_clicked)
        hbox.pack_start(submit_button, True, True, 0)

    def on_save_button_clicked(self, button):
        pass


