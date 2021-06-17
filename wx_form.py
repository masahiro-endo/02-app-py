import wx

# メインフレームクラス
class SampleFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, title=title, pos=(0, 0), size=(320, 500))
        self.__create_widget()
        self.__do_layout()

    # Widgetを作成するメソッド
    def __create_widget(self):
        # テキストWidgetの作成
        self.text = wx.StaticText(self, label="wxPython widgets")
        # テキストボックスWidgetの作成
        self.txtCtrl = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE, size=(200, 150) )
        # ボタンWidgetの作成および、ボタン押下時のイベントを定義
        self.button = wx.Button(self, label="Push Me")
        self.button.Bind(wx.EVT_BUTTON, self.OnButton)
        # コンボボックスWidgetの作成
        self.combobox = wx.ComboBox(self, choices=["choice A", "choice B", "choice C"], style=wx.CB_READONLY)
        # チェックボックスWidgetの作成
        self.checkbox = wx.CheckBox(self, label='Check Box')
        # スライダーWidgetの作成
        self.slider = wx.Slider(self, minValue=1, maxValue=10, size=(200, -1))     
        # ラジオボタンWidgetの作成
        self.radiobutton1 = wx.RadioButton(self, label='radio A')
        self.radiobutton2 = wx.RadioButton(self, label='radio B')
        self.radiobutton3 = wx.RadioButton(self, label='radio C')
        # プログレスバーWidgetの作成
        self.gauge = wx.Gauge(self, size=(250, -1))
        # スピンコントロールWidgetの作成
        self.spinctrl = wx.SpinCtrl(self)

    # レイアウトを設定するメソッド
    def __do_layout(self):
        # レイアウトの設定
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

    # メッセージボックスを表示するメソッド
    def OnButton(event, button_label):
        wx.MessageBox( "Thank you for clicking me.", "Messsage.")

# アプリケーションクラス
class SampleApp(wx.App):
    # wxPythonのアプリケーションクラスの初期化にはOnInitメソッドを使用する
    def OnInit(self):
        # フレームのオブジェクト生成
        frame = SampleFrame(None, -1, "Sample wxPython")
        # メインフレームに設定
        self.SetTopWindow(frame)
        # フレームの表示
        frame.Show(True)
        return True

if __name__ == '__main__':
    # アプリケーションオブジェクトの生成
    app = SampleApp()
    # メインループ
    app.MainLoop()

