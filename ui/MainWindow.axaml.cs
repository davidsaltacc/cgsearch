using Avalonia.Controls;
using Avalonia.Threading;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;

namespace CGSearchUI
{
    public partial class MainWindow : Window
    {

        public ObservableCollection<EngineResultLink> Results { get; }

        public MainWindow()
        {
            InitializeComponent();

            var results = new List<EngineResultLink>{
                new("Hollow Knight", "FitGirl", "Gofile", "Example URL", "Direct", 0.95f),
                new("Hollow Knight vSomething", "Dodi", "Gofile", "Example URL", "Direct", 0.9f),
                new("Hollow Thing", "Some Repacker", "Torrent Download", "magnet:somefuckingshitbroidk", "Torrent", 0.68f)
            };
            Results = new ObservableCollection<EngineResultLink>(results);
            DataContext = this;

            Dispatcher.UIThread.InvokeAsync(() => this.FindControl<DataGrid>("ResultsDataGrid").Columns.Last().Sort(ListSortDirection.Descending));

        }
    }
}