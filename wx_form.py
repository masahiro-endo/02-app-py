import wx

# メインフレームクラス
class SampleFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, title=title, pos=(0, 0), size=(320, 500))
        self.__create_widget()
        self.__do_layout()

    def __create_widget(self):
        self.text = wx.StaticText(self, label="wxPython widgets")
        self.txtCtrl = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE, size=(200, 150) )
        self.button = wx.Button(self, label="Push Me")
        self.button.Bind(wx.EVT_BUTTON, self.OnButton)
        self.combobox = wx.ComboBox(self, choices=["choice A", "choice B", "choice C"], style=wx.CB_READONLY)
        self.checkbox = wx.CheckBox(self, label='Check Box')
        self.slider = wx.Slider(self, minValue=1, maxValue=10, size=(200, -1))     
        self.radiobutton1 = wx.RadioButton(self, label='radio A')
        self.radiobutton2 = wx.RadioButton(self, label='radio B')
        self.radiobutton3 = wx.RadioButton(self, label='radio C')
        self.gauge = wx.Gauge(self, size=(250, -1))
        self.spinctrl = wx.SpinCtrl(self)

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text, flag=wx.ALIGN_LEFT)
        sizer.Add(self.txtCtrl, flag=wx.ALIGN_CENTER | wx.TOP, border=7)
        sizer.Add(self.button, flag=wx.ALIGN_CENTER | wx.TOP, border=15)
        sizer.Add(self.combobox, flag=wx.ALIGN_CENTER | wx.TOP, border=5)
        sizer.Add(self.checkbox, flag=wx.ALIGN_CENTER | wx.TOP, border=5)
        sizer.Add(self.slider, flag=wx.ALIGN_CENTER | wx.TOP, border=5)
        sizer.Add(self.radiobutton1, flag=wx.ALIGN_CENTER | wx.TOP, border=5)
        sizer.Add(self.radiobutton2, flag=wx.ALIGN_CENTER | wx.TOP, border=5)
        sizer.Add(self.radiobutton3, flag=wx.ALIGN_CENTER | wx.TOP, border=5)
        sizer.Add(self.gauge, flag=wx.ALIGN_CENTER | wx.TOP, border=5)
        sizer.Add(self.spinctrl, flag=wx.ALIGN_CENTER | wx.TOP, border=5)
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

