import wx
from wx.svg import SVGimage


class MainPage:

    def OnClicked(event):
        print("Settings")

    # room switch event
    def OnRooms(self, event):
        """ @l33tlinux TODO: DYNAMIC ROOM SWITCHING (COMMUNICATION USERNAMES_ROOMS DICT)
            If you  want to access it, think about parsing the communication object to the class __init__ call """
        if self.rooms.GetStringSelection() == "Connect":
            client.start_client()
        elif self.rooms.GetStringSelection() == "Room 1":
            print("room switched: Room 1")
            client.enter_room("room1")
        elif self.rooms.GetStringSelection() == "Room 2":
            print("room switched: Room 2")
            client.enter_room("room2")
        elif self.rooms.GetStringSelection() == "Room 3":
            print("room switched: Room 3")
            client.enter_room("room3")

    # options events
    def OnMute(event):
        pass
        """client.muted = not client.muted
        print("muted " + str(client.muted))"""

    def OnDeaf(event):
        pass
        """client.deaf = not client.deaf
        print("deaf " + str(client.deaf))"""

    def OnLeave(event):
        pass
        """client.stop_client()
        window.Close()"""

    def __init__(self):

        # window stuff
        resolution = (1080, 720)
        icon_size = (16, 16)
        bsize = (32, 32)
        app = wx.App()

        # sets the default window size
        window = wx.Frame(None, size=resolution)
        # makes the window so that it can't be shrunk less than the default size
        window.SetMinSize(resolution)

        # settings for window
        window.SetBackgroundColour("#030017")
        window.SetTitle("Better Discord (dot) py")

        # make panels left, middle and right and set attributes
        panel = wx.Panel(window)
        left_panel = wx.Panel(panel, size=(200, wx.EXPAND))
        left_panel.SetBackgroundColour("#251C3B")
        left_panel.SetForegroundColour("white")

        #         # for future expansion
        #         mid_panel = wx.Panel(panel)
        #         right_panel = wx.Panel(panel)

        # load images
        img_deaf = SVGimage.CreateFromFile("ui/graphics/ear.svg")
        img_undeaf = SVGimage.CreateFromFile("ui/graphics/deaf.svg")
        img_leave = SVGimage.CreateFromFile("ui/graphics/exit.svg")
        img_mic = SVGimage.CreateFromFile("ui/graphics/mute.svg")
        img_muted = SVGimage.CreateFromFile("ui/graphics/mic.svg")
        img_rnnoise = SVGimage.CreateFromFile("ui/graphics/sound_waves.svg")
        img_rnnoised = SVGimage.CreateFromFile("ui/graphics/sound_waves.svg")
        img_room = SVGimage.CreateFromFile("ui/graphics/room.svg")
        img_settings = SVGimage.CreateFromFile("ui/graphics/settings.svg")

        # convert images to a usable format
        bmp_deaf = img_deaf.ConvertToScaledBitmap(icon_size)
        bmp_undeaf = img_undeaf.ConvertToScaledBitmap(icon_size)
        bmp_leave = img_leave.ConvertToScaledBitmap(icon_size)
        bmp_mic = img_mic.ConvertToScaledBitmap(icon_size)
        bmp_muted = img_muted.ConvertToScaledBitmap(icon_size)
        bmp_rnnoise = img_rnnoise.ConvertToScaledBitmap(icon_size)
        bmp_rnnoised = img_rnnoised.ConvertToScaledBitmap(icon_size)
        bmp_room = img_room.ConvertToScaledBitmap(icon_size)
        bmp_settings = img_settings.ConvertToScaledBitmap(icon_size)

        # rooms header
        rooms_text = wx.StaticText(panel, label="Rooms", size=(200, 20), style=wx.ALIGN_CENTER)
        rooms_text.SetForegroundColour("white")

        # replaced with listbox!
        room_list = ["Connect", "Room 1", "Room 2", "Room 3"]   # @l33tlinux TODO: REPLACE WITH DYNAMIC ROOMS (COMMUNICATION.PY USERNAMES_ROOMS DICT)
        self.rooms = wx.ListBox(left_panel, size=(190, 360), choices=room_list, style=wx.LB_SINGLE)
        self.rooms.SetBackgroundColour("#251C3B")
        app.Bind(wx.EVT_LISTBOX, self.OnRooms, self.rooms)

        # add actions bar
        settings_b = wx.Button(left_panel, size=bsize)
        settings_b.SetBitmap(bmp_settings)
        settings_b.Bind(wx.EVT_BUTTON, self.OnClicked)

        mute_b = wx.ToggleButton(left_panel, size=bsize)
        mute_b.SetBitmap(bmp_mic)
        mute_b.SetBitmapPressed(bmp_muted)
        mute_b.Bind(wx.EVT_TOGGLEBUTTON, self.OnMute)

        deaf_b = wx.ToggleButton(left_panel, size=bsize)
        deaf_b.SetBitmap(bmp_deaf)
        deaf_b.SetBitmapPressed(bmp_undeaf)
        deaf_b.Bind(wx.EVT_TOGGLEBUTTON, self.OnDeaf)

        rnnoise_b = wx.ToggleButton(left_panel, size=bsize)
        rnnoise_b.SetBitmap(bmp_rnnoise)
        rnnoise_b.SetBitmapPressed(bmp_rnnoised)
        rnnoise_b.Bind(wx.EVT_TOGGLEBUTTON, self.OnClicked)

        leave_b = wx.Button(left_panel, size=bsize)
        leave_b.SetBitmap(bmp_leave)
        leave_b.Bind(wx.EVT_BUTTON, self.OnLeave)

        # main panels controlled by sizers h/v and left, mid and right
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        l_sizer = wx.BoxSizer(wx.VERTICAL)

        #         # for future additions...
        #         m_sizer = wx.BoxSizer(wx.VERTICAL)
        #         r_sizer = wx.BoxSizer(wx.VERTICAL)

        # sizer for rooms

        # adding items to sizer
        l_sizer.AddSpacer(10)
        l_sizer.Add(rooms_text)
        l_sizer.AddSpacer(10)
        l_sizer.Add(rooms, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)

        # sizer for action buttons
        action_sizer = wx.BoxSizer(wx.HORIZONTAL)
        action_sizer.AddStretchSpacer()
        action_sizer.Add(settings_b)
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
        window.Show()
        app.MainLoop()