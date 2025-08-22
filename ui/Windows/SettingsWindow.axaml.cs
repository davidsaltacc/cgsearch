using Avalonia.Controls;
using Avalonia.Media.Imaging;
using Newtonsoft.Json.Linq;
using System;
using System.IO;

namespace CGSearchUI;

public partial class SettingsWindow : Window
{

    public bool AskPopup 
    {
        get 
        {
            return SharedStuff.askPopup;
        }
        set
        {
            WarningPopupBox.IsEnabled = !value;
            SharedStuff.askPopup = value;
        }
    }
    public bool AskPopupWarnings { 
        get {
            return SharedStuff.askPopupWarnings;
        }
        set {
            SharedStuff.askPopupWarnings = value;
        }
    }
    public bool BoostOfficialLinks
    {
        get
        {
            return SharedStuff.boostOfficialLinks;
        }
        set
        {
            IPCHelper.SendMessage("bsof", value ? "true" : "false");
            SharedStuff.boostOfficialLinks = value;
        }
    }

    public SettingsWindow()
    {
        InitializeComponent();
        TitleBarIcon.Source = new Bitmap(Path.Combine(AppContext.BaseDirectory, "icon.ico"));
        DataContext = this;

        if (IPCHelper.engines == null)
        {
            return;
        }

        foreach (var engine in IPCHelper.engines)
        {
            string id = engine.Key;
            string name = engine.Value.ToObject<JObject>().GetValue("name").ToString();

            var enabled = engine.Value.ToObject<JObject>()["enabled"];

            var cbox = new CheckBox
            {
                Content = name,
                IsChecked = enabled == null || bool.Parse(enabled.ToString()),
            };

            cbox.Click += (sender, args) => {
                var newObj = engine.Value.ToObject<JObject>();
                newObj["enabled"] = cbox.IsChecked.Value;
                IPCHelper.engines[id] = newObj;
                IPCHelper.SendMessage("xegn", "{\"action\":\"" + (cbox.IsChecked.Value ? "include" : "exclude") + "\",\"id\":\"" + id + "\"}");
            };
            
            AllEnginesContainer.Children.Add(cbox);
        }

    }
}