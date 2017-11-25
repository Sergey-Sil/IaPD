from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QAbstractItemView, QVBoxLayout
from PyQt5.QtWidgets import QWidget, QLabel, QTextBrowser, QTableWidget, QGridLayout, QTableWidgetItem, QPushButton
from device_finder import DeviceFinder
from PyQt5.Qt import Qt
import os


class DeviceManager(QWidget):


    usb_table = []
    table_update_interval = 1000
    dev_finder = DeviceFinder()

    def __init__(self, parent=None):
        super(DeviceManager, self).__init__(parent)

        block_device_table_label = QLabel("Block devices:")
        mtp_device_table_label = QLabel("MTP devices:")

        self.unmount_button = QPushButton("Unmount selected drives")
        self.reload_mtp_list_button = QPushButton("Reload MTP list")

        self.block_device_table_widget = QTableWidget()
        self.mtp_device_table_widget = QTableWidget()
        self.block_header = ["Device", "Label", "Mount point", "Total", "Free", "Used"]
        self.mtp_header = ["Manufacturer", "Model", "Total", "Free", "Used", "Storage Description"]

        self.table_view_setup(self.block_device_table_widget, self.block_header)
        self.table_view_setup(self.mtp_device_table_widget, self.mtp_header)

        self.grid_layout_init(block_device_table_label, mtp_device_table_label)
        self.setWindowTitle("USB Manager")

        self.usb_table = self.dev_finder.get_usb_table()
        self.update_table_widget(self.usb_table)
        self.reload_device_table()

        self.unmount_button.pressed.connect(self.unmount_button_handler)
        self.reload_mtp_list_button.pressed.connect(self.reload_mtp_list_button_handler)

    def table_view_setup(self, table_widget, header):
        table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table_widget.setColumnCount(len(header))
        table_widget.setHorizontalHeaderLabels(header)
        table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def reload_mtp_list_button_handler(self):
        mtp_list = self.dev_finder.get_mtp_devices()
        self.mtp_device_table_widget.clear()
        self.mtp_device_table_widget.setHorizontalHeaderLabels(self.mtp_header)
        self.mtp_device_table_widget.setRowCount(len(mtp_list))
        for i, device in enumerate(mtp_list):
            for j, field in enumerate(device):
                self.mtp_device_table_widget.setItem(i, j, QTableWidgetItem(field))

    def grid_layout_init(self, block_device_table_label, mtp_device_table_label):
        grid_layout = QGridLayout()
        grid_layout.addWidget(block_device_table_label, 0, 0, Qt.AlignCenter)
        grid_layout.addWidget(mtp_device_table_label, 0, 1, Qt.AlignCenter)
        grid_layout.addWidget(self.block_device_table_widget, 1, 0)
        grid_layout.addWidget(self.mtp_device_table_widget, 1, 1)
        grid_layout.addWidget(self.unmount_button, 2, 0)
        grid_layout.addWidget(self.reload_mtp_list_button, 2, 1)
        self.setLayout(grid_layout)

    def unmount_button_handler(self):
        """Unmount selected devices if they are not busy"""
        selected_fields = self.block_device_table_widget.selectedItems()
        for item in selected_fields:
            for device in self.usb_table:
                if item.text() == device[0] and len(device) > 2:
                    res = os.system("umount " + device[2])
        self.usb_table = self.dev_finder.get_usb_table()
        self.update_table_widget(self.usb_table)

    def reload_device_table(self):
        """Gather info about connected devices"""
        new_usb_table = self.dev_finder.get_usb_table()
        usb_table =[]
        for i in new_usb_table:
        	if len(i) > 2:
        		usb_table.append(i)
        new_usb_table =  usb_table
        if self.usb_table != new_usb_table:
            self.update_table_widget(new_usb_table)
            self.usb_table = new_usb_table
        QTimer.singleShot(self.table_update_interval, self.reload_device_table)

    def update_table_widget(self, new_usb_table):
        """Update connected devices table"""
        self.block_device_table_widget.clear()
        self.block_device_table_widget.setHorizontalHeaderLabels(self.block_header)
        self.block_device_table_widget.setRowCount(len(new_usb_table))
       
        for i, device in enumerate(new_usb_table):
            for j, field in enumerate(device):
                self.block_device_table_widget.setItem(i, j, QTableWidgetItem(field))
