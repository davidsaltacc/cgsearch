using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Media.Imaging;
using System;
using System.IO;

namespace CGSearchUI;

public partial class PopupWindow : Window
{

    public string TextContent { get; set; }
    public string Button1Content { get; set; }
    public string Button2Content { get; set; }

    private readonly Action<PopupWindow> Button1Handler;
    private readonly Action<PopupWindow> Button2Handler;

    public PopupWindow(string textContent, string button1Content, string button2Content, Action<PopupWindow> button1Handler, Action<PopupWindow> button2Handler)
    {

        TextContent = textContent;
        Button1Content = button1Content;
        Button2Content = button2Content;
        Button1Handler = button1Handler;
        Button2Handler = button2Handler;

        InitializeComponent();

        DataContext = this;
        TitleBarIcon.Source = new Bitmap(Path.Combine(AppContext.BaseDirectory, "icon.ico"));

    }

    void Button1Clicked(object? sender, RoutedEventArgs e)
    {
        Button1Handler.Invoke(this);
    }

    void Button2Clicked(object? sender, RoutedEventArgs e)
    {
        Button2Handler.Invoke(this);
    }
}