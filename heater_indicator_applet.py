#!/usr/bin/env python3

import os
import signal
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

import gi.repository.Gtk as gtk
import gi.repository.AppIndicator3 as appindicator
import gi.repository.Notify as notify

APPINDICATOR_ID = 'heater_control_indicator'


def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath("/home/george/Downloads/heater_icon.png"),
                                           appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()


def set_config(_):
    notify.Notification.new("<b>Configuration unavailable</b>").show()
    pass


def turn_on(_):
    notify.Notification.new("<b>Heater Control</b><br>Turning heater on....").show()
    pass


def turn_off(_):
    notify.Notification.new("<b>Heater Control</b><br>Turning heater off....").show()
    pass


def build_menu():
    menu = gtk.Menu()

    control_menu = gtk.Menu()
    item_controlmenu_on = gtk.MenuItem("Turn ON")
    item_controlmenu_off = gtk.MenuItem("Turn OFF")
    item_controlmenu_on.connect('activate', turn_on)
    item_controlmenu_off.connect('activate', turn_off)
    control_menu.append(item_controlmenu_on)
    control_menu.append(item_controlmenu_off)

    item_control = gtk.MenuItem("Control")
    item_control.set_submenu(control_menu)
    menu.append(item_control)
    item_config = gtk.MenuItem("Configuration")
    item_config.connect('activate', set_config)
    menu.append(item_config)
    item_quit = gtk.MenuItem("Exit")
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu


def quit(_):
    notify.uninit()
    gtk.main_quit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
