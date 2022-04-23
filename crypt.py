from cryptography.fernet import Fernet
import wx

APP_EXIT = 1
BOTTON1 = 2
BOTTON2 = 3
BOTTON3 = 4


class Crypt(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 300))
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Path to the file:')
        self.tc1 = wx.TextCtrl(panel)
        hbox1.Add(st1, flag=wx.RIGHT | wx.LEFT | wx.TOP, border=6)
        hbox1.Add(self.tc1, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, BOTTON1, label='encrypt', size=(85, 25))
        btn2 = wx.Button(panel, BOTTON2, label='decrypt', size=(85, 25))
        self.tc2 = wx.TextCtrl(panel, value='Key')
        hbox2.Add(btn1, flag=wx.RIGHT, border=5)
        hbox2.Add(btn2, flag=wx.RIGHT, border=5)
        hbox2.Add(self.tc2, flag=wx.ALIGN_CENTER, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        btn3 = wx.Button(panel, BOTTON3, label='Show content', size=(175, 25))
        vbox.Add(btn3, flag=wx.LEFT | wx.TOP, border=10)

        self.tc3 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        vbox.Add(self.tc3, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)
        menubar = wx.MenuBar()
        filemenu = wx.Menu()

        filemenu.Append(wx.ID_OPEN, '&Open\tCtrl+O')
        filemenu.AppendSeparator()
        filemenu.Append(APP_EXIT, 'exit\tCtrl+Q')
        menubar.Append(filemenu, '&File')

        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_MENU, self.quit, id=APP_EXIT)
        self.Bind(wx.EVT_MENU, self.find_path, id=wx.ID_OPEN)
        btn1.Bind(wx.EVT_BUTTON, self.encode, id=BOTTON1)
        btn2.Bind(wx.EVT_BUTTON, self.decode, id=BOTTON2)
        btn3.Bind(wx.EVT_BUTTON, self.show_decoded_content, id=BOTTON3)

    def on_close(self, event):
        dial = wx.MessageDialog(None, "Are you sure to quit? Don't forget to save your key!", 'Warning',
                                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        rest = dial.ShowModal()
        if rest == wx.ID_YES:
            self.Destroy()
        else:
            event.Veto()

    def quit(self, event):
        self.Close()

    def find_path(self, event):
        style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        dialog = wx.FileDialog(None, 'Open', style=style)
        if dialog.ShowModal() == wx.ID_OK:
            self.path = dialog.GetPath()
        else:
            self.path = None
        self.tc1.SetValue(self.path)

    def encode(self, event):
        if self.tc2.GetValue() in ['', 'Key']:
            dial = wx.MessageDialog(None, "Are you sure to encode? Don't forget to save your key!", 'Warning',
                                    wx.YES_NO | wx.NO_DEFAULT)
            rest = dial.ShowModal()
            if rest == wx.ID_YES:
                event.Skip()
            else:
                return None
            try:
                text = open(self.path, 'rb').read()
            except:
                return wx.MessageDialog(None, "Can't open the file", 'Warning',
                                        wx.OK | wx.ICON_WARNING).ShowModal()
            key = Fernet.generate_key()
            f = Fernet(key)
            try:
                with open(self.path, 'wb') as file:
                    file.write(f.encrypt(text))
                return self.tc2.SetValue(key)
            except:
                return wx.MessageDialog(None, "Can't encrypt a file", 'Warning',
                                        wx.OK | wx.ICON_WARNING).ShowModal()
        else:
            return wx.MessageDialog(None, "Maybe the file was already encrypted!", 'Warning',
                                    wx.OK).ShowModal()

    def show_decoded_content(self, event):
        try:
            key = self.tc2.GetValue()
            f = Fernet(key)
        except:
            return wx.MessageDialog(None, "Key is expected", 'Warning',
                                    wx.OK | wx.ICON_WARNING).ShowModal()
        try:
            with open(self.path, 'rb') as text:
                content = f.decrypt(text.read()).decode()
            self.tc3.SetValue(content)
        except:
            return wx.MessageDialog(None, "File Error", 'Warning',
                                    wx.OK | wx.ICON_WARNING).ShowModal()

    def decode(self, event):
        try:
            key = self.tc2.GetValue()
            f = Fernet(key)
        except:
            return wx.MessageDialog(None, "Key is expected", 'Warning',
                                    wx.OK | wx.ICON_WARNING).ShowModal()
        try:
            text = open(self.path, 'rb').read()
            with open(self.path, 'wb') as file:
                file.write(f.decrypt(text))
            self.tc2.SetValue('Key')
            self.tc3.SetValue('')
            return wx.MessageDialog(None, "File Decoded", 'Message',
                                    wx.OK).ShowModal()
        except:
            return wx.MessageDialog(None, "File Error", 'Warning',
                                    wx.OK | wx.ICON_WARNING).ShowModal()


if __name__ == '__main__':
    app = wx.App()
    frame = Crypt(None, 'Crypt')
    frame.Show()
    frame.Centre()
    app.MainLoop()
