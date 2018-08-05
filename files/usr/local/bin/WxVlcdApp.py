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

import wx

class AppFrame(wx.Frame):
  """ Application toplevel frame """

  # --- Constructor   ---------------------------------------------------------
  
  def __init__(self, parent, title):
    wx.Frame.__init__(self, parent, -1, title,size=(800, 480))

    #self.SetMenuBar(self.create_menu())
    #self.CreateStatusBar()
    self.create_controls()

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
    text_panel.SetBackgroundColour('blue')
    
    text = wx.StaticText(text_panel, -1, "Hello World!")
    text.SetForegroundColour(wx.WHITE)
    text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
    text.SetSize(text.GetBestSize())

    hbox = wx.BoxSizer(wx.HORIZONTAL)
    hbox.Add(text,1,wx.EXPAND,0)
    text_panel.SetSizer(hbox)
    text_panel.Layout()
    return text_panel

  # --- on_uptime handler   ---------------------------------------------------

  def on_uptime(self,evt):
    pass

  # --- on_df handler   -------------------------------------------------------

  def on_df(self,evt):
    pass

  # --- on_ip handler   -------------------------------------------------------

  def on_ip(self,evt):
    pass

  # --- exit-handler   --------------------------------------------------------

  def on_exit(self,evt):
    """ exit-handler """
    self.Close()

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

