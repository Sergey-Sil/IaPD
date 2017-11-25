import os


class DeviceFinder:


    def get_usb_table(self):
        usb_set = self.get_device_list_by_path()
        block_device_list = self.get_device_list_by_label()

        usb_set = sorted(usb_set)
        usb_table = []
        for device in usb_set:
            for element in block_device_list:
                if device == element[0]:
                    usb_table.append(element)
                    break
        usb_table = self.find_dev_mount_point(usb_table)
        return usb_table

    def find_dev_mount_point(self, usb_table):
        mounts = open("/proc/mounts")
        mount_lines = mounts.readlines()
        table = usb_table
        for i, device in enumerate(table):
            for line in mount_lines:
                arguments = line.split(" ")
                if arguments[0] == device[0]:
                    usb_table[i].append(arguments[1])
                    usb_table[i] = self.get_drive_stat(usb_table[i])
                    break
        return usb_table

    def get_drive_stat(self, table_row):
        statvfs = os.statvfs(table_row[2])
        bytes_in_gigabytes = 10 ** 9
        total = statvfs.f_frsize * statvfs.f_blocks / bytes_in_gigabytes
        free = statvfs.f_frsize * statvfs.f_bavail / bytes_in_gigabytes
        used = total - free
        for item in [total, free, used]:
            table_row.append(str("%.2f" % item + " GiB"))
        return table_row

    def get_device_list_by_label(self):
        by_label_dir = "/dev/disk/by-id/"
        block_devices = os.listdir(by_label_dir)
        block_device_list = []
        for device in block_devices:
            block_device_list.append([os.path.abspath(by_label_dir + os.readlink(by_label_dir + device)),
                                      device])
        return block_device_list

    def get_device_list_by_path(self):
        by_path_dir = "/dev/disk/by-path/"
        disk_list = os.listdir(by_path_dir)
        usb_set = set()
        for device in disk_list:
            if device.find("usb") != -1:
                path = os.readlink(by_path_dir + device)
                abs_path = os.path.abspath(by_path_dir + path)
                usb_set.add(abs_path)
        return usb_set

    def get_mtp_devices(self):
        f = os.popen('mtp-detect')
        output_lines = f.readlines()
        mtp_list = []
        first_storage_flag = False
        device = []
        bytes_in_gigabytes = 10 ** 9
        total = 0
        for line in output_lines:
            if line.find("Manufacturer") != -1:
                device.clear()
                device.append(" ".join(line.split()[1:]))
                first_storage_flag = False
            if line.find("Model") != -1:
                device.append(" ".join(line.split()[1:]))
            if line.find("MaxCapacity") != -1:
                total = float(line.split()[1]) / bytes_in_gigabytes
                device.append("%.2f" % total + " G")
            if line.find("FreeSpaceInBytes") != -1:
                free = float(line.split()[1]) / bytes_in_gigabytes
                device.append("%.2f" % free + " G")
                device.append("%.2f" % (total - free) + " G")
            if line.find("StorageDescription") != -1:
                if not first_storage_flag:
                    device.append(" ".join(line.split()[1:]))
                    first_storage_flag = True
                    mtp_list.append(device.copy())
        return mtp_list
