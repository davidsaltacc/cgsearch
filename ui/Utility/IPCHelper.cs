using Newtonsoft.Json.Linq;
using System;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;

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
                _ = MessageBox(IntPtr.Zero, "Failed to launch search engine backend. Please re-install CGSearch.\n\nError: " + ex, "Error starting python", 0);
                Environment.Exit(-1);
                return null;
            }

            process.ErrorDataReceived += (sender, e) =>
            {
                if (e.Data == null)
                {
                    return;
                }
                Debug.WriteLine("[PYTHON STDERR] " + e.Data);
            };
            process.BeginErrorReadLine();

            PyStdin = process.StandardInput.BaseStream; 
            PyStdout = process.StandardOutput.BaseStream;

            return process;
        }

        public static void SendMessage(byte[] type, byte[] data)
        {
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
            var lenBytes = new byte[4];
            if (PyStdout.Read(lenBytes, 0, 4) != 4)
            {
                return new Tuple<byte[]?, byte[]?>([], []);
            }
            int length = System.Net.IPAddress.NetworkToHostOrder(BitConverter.ToInt32(lenBytes, 0));
            var buffer = new byte[length];
            int read = 0;
            while (read < length)
            {
                int r = PyStdout.Read(buffer, read, length - read);
                if (r <= 0)
                {
                    return new Tuple<byte[]?, byte[]?>([], []);
                }
                read += r;
            }
            byte[] type = new byte[4];
            byte[] data = new byte[buffer.Length - 4];
            Array.Copy(buffer, 0, type, 0, 4); 
            Array.Copy(buffer, 4, data, 0, buffer.Length - 4);
            return new Tuple<byte[]?, byte[]?>(type, data);
        }

        [DllImport("user32.dll", CharSet = CharSet.Unicode)]
        public static extern int MessageBox(IntPtr hWnd, String text, String caption, uint type);

    }
}