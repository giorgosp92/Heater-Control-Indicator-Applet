#!/usr/bin/env python3

import os
import signal
import gi
import ConfigParser
import yaml
import socket

from classes.ConfigWindow import ConfigWindow

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

import gi.repository.Gtk as gtk
import gi.repository.AppIndicator3 as appindicator
import gi.repository.Notify as notify

APPINDICATOR_ID = 'heater_control_indicator'

# some global variables
networkHost = 0
networkPort = 0
networkLocalHost = 0
networkLocalPort = 0
# Colors
colors = {}


def init():
    global colors
    with open("colors.yml", 'r') as ymlfile:
        colors = yaml.load(ymlfile)


def main():
    init()
    get_config()
    indicator = appindicator.Indicator.new(APPINDICATOR_ID,
                                           os.path.abspath("resources/icon.png"),
                                           appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()


def get_config(args = None):
    global networkHost
    global networkPort
    global networkLocalHost
    global networkLocalPort
    config = ConfigParser.ConfigParser();
    config.read("config.ini")
    if config.has_section("Network"):
        networkHost = config.get("Network", "host")
        networkPort = config.get("Network", "port")
        networkLocalHost = config.get("Network", "localHost")
        networkLocalPort = config.get("Network", "localPort")
        print "Read Settings: %s:%s" % (networkHost, networkPort)
    else:
        set_config()


def set_config(args = None):
    config = ConfigParser.ConfigParser();
    config.read("config.ini")
    configWindow = ConfigWindow()
    # Grab destroy event in this class to trigger get config and replace configuration
    configWindow.window.connect("destroy", get_config)
    configWindow.window.show_all()



def changeColor(e, colorCode):
    global colors
    changeTo = colors[colorCode]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    s.connect((networkHost, int(networkPort)))
    s.send(changeTo)
    s.close()


def build_menu():
    menu = gtk.Menu()

    control_menu = gtk.Menu()

    item_controlmenu_red = gtk.MenuItem("Red")
    item_controlmenu_Green = gtk.MenuItem("Green")
    item_controlmenu_Blue = gtk.MenuItem("Blue")
    item_controlmenu_Cyan = gtk.MenuItem("Cyan")
    item_controlmenu_Pink = gtk.MenuItem("Pink")
    item_controlmenu_Purple = gtk.MenuItem("Purple")
    item_controlmenu_Orange = gtk.MenuItem("Orange")
    item_controlmenu_White = gtk.MenuItem("White")
    item_controlmenu_Black = gtk.MenuItem("Black")

    item_controlmenu_red.connect('activate', changeColor, "Red")
    item_controlmenu_Green.connect('activate', changeColor, "Green")
    item_controlmenu_Blue.connect('activate', changeColor, "Blue")
    item_controlmenu_Cyan.connect('activate', changeColor, "Cyan")
    item_controlmenu_Pink.connect('activate', changeColor, "Pink")
    item_controlmenu_Purple.connect('activate', changeColor, "Purple")
    item_controlmenu_Orange.connect('activate', changeColor, "Orange")
    item_controlmenu_White.connect('activate', changeColor, "White")
    item_controlmenu_Black.connect('activate', changeColor, "Black")

    control_menu.append(item_controlmenu_red)
    control_menu.append(item_controlmenu_Green)
    control_menu.append(item_controlmenu_Blue)
    control_menu.append(item_controlmenu_Cyan)
    control_menu.append(item_controlmenu_Pink)
    control_menu.append(item_controlmenu_Purple)
    control_menu.append(item_controlmenu_Orange)
    control_menu.append(item_controlmenu_White)
    control_menu.append(item_controlmenu_Black)

    item_control = gtk.MenuItem("Change color to")
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
