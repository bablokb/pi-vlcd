#!/usr/bin/python
# -----------------------------------------------------------------------------
# A simple WxApp implementing a virtual LCD-screen with a row of buttons.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pi-vlcd
#
# -----------------------------------------------------------------------------

import threading, subprocess, re
import wx

# --- helper class for asynchronous events   ----------------------------------

SYSCMD_EVENT_TYPE = wx.NewEventType()
EVT_SYSCMD = wx.PyEventBinder(SYSCMD_EVENT_TYPE,1)

class SysCmdFinishEvent(wx.PyCommandEvent):
  """ wrap result of a system-command into an event """

  def __init__(self,ev_id,value=None):
    wx.PyCommandEvent.__init__(self,SYSCMD_EVENT_TYPE,ev_id)
    self._value = value

  def get_output(self):
    return self._value

# --- main application frame   ------------------------------------------------

class AppFrame(wx.Frame):
  """ Application toplevel frame """

  # --- Constructor   ---------------------------------------------------------
  
  def __init__(self, parent, title):
    wx.Frame.__init__(self, parent, -1, title,size=(800, 480))

    #self.SetMenuBar(self.create_menu())
    #self.CreateStatusBar()
    self.create_controls()
    self.Bind(EVT_SYSCMD, self.on_syscmd_result)
    self.on_uptime(None)

  # --- create the panel with all controls   ----------------------------------

  def create_controls(self):
    """ create panel with all controls """

    #vpanel = wx.Panel(self)
    vpanel = self
    vbox = wx.BoxSizer(wx.VERTICAL)
    vbox.Add(self.create_outputarea(vpanel),1, wx.ALL|wx.EXPAND,10)
    vbox.Add(self.create_buttons(vpanel),0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL,10)
    vpanel.SetSizer(vbox)
    #vpanel.Layout()

  # --- create the application menu   -----------------------------------------

  def create_menu(self):
    """ create File-menu with single entry 'exit' """

    menu = wx.Menu()
    menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Exit")
    self.Bind(wx.EVT_MENU,self.on_exit,id=wx.ID_EXIT)

    menuBar = wx.MenuBar()
    menuBar.Append(menu, "&File")
    return menuBar

  # --- create buttons   ------------------------------------------------------

  def create_buttons(self,parent):
    button_panel = wx.Panel(parent)
    sys_btn      = wx.Button(button_panel,-1,"System")
    disk_btn     = wx.Button(button_panel,-1,"Disk")
    net_btn      = wx.Button(button_panel,-1,"Network")

    self.Bind(wx.EVT_BUTTON,self.on_uptime,sys_btn)
    self.Bind(wx.EVT_BUTTON,self.on_df,disk_btn)
    self.Bind(wx.EVT_BUTTON,self.on_ip,net_btn)

    hbox = wx.BoxSizer(wx.HORIZONTAL)
    hbox.Add(sys_btn,0,wx.ALL,10)
    hbox.Add(disk_btn,0,wx.ALL,10)
    hbox.Add(net_btn,0,wx.ALL,10)
    button_panel.SetSizer(hbox)
    return button_panel

  # --- create output-area   --------------------------------------------------

  def create_outputarea(self,parent):
    text_panel = wx.Panel(parent)
    text_panel.SetBackgroundColour(wx.BLUE)
    
    self._output_text = wx.StaticText(text_panel, -1,"")
    self._output_text.SetForegroundColour(wx.WHITE)
    self._output_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
    self._output_text.SetSize(self._output_text.GetBestSize())

    hbox = wx.BoxSizer(wx.HORIZONTAL)
    hbox.Add(self._output_text,1,wx.EXPAND,0)
    text_panel.SetSizer(hbox)
    return text_panel

  # --- on_uptime handler   ---------------------------------------------------

  def on_uptime(self,evt):
    """ start asynchronous command """
    threading.Thread(target=self.get_uptime).start()

  # --- on_df handler   -------------------------------------------------------

  def on_df(self,evt):
    """ start asynchronous command """
    threading.Thread(target=self.get_df).start()

  # --- on_ip handler   -------------------------------------------------------

  def on_ip(self,evt):
    """ start asynchronous command """
    threading.Thread(target=self.get_ip).start()

  # --- event-handler for updates to the text field   -------------------------

  def on_syscmd_result(self,evt):
    self._output_text.SetLabelText(evt.get_output())

  # --- exit-handler   --------------------------------------------------------

  def on_exit(self,evt):
    """ exit-handler """
    self.Close()

  # --- get uptime (asynchronous execution)   ---------------------------------

  def get_uptime(self):
    hostname = subprocess.check_output("hostname",stderr=subprocess.STDOUT).split()
    uptime = subprocess.check_output("uptime",stderr=subprocess.STDOUT).split()
    output = """Hostname: %s
Uhrzeit:  %s
Uptime:   %s Tage, %s Stunden
Benutzer: %s
Last:     %s %s %s""" % (hostname[0],uptime[0],uptime[1],uptime[3],
                 uptime[5],uptime[8],uptime[9],uptime[10])
    evt = SysCmdFinishEvent(-1,output)
    wx.PostEvent(self,evt)

  # --- get free disk space (asynchronous execution)   ------------------------

  def get_df(self):
    args   = ["df","-h","--output=source,size,avail,pcent"]
    output = subprocess.check_output(args,stderr=subprocess.STDOUT)
    #output = re.sub(r'\t','    ',output)
    evt = SysCmdFinishEvent(-1,output)
    wx.PostEvent(self,evt)

  # --- get ip information (asynchronous execution)   -------------------------

  def get_ip(self):
    args = ["ip","-o","addr","show","up"]
    ip = subprocess.check_output(args,stderr=subprocess.STDOUT).split('\n')
    output = "Network:"
    for line in ip:
      line = line.split()
      if line:
        output = "{0}\n{1} {2} {3} {4}".format(output,*line[:4])
    evt = SysCmdFinishEvent(-1,output)
    wx.PostEvent(self,evt)

# --- main application class   ------------------------------------------------

class WxVlcdApp(wx.App):
  def OnInit(self):
    frame = AppFrame(None, "Virtual LCD")
    self.SetTopWindow(frame)
    frame.Show(True)
    return True
        
# --- main program   ----------------------------------------------------------

if __name__ == '__main__':
  app = WxVlcdApp(redirect=False)
  app.MainLoop()

