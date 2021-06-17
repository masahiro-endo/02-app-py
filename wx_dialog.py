import wx

# メインフレームクラス
class SampleFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, title=title, pos=(0, 0), size=(320, 240))
        self.__create_widget()
        self.__do_layout()

    def __create_widget(self):
        self.text = wx.StaticText(self, label="Hello World", pos=wx.Point(50, 20))
        self.button = wx.Button(self, label="Push Me")
        self.button.Bind(wx.EVT_BUTTON, self.OnButton)

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text, flag=wx.ALIGN_LEFT)
        sizer.Add(self.button, flag=wx.ALIGN_CENTER | wx.TOP, border=15)
        self.SetSizer(sizer)


    def OnButton(event, button_label):
        wx.MessageBox( "Thank you for clicking me.", "Messsage.")


# アプリケーションクラス
class SampleApp(wx.App):
    # wxPythonのアプリケーションクラスの初期化にはOnInitメソッドを使用する
    def OnInit(self):
        frame = SampleFrame(None, -1, "Sample wxPython")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

if __name__ == '__main__':
    app = SampleApp()
    app.MainLoop()

