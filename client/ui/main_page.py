import os
import wx
from wx.svg import SVGimage

class MainPage:

    def __init__(self):
        # window stuff
        self.resolution = (1080, 720)
        self.icon_size = (16, 16)
        self.bsize = (32, 32)

        # sets the default window size
        self.window = wx.Frame(None, size=self.resolution)
        # makes the window so that it can't be shrunk less than the default size
        self.window.SetMinSize(self.resolution)

    def load_pictures(self):
        # load images
        self.img_deaf = SVGimage.CreateFromFile("graphics/ear.svg")
        self.img_undeaf = SVGimage.CreateFromFile("graphics/deaf.svg")
        self.img_leave = SVGimage.CreateFromFile("graphics/exit.svg")
        self.img_mic = SVGimage.CreateFromFile("graphics/mute.svg")
        self.img_muted = SVGimage.CreateFromFile("graphics/mic.svg")

        # convert images to a usable format
        self.bmp_deaf = self.img_deaf.ConvertToScaledBitmap(self.icon_size)
        self.bmp_undeaf = self.img_undeaf.ConvertToScaledBitmap(self.icon_size)
        self.bmp_leave = self.img_leave.ConvertToScaledBitmap(self.icon_size)
        self.bmp_mic = self.img_mic.ConvertToScaledBitmap(self.icon_size)
        self.bmp_muted = self.img_muted.ConvertToScaledBitmap(self.icon_size)

    def draw_UI(self):
        self.app = wx.App()

        # settings for window
        self.window.SetBackgroundColour("#030017")
        self.window.SetTitle("SimpleSpeak")

        # make panels left, middle and right and set attributes
        panel = wx.Panel(self.window)
        left_panel = wx.Panel(panel, size=(200, wx.EXPAND))
        left_panel.SetBackgroundColour("#251C3B")
        left_panel.SetForegroundColour("white")

        #   # for future expansion
        #   mid_panel = wx.Panel(panel)
        #   right_panel = wx.Panel(panel)

        # rooms header
        rooms_text = wx.StaticText(panel, label="Rooms", size=(200, 20), style=wx.ALIGN_CENTER)
        rooms_text.SetForegroundColour("white")

        # replaced with listbox! # TODO: There is a bug here with the background color
        room_list = ["Connect", "Room 1", "Room 2", "Room 3"]
        rooms = wx.ListBox(left_panel, size=(190, 360), choices=room_list, style=wx.LB_SINGLE)
        rooms.SetBackgroundColour("#251C3B")
        #app.Bind(wx.EVT_LISTBOX, OnRooms, rooms)

        # add actions bar
        #settings_b = wx.Button(left_panel, size=bsize)
        #settings_b.SetBitmap(bmp_settings)
        #settings_b.Bind(wx.EVT_BUTTON, OnClicked)

        mute_b = wx.ToggleButton(left_panel, size=self.bsize)
        mute_b.SetBitmap(self.bmp_mic)
        mute_b.SetBitmapPressed(self.bmp_muted)
        #mute_b.Bind(wx.EVT_TOGGLEBUTTON, OnMute)

        deaf_b = wx.ToggleButton(left_panel, size=self.bsize)
        deaf_b.SetBitmap(self.bmp_deaf)
        deaf_b.SetBitmapPressed(self.bmp_undeaf)
        #deaf_b.Bind(wx.EVT_TOGGLEBUTTON, OnDeaf)

        rnnoise_b = wx.ToggleButton(left_panel, size=self.bsize)
        rnnoise_b.SetBitmap(self.bmp_rnnoise)
        rnnoise_b.SetBitmapPressed(self.bmp_rnnoised)
        #rnnoise_b.Bind(wx.EVT_TOGGLEBUTTON, OnClicked)

        leave_b = wx.Button(left_panel, size=self.bsize)
        leave_b.SetBitmap(self.bmp_leave)
        #leave_b.Bind(wx.EVT_BUTTON, OnLeave)

        # main panels controlled by sizers h/v and left, mid and right
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        l_sizer = wx.BoxSizer(wx.VERTICAL)

        #   # for future additions...
        #   m_sizer = wx.BoxSizer(wx.VERTICAL)
        #   r_sizer = wx.BoxSizer(wx.VERTICAL)

        # sizer for rooms

        # adding items to sizer
        l_sizer.AddSpacer(10)
        l_sizer.Add(rooms_text)
        l_sizer.AddSpacer(10)
        l_sizer.Add(rooms, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        # sizer for action buttons
        action_sizer = wx.BoxSizer(wx.HORIZONTAL)
        action_sizer.AddStretchSpacer()
        action_sizer.Add(self.settings_b)
        action_sizer.AddSpacer(5)
        action_sizer.Add(mute_b)
        action_sizer.AddSpacer(5)
        action_sizer.Add(deaf_b)
        action_sizer.AddSpacer(5)
        action_sizer.Add(rnnoise_b)
        action_sizer.AddSpacer(5)
        action_sizer.Add(leave_b)

        action_sizer.AddStretchSpacer()

        l_sizer.AddStretchSpacer()
        l_sizer.Add(action_sizer, flag=wx.EXPAND)

        main_sizer.Add(l_sizer, flag=wx.EXPAND)

        panel.SetSizer(main_sizer)

        # show everything :P
        self.window.Show()
        self.app.MainLoop()