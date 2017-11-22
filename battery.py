import time
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QComboBox, QLabel, QListView, QLineEdit, QTextEdit, \
    QGridLayout, QListWidget, QListWidgetItem, QMainWindow
import sys
import os
from PyQt5 import QtCore
import wmi
import threading
import win32com.client

class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.timeout = QComboBox()
        self.timeout.addItems(['1', '2', '3', '5', '10', '15', '30', '45', '60', '120', '180'])
        self.timeout.currentIndexChanged.connect(self.change_timeout)

        self.name_timeout = QLabel("min")

        self.type_connect = QLabel("")
        self.remaining_charge = QLabel("")
        self.remaining_time = QLabel("")

        self.change_button = QPushButton("Change")
        self.change_button.setFixedHeight(40)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.timeout, 0, 0)
        mainLayout.addWidget(self.name_timeout, 0, 1)
        mainLayout.addWidget(self.type_connect, 1, 0)
        mainLayout.addWidget(self.remaining_charge, 2, 0)
        mainLayout.addWidget(self.remaining_time, 3, 0)

        qwidget = QWidget()
        qwidget.setLayout(mainLayout)
        self.setCentralWidget(qwidget)

        self.setWindowTitle("Battery")

        self.strComputer = "."
        self.objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        self.t = self.objWMIService.ConnectServer(self.strComputer, "root\WMI")

        self.th = UpdateInfo()
        self.th.update_info.connect(self.update_info)
        self.th.start()
        self.get_current_time()

    def get_current_time(self):
        f = os.popen("powercfg -q")
        query = f.read()
        s = str(query.encode('ascii', 'ignore'))
        number = 0
        for n, i in enumerate(s.split('\\n')):
            if 'VIDEOIDLE' in i:
                number = n
                break
        self.current_time = int(s.split('\\n')[number+6][-8:], 16)//60


    def close_event(self):
        self.change_timeout(self.current_time)

    def change_timeout(self, i):
        time = int(self.timeout.currentText())
        f = os.popen("powercfg -x monitor-timeout-dc " + str(time))


    def update_info(self):
        fully_charge = 1

        batts = self.t.ExecQuery('Select * from BatteryFullChargedCapacity')
        for i, b in enumerate(batts):
            fully_charge = b.FullChargedCapacity

        batts = self.t.ExecQuery('Select * from BatteryStatus where Voltage > 0')
        for i, b in enumerate(batts):
            rem_cap = b.RemainingCapacity

            if b.PowerOnline:
                self.type_connect.setText("Type: AC")
                if b.ChargeRate == 0:
                    self.remaining_time.setText("Remaining time: - h - min")
                else:
                    time_h = (fully_charge - rem_cap)//b.ChargeRate
                    time_min = 60*((fully_charge - rem_cap)%b.ChargeRate)//b.ChargeRate
                    self.remaining_time.setText("Remaining time charging: " + str(time_h) + " h " +
                                            str(time_min) + " min")
            else:
                self.type_connect.setText("Type: Battery")
                self.remaining_time.setText("Remaining time: " + str(rem_cap // b.DischargeRate) + " h " +
                                          str(60*(rem_cap % b.DischargeRate)//b.DischargeRate) + " min")
            self.remaining_charge.setText("Remaining charge: " + str(int(rem_cap * 100 / fully_charge)) + " %")


class UpdateInfo(QtCore.QThread):
    update_info = QtCore.pyqtSignal()
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        while True:
            self.update_info.emit()
            time.sleep(2)



if __name__ == '__main__':

    app = QApplication(sys.argv)

    info_bat = Window()
    info_bat.show()

    sys.exit(app.exec_())



