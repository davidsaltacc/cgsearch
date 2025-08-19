using Avalonia.Controls;
using Avalonia.Media.Imaging;
using System;
using System.IO;

namespace CGSearchUI;

public partial class SettingsWindow : Window
{
    public SettingsWindow()
    {
        InitializeComponent();
        TitleBarIcon.Source = new Bitmap(Path.Combine(AppContext.BaseDirectory, "icon.ico"));
        DataContext = this;
    }
}