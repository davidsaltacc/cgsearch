using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.Primitives;
using Avalonia.Input;
using Avalonia.Interactivity;
using Avalonia.Media.Imaging;
using Avalonia.Threading;
using Avalonia.VisualTree;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CGSearchUI
{
    public partial class MainWindow : Window
    {

        public ObservableCollection<EngineResultLink> Results { get; }

        private JObject? engines;

        private object _lock = new object();

        public static readonly StyledProperty<bool> IsSearchingProperty = AvaloniaProperty.Register<MainWindow, bool>(nameof(IsSearching));

        public bool IsSearching
        {
            get => GetValue(IsSearchingProperty);
            set => SetValue(IsSearchingProperty, value);
        }

        public MainWindow()
        {
            InitializeComponent();

            TitleBarIcon.Source = new Bitmap(Path.Combine(AppContext.BaseDirectory, "icon.ico"));

            var results = new List<EngineResultLink>{};
            Results = new ObservableCollection<EngineResultLink>(results);
            DataContext = this;

            Dispatcher.UIThread.InvokeAsync(() => ResultsDataGrid.Columns.Last().Sort(ListSortDirection.Descending));

            ResultsDataGrid.AddHandler(InputElement.PointerPressedEvent,
                new EventHandler<PointerPressedEventArgs>(DataGrid_PointerPressed), RoutingStrategies.Tunnel);

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

                                JArray? allLinks = (JArray?) repackData.GetValue("DownloadLinks");

                                foreach (var link in allLinks)
                                {

                                    JArray linkData = (JArray) link;

                                    Dispatcher.UIThread.InvokeAsync(() =>
                                    {
                                        Results.Add(new EngineResultLink(
                                            repackData.GetValue("RepackTitle").ToString(),
                                            engines.GetValue(engineId).ToObject<JObject>().GetValue("name").ToString(),
                                            linkData.ElementAt(0).ToString(),
                                            linkData.ElementAt(1).ToString(),
                                            linkData.ElementAt(2).ToString(),
                                            float.Parse(repackData.GetValue("Score").ToString())
                                        ));
                                    });
                                }

                                break;
                            }
                        case "egns":
                            {
                                engines = JObject.Parse(text ?? "{}");
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

        private void DataGrid_PointerPressed(object? sender, PointerPressedEventArgs e)
        {

            if (sender is DataGrid grid)
            {

                grid.SelectedIndex = -1;
                grid.SelectedItem = null;
                grid.SelectedItems.Clear();

                var hit = grid.InputHitTest(e.GetPosition(grid)) as Control;

                var cell = hit?.FindAncestorOfType<DataGridCell>();
                if (cell == null) 
                {
                    return;
                }

                var row = cell.FindAncestorOfType<DataGridRow>();
                if (row == null) 
                {
                    return;
                }

                var presenter = row.FindDescendantOfType<DataGridCellsPresenter>();
                if (presenter == null)
                {
                    return;
                }

                e.Handled = true;

            }

        }

        private void ClickedCell(string column, object? value, EngineResultLink fullResult)
        {
            switch (column)
            {
                case "LinkUrl":
                    {
                        // yeah show a dialog or smt idk yet
                        break;
                    }
                default: break;
            }
        }

        void LinkCell_PointerPressed(object sender, PointerPressedEventArgs e) {
            


        }

        void SearchClicked(object? sender, RoutedEventArgs e) 
        {
            IPCHelper.SendMessage("srch", "hollow knight");
            IsSearching = true;
        }

        void CancelClicked(object? sender, RoutedEventArgs e)
        {
            IPCHelper.SendMessage("cncl", "");
        }

    }
}