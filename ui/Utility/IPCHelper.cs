using Newtonsoft.Json.Linq;
using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace CGSearchUI
{
    class IPCHelper
    {

        static public JObject? engines;

        static Stream? PyStdin;
        static Stream? PyStdout;

        public static Process StartPython()
        {
            var psi = new ProcessStartInfo
            {
                FileName = "bin/runtime/python.exe",
                Arguments = "main.py CGSearch",
                WorkingDirectory = "search",
                RedirectStandardInput = true,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            Process? process;

            try
            {
                process = Process.Start(psi);
            }
            catch (Exception ex) 
            {
                MessageBox("Failed to launch search engine backend. Please re-install CGSearch to try and fix this issue.\n\nError: " + ex, "Error starting python", "Error");
                Environment.Exit(-1);
                return null;
            }

            Task errorTask = new(() =>
            {
                var pyStderr = process.StandardError.BaseStream;
                while (true) 
                {
                    var lenBytes = new BinaryReader(pyStderr).ReadBytes(4);
                    int length = System.Net.IPAddress.NetworkToHostOrder(BitConverter.ToInt32(lenBytes, 0));
                    var buffer = new BinaryReader(pyStderr).ReadBytes(length);
                    var data = Encoding.UTF8.GetString(buffer);
                    Debug.WriteLine("[PYTHON STDERR] " + data);
                    MessageBox("Error in search backend occured. \n\n" + data, "Error in python backend", "Error");
                    if (data.Contains("critical"))
                    {
                        Environment.Exit(-1);
                    }
                }
            });
            errorTask.Start();

            PyStdin = process.StandardInput.BaseStream; 
            PyStdout = process.StandardOutput.BaseStream;

            return process;
        }

        public static void SendMessage(byte[] type, byte[] data)
        {
            if (PyStdin == null)
            {
                return;
            }
            if (type.Length != 4)
            {
                throw new ArgumentException("type must be 4 bytes");
            }
            var lenBytes = BitConverter.GetBytes(System.Net.IPAddress.HostToNetworkOrder(type.Length + data.Length));
            PyStdin.Write(lenBytes, 0, 4);
            PyStdin.Write(type, 0, 4);
            PyStdin.Write(data, 0, data.Length);
            PyStdin.Flush();
        }
        
        public static void SendMessage(string type, string data)
        {
            SendMessage(Encoding.UTF8.GetBytes(type), Encoding.UTF8.GetBytes(data));
        }
        
        public static Tuple<byte[]?, byte[]?> ReadMessage()
        {
            if (PyStdout == null)
            {
                return new Tuple<byte[]?, byte[]?>([], []);
            }
            var lenBytes = new BinaryReader(PyStdout).ReadBytes(4);
            int length = System.Net.IPAddress.NetworkToHostOrder(BitConverter.ToInt32(lenBytes, 0));
            var buffer = new BinaryReader(PyStdout).ReadBytes(length);
            byte[] type = new byte[4];
            byte[] data = new byte[buffer.Length - 4];
            Array.Copy(buffer, 0, type, 0, 4); 
            Array.Copy(buffer, 4, data, 0, buffer.Length - 4);
            return new Tuple<byte[]?, byte[]?>(type, data);
        }

        static void MessageBox(String text, String title, String type)
        {
            var command = $@"
Add-Type -AssemblyName PresentationFramework;
[System.Windows.MessageBox]::Show(@'
{text}
'@, '{title}', 'OK', '{type}')
";
            var proc = Process.Start(new ProcessStartInfo
            {
                FileName = "powershell.exe",
                Arguments = $"-NoProfile -EncodedCommand \"{Convert.ToBase64String(Encoding.Unicode.GetBytes(command))}\"",
                CreateNoWindow = true,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false
            });
            string output = proc.StandardOutput.ReadToEnd();
            string error = proc.StandardError.ReadToEnd();
            proc.WaitForExit();
        }

    }
}