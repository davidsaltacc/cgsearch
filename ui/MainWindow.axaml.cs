using Avalonia;
using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Interactivity;
using Avalonia.Media.Imaging;
using Avalonia.Threading;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace CGSearchUI
{
    public partial class MainWindow : Window
    {

        public ObservableCollection<EngineResultLink> Results { get; }

        private JObject? engines;

        public static readonly StyledProperty<bool> IsSearchingProperty = AvaloniaProperty.Register<MainWindow, bool>(nameof(IsSearching));

        public bool IsSearching
        {
            get => GetValue(IsSearchingProperty);
            set => SetValue(IsSearchingProperty, value);
        }

        private Dictionary<string, Action<string?>> waitingForLinkInfo = new(); 

        public MainWindow()
        {

            InitializeComponent();

            TitleBarIcon.Source = new Bitmap(Path.Combine(AppContext.BaseDirectory, "icon.ico"));

            var results = new List<EngineResultLink>{};
            Results = new ObservableCollection<EngineResultLink>(results);
            DataContext = this;

            Dispatcher.UIThread.InvokeAsync(() => ResultsDataGrid.Columns.Last().Sort(ListSortDirection.Descending));

            IPCHelper.StartPython();

            Task IPCTask = new(() => 
            {
                while (true)
                {
                    var response = IPCHelper.ReadMessage();
                    var type = Encoding.UTF8.GetString(response.Item1 ?? []);
                    var text = Encoding.UTF8.GetString(response.Item2 ?? []);

                    switch (type)
                    {
                        case "rset":
                            {
                                Dispatcher.UIThread.InvokeAsync(() =>
                                {
                                    Results.Clear();
                                });
                                break;
                            }
                        case "link":
                            {
                                JObject? data = JObject.Parse(text);
                                JObject? repackData = (JObject?) data.GetValue("result");
                                string? engineId = (string?) data.GetValue("engine_id");

                                Dispatcher.UIThread.InvokeAsync(() =>
                                {
                                    Results.Add(new EngineResultLink(
                                        repackData.GetValue("RepackTitle").ToString(),
                                        engines.GetValue(engineId).ToObject<JObject>().GetValue("name").ToString(),
                                        repackData.GetValue("LinkName").ToString(),
                                        repackData.GetValue("LinkUrl").ToString(),
                                        repackData.GetValue("LinkType").ToString(),
                                        float.Parse(repackData.GetValue("Score").ToString())
                                    ));
                                });

                                break;
                            }
                        case "egns":
                            {
                                engines = JObject.Parse(text ?? "{}");
                                break;
                            }
                        case "lnfo":
                            {
                                JObject? data = JObject.Parse(text);
                                string? query = data.GetValue("query").ToString();
                                string? message = data.GetValue("message")?.ToString();

                                var success = waitingForLinkInfo.TryGetValue(query, out var callback);

                                if (success) 
                                {
                                    waitingForLinkInfo.Remove(query);
                                    callback.Invoke(message);
                                }

                                break;
                            }
                        case "done":
                            {
                                Dispatcher.UIThread.InvokeAsync(() =>
                                {
                                    IsSearching = false;
                                });
                                break;
                            }
                        default: break;
                    }
                }
            });
            IPCTask.Start();

            IPCHelper.SendMessage("egns", ""); 

        }

        private void ClickedCell(string column, object? value, EngineResultLink? fullResult)
        {
            switch (column)
            {
                case "LinkUrl":
                    {
                        try
                        {
                            // TODO ability to include an exclude engines - functionality already exists
                            // TODO in the gamebounty engine - if there is only one part, and there usually is, then directly provide all the filehosts as seperate links. else - just include the page to the gamebounty page containing parts

                            if (value == null)
                            {
                                break;
                            }

                            List<string> queryList = new();
                            queryList.Add(fullResult.LinkName);
                            queryList.Add(fullResult.LinkUrl);
                            string query = JsonConvert.SerializeObject(queryList);

                            IPCHelper.SendMessage("lnfo", query);

                            waitingForLinkInfo.Add(query, result =>
                            { 
                                Dispatcher.UIThread.InvokeAsync(() =>
                                {
                                    var popuptext = "Do you want to open this with " + GetAssociatedApp((string)value) + "?";
                                    popuptext = (result != null) ? result + "\n\n" + popuptext : popuptext;

                                    var popup = new PopupWindow(popuptext, "Okay", "Cancel", (popup) =>
                                    {
                                        Process.Start(new ProcessStartInfo((string)value) { UseShellExecute = true });
                                        popup.Close();
                                    }, (popup) =>
                                    {
                                        popup.Close();
                                    });
                                    popup.ShowDialog(this);
                                });
                            });

                        } catch (Exception ex)
                        {
                            Debug.WriteLine("failed to open url " + value + ": " + ex);
                        }
                        break;
                    }
                case "Provider":
                    {
                        string description = "";
                        string homepage = "";
                        foreach (var engine in engines?.Values())
                        {
                            JObject? engObj = engine.ToObject<JObject>();
                            if (engObj.GetValue("name").ToString() == (string?) value)
                            {
                                homepage = engObj.GetValue("homepage").ToString();
                                description = engObj.GetValue("description").ToString();
                            }
                        }
                        var popup = new PopupWindow(description, "Close", "Open Homepage", (popup) =>
                        {
                            popup.Close();
                        }, (popup) =>
                        {
                            popup.Close();

                            var popup2 = new PopupWindow("Do you want to open this with " + GetAssociatedApp(homepage) + "?", "Okay", "Cancel", (popup2) =>
                            {
                                Process.Start(new ProcessStartInfo(homepage) { UseShellExecute = true });
                                popup2.Close();
                            }, (popup2) =>
                            {
                                popup2.Close();

                            });
                            popup2.ShowDialog(this);

                        });
                        popup.ShowDialog(this);
                        break;
                    }
                default: break;
            }
        }

        private void LinkCell_PointerPressed(object? sender, PointerPressedEventArgs e) {
            EngineResultLink? fullResult = null;
            foreach (var res in Results)
            {
                if (res.LinkUrl == ((TextBlock?) sender).Text) 
                { 
                    fullResult = res;
                }
            }
            if (fullResult != null)
            {
                ClickedCell("LinkUrl", ((TextBlock?) sender).Text, fullResult);
            }
        }

        private void ProviderCell_PointerPressed(object? sender, PointerPressedEventArgs e)
        {

            ClickedCell("Provider", ((TextBlock?) sender).Text, null); 
            // fullResult can be null, only needed when a link LinkUrl cell is clicked
        }

        void SearchClicked(object? sender, RoutedEventArgs e) 
        {
            IPCHelper.SendMessage("srch", (SearchBar.Text ?? "").Trim());
            IsSearching = true;
        }

        void CancelClicked(object? sender, RoutedEventArgs e)
        {
            IPCHelper.SendMessage("cncl", "");
        }


        [Flags]
        private enum AssocF : uint
        {
            None = 0
        }

        private enum AssocStr
        {
            Executable = 2,
            FriendlyAppName = 4 
        }

        [DllImport("Shlwapi.dll", CharSet = CharSet.Unicode)]
        private static extern uint AssocQueryString(
            AssocF flags,
            AssocStr str,
            string pszAssoc,
            string? pszExtra,
            [Out] StringBuilder? pszOut,
            ref uint pcchOut);

        static string? GetAssociatedApp(string value, bool friendlyName = true)
        {
            string assocKey;

            if (Uri.TryCreate(value, UriKind.Absolute, out var uri))
            {
                assocKey = uri.Scheme;
            }
            else if (value.StartsWith('.'))
            {
                assocKey = value; 
            }
            else
            {
                assocKey = value;
            }

            if (assocKey == null)
            {
                return null;
            }

            uint length = 0;
            AssocStr assocStr = friendlyName ? AssocStr.FriendlyAppName : AssocStr.Executable;

            AssocQueryString(AssocF.None, assocStr, assocKey, null, null, ref length);

            var sb = new StringBuilder((int)length);
            if (AssocQueryString(AssocF.None, assocStr, assocKey, null, sb, ref length) == 0)
            {
                return sb.ToString();
            }

            return null;
        }

    }
}