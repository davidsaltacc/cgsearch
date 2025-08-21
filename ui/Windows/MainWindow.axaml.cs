using Avalonia;
using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Interactivity;
using Avalonia.LogicalTree;
using Avalonia.Media.Imaging;
using Avalonia.Threading;
using Avalonia.VisualTree;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CGSearchUI
{
    public partial class MainWindow : Window
    {

        public ObservableCollection<EngineResultLink> Results { get; }

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

            if (Design.IsDesignMode)
            {
                return;
            }

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
                                        IPCHelper.engines.GetValue(engineId).ToObject<JObject>().GetValue("name").ToString(),
                                        repackData.GetValue("LinkName").ToString(),
                                        repackData.GetValue("LinkUrl").ToString(),
                                        repackData.GetValue("LinkType").ToString(),
                                        repackData.GetValue("RepackPage").ToString(),
                                        float.Parse(repackData.GetValue("Score").ToString())
                                    ));
                                });

                                break;
                            }
                        case "egns":
                            {
                                IPCHelper.engines = JObject.Parse(text ?? "{}");
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
                                    var isWarning = result != null;
                                    var popuptext = "Do you want to open this with " + SystemHelpers.GetAssociatedApp((string) value) + "?";
                                    popuptext = isWarning ? result + "\n\n" + popuptext : popuptext;

                                    void startFunc()
                                    {
                                        Process.Start(new ProcessStartInfo((string)value) { UseShellExecute = true });
                                    }

                                    if (SharedStuff.askPopup || (SharedStuff.askPopupWarnings && isWarning))
                                    {
                                        var popup = new PopupWindow(popuptext, "Okay", "Cancel", (popup) =>
                                        {
                                            startFunc();
                                            popup.Close();
                                        }, (popup) =>
                                        {
                                            popup.Close();
                                        });
                                        popup.ShowDialog(this);
                                    } else
                                    { 
                                        startFunc(); 
                                    }
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
                        foreach (var engine in IPCHelper.engines?.Values())
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

                            void startFunc()
                            {
                                Process.Start(new ProcessStartInfo(homepage) { UseShellExecute = true });
                            }

                            if (SharedStuff.askPopup)
                            {
                                var popup2 = new PopupWindow("Do you want to open this with " + SystemHelpers.GetAssociatedApp(homepage) + "?", "Okay", "Cancel", (popup2) =>
                                {
                                    startFunc();
                                    popup2.Close();
                                }, (popup2) =>
                                {
                                    popup2.Close();

                                });
                                popup2.ShowDialog(this);
                            } else
                            {
                                startFunc();
                            }

                        });
                        popup.ShowDialog(this);
                        break;
                    }
                case "RepackPage":
                    {
                        void startFunc()
                        {
                            Process.Start(new ProcessStartInfo((string)(value ?? "")) { UseShellExecute = true });
                        }

                        if (SharedStuff.askPopup)
                        {
                            var popup = new PopupWindow("Do you want to open this with " + SystemHelpers.GetAssociatedApp((string) (value ?? "")) + "?", "Okay", "Cancel", (popup) =>
                            {
                                startFunc();
                                popup.Close();
                            }, (popup) =>
                            {
                                popup.Close();

                            });
                            popup.ShowDialog(this);
                        }
                        else
                        {
                            startFunc();
                        }
                        break;
                    }
                default: break;
            }
        }

        private void LinkCell_PointerPressed(object? sender, PointerPressedEventArgs? e) {
            if (e != null && !e.GetCurrentPoint((TextBlock?) sender).Properties.IsLeftButtonPressed)
            {
                return;
            }
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

        private void RepackPageCell_PointerPressed(object? sender, PointerPressedEventArgs? e)
        {
            if (e != null && !e.GetCurrentPoint((TextBlock?) sender).Properties.IsLeftButtonPressed)
            { 
                return;
            }
            ClickedCell("RepackPage", ((TextBlock?) sender).Text, null);
            // fullResult can be null, only needed when a link LinkUrl cell is clicked
        }

        private void ProviderCell_PointerPressed(object? sender, PointerPressedEventArgs e)
        {
            if (e != null && !e.GetCurrentPoint((TextBlock?) sender).Properties.IsLeftButtonPressed)
            {
                return;
            }
            ClickedCell("Provider", ((TextBlock?) sender).Text, null); 
            // fullResult can be null, only needed when a link LinkUrl cell is clicked
        }

        private void LinkUrlContextMenu_Open_Clicked(object? sender, RoutedEventArgs e) 
        {
            TextBlock? cell = ((MenuItem?) sender).FindLogicalAncestorOfType<TextBlock>();
            if (cell != null) {
                LinkCell_PointerPressed(cell, null);
            }
        }

        private void LinkUrlContextMenu_Copy_Clicked(object? sender, RoutedEventArgs e)
        {
            TextBlock? cell = ((MenuItem?) sender).FindLogicalAncestorOfType<TextBlock>();
            if (cell != null)
            {
                Clipboard.SetTextAsync(cell.Text);
            }
        }

        private void RepackPageContextMenu_Open_Clicked(object? sender, RoutedEventArgs e)
        {
            TextBlock? cell = ((MenuItem?) sender).FindLogicalAncestorOfType<TextBlock>();
            if (cell != null)
            {
                RepackPageCell_PointerPressed(cell, null);
            }
        }

        private void RepackPageContextMenu_Copy_Clicked(object? sender, RoutedEventArgs e)
        {
            TextBlock? cell = ((MenuItem?) sender).FindLogicalAncestorOfType<TextBlock>();
            if (cell != null)
            {
                Clipboard.SetTextAsync(cell.Text);
            }
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

        void SettingsClicked(object? sender, RoutedEventArgs e)
        {
            var settings = new SettingsWindow();
            settings.ShowDialog(this);
        }

    }
}