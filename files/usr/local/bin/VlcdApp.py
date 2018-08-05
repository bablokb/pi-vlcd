#!/usr/bin/python
# -----------------------------------------------------------------------------
# A simple kivy-app implementing a virtual LCD-screen with a row of buttons.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pi-vlcd
#
# -----------------------------------------------------------------------------

import subprocess

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock

 # --- main application class   ----------------------------------------------

class VlcdWidget(BoxLayout):
  lcd_display = ObjectProperty(None)

  def __init__(self):
    super(VlcdWidget, self).__init__(size=(800,480))

  def on_uptime(self,button):
    Clock.schedule_once(self.show_uptime,0)

  def on_df(self,button):
    Clock.schedule_once(self.show_df,0)

  def on_ip(self,button):
    Clock.schedule_once(self.show_ip,0)

  def show_uptime(self,_):
    hostname = subprocess.check_output("hostname",stderr=subprocess.STDOUT).split()
    uptime = subprocess.check_output("uptime",stderr=subprocess.STDOUT).split()
    ausgabe = """Hostname: %s
Uhrzeit:  %s
Uptime:   %s Tage, %s Stunden
Benutzer: %s
Last:     %s %s %s""" % (hostname[0],uptime[0],uptime[1],uptime[3],
                 uptime[5],uptime[8],uptime[9],uptime[10])
    self.lcd_display.text = ausgabe
    self.lcd_display.cursor = (0,0)

  def show_df(self,_):
    args = ["df","-h","--output=source,size,avail,pcent"]
    df = subprocess.check_output(args,stderr=subprocess.STDOUT)
    self.lcd_display.text = df

  def show_ip(self,_):
    args = ["ip","-o","addr","show","up"]
    ip = subprocess.check_output(args,stderr=subprocess.STDOUT).split('\n')
    text = "Network:"
    for line in ip:
      line = line.split()
      if line:
        text = "{0}\n{1} {2} {3} {4}".format(text,*line[:4])
    self.lcd_display.text = text

# --- main application class   ------------------------------------------------

class VlcdApp(App):
  """ application root class """

  def build(self):
    return VlcdWidget()

# --- main program   ----------------------------------------------------------

if __name__ == '__main__':
# Window.fullscreen = 'auto'
#  Window.size = (800,480)
  VlcdApp().run()
