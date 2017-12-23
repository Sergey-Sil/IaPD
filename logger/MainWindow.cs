using System;
using System.Windows.Forms;

namespace Laba_8
{
    public partial class MainWindow : Form
    {
        private readonly Settings _tempConfig = new Settings();
        private readonly GlobalHooks _globalHooks;
        private Settings _config;

        public MainWindow()
        {
            InitializeComponent();
            ConfigInit();
            _globalHooks = new GlobalHooks(_config, MainWindowShow);
        }

        private void ConfigInit()
        {
            _config = _tempConfig.UpdateProgram();
            hooksMode.Checked = _config.IsHooks;
            email.Text = _config.Email;
            fileSize.Value = _config.FileSize > 5000 ? _config.FileSize : 5000;
            hideMode.Checked = _config.HideCheck;
        }

        private void SaveSettingsButtonClick(object sender, EventArgs e)
        {
            _config.Email = email.Text;
            _config.IsHooks = hooksMode.Checked;
            _config.FileSize = (long) fileSize.Value;
            _config.HideCheck = hideMode.Checked;

            _tempConfig.SaveConfig(_config);
        }

        private void HideProgramButtonClick(object sender, EventArgs e)
        {
            Hide();
        }

        private void MainWindowShown(object sender, EventArgs e)
        {
            if (_config.HideCheck)
            {
                Hide();
            }
        }

        private void MainWindowShow()
        {
            Show();
        }
    }
}