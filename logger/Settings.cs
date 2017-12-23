using Newtonsoft.Json;
using System;
using System.IO;
using System.Linq;

namespace Laba_8
{
    public class Settings
    {
        public bool IsHooks { get; set; }
        public string Email { get; set; }
        public long FileSize { get; set; }
        public bool HideCheck { get; set; }

        public Settings UpdateProgram()
        {
            try
            {
                using (var streamReader = new StreamReader("./config.txt"))
                {
                    return JsonConvert.DeserializeObject<Settings>(Decode(streamReader.ReadToEnd()));
                }
            }
            catch (Exception)
            {
                return new Settings();
            }
        }

        public void SaveConfig(Settings config)
        {
            using (var streamWriter = new StreamWriter("./config.txt", false))
            {
                streamWriter.Write(Encode(JsonConvert.SerializeObject(config)));
            }
        }

        private string Encode(string content)
        {
            var tempList = content.ToList();
            for (int i = 0; i < tempList.Count; i++)
            {
                tempList[i] = (char)(tempList[i] + 1);
            }
            return string.Join("", tempList);
        }

        private string Decode(string content)
        {
            var tempList = content.ToList();
            for (int i = 0; i < tempList.Count; i++)
            {
                tempList[i] = (char)(tempList[i] - 1);
            }
            return string.Join("", tempList);
        }
    }
}
