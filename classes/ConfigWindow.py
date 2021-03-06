import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk
import gi.repository.Notify as notify
import ConfigParser


PROJECT_PATH = "/home/giorgos/Projects/Iot-Controller-Applet/"


class ConfigWindow(Gtk.Window):
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file(PROJECT_PATH + "views/network_config_view.glade")
        builder.connect_signals(self)

        self.window = builder.get_object("network_config_window")
        self.entry_ip = builder.get_object("local_ip_address_field")
        self.entry_port = builder.get_object("local_port_field")

        config = ConfigParser.ConfigParser()
        config.read(PROJECT_PATH + "config.ini")
        if config.has_section("Network"):
            self.entry_ip.set_text(config.get("Network", "host"))
            self.entry_port.set_text(config.get("Network", "port"))

    def on_button_clicked(self, button):
        # Validate input
        if self.entry_ip.get_text() == "" and self.entry_port.get_text() == "":
            notify.Notification.new("IP Address and Port cannot be empty").show()
            return 0

        config = ConfigParser.RawConfigParser()

        config.add_section('Network')
        config.set("Network", "host", self.entry_ip.get_text())
        config.set("Network", "port", self.entry_port.get_text())

        with open(PROJECT_PATH + "config.ini", "wb") as configfile:
            config.write(configfile)
        self.window.destroy()
        notify.Notification.new("Network Configuration Saved").show()
