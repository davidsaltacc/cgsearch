using System;
using System.Runtime.InteropServices;
using System.Text;

namespace CGSearchUI
{
    internal class SystemHelpers
    {

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

        public static string? GetAssociatedApp(string value, bool friendlyName = true)
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
