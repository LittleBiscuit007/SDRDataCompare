from __future__ import division
import os
import openpyxl

import conf


class GetThresholdData(object):
    """
    read spec file
    get ipmi sdr/sensor info
    """
    def __init__(self, SplitString):
        self.SplitString = SplitString
        # get excel workbook
        self.workbook = openpyxl.load_workbook("../" + conf.SpecFileName)

    def innsbruck(self, row, spec_sensor):
        for i in range(7, 11):
            if row[i].value == "X" or row[i].value == "x" or row[i].value is None:
                row[i].value = "na"
            if "=" in str(row[i].value):
                row[i].value = row[i].value[1:]
                # print row[i].value, row[i].value[row[i].value.index("*")+1:]
                try:
                    if "%" in row[i].value[row[i].value.index("*") + 1:]:
                        div_str = int(row[i].value[row[i].value.index("*") + 1:row[i].value.index("%")]) / 100
                        # print div_str
                        row[i].value = row[i].value[:row[i].value.index("*") + 1] + str(div_str)
                except ValueError:
                    pass
        spec_sensor[row[1].value] = [row[7].value, row[8].value, row[9].value, row[10].value]

    def hr650xplus(self, row, spec_sensor):
        for i in range(8, 11):
            if row[i].value == "X" or row[i].value is None:
                row[i].value = "na"
        spec_sensor[row[1].value] = [row[8].value, row[9].value, row[10].value, row[11].value]

    def get_spec_threshold_discrete_data(self, sheet, start, end):
        spec_sdr = {}
        spec_sensor = {}
        # get valid workobject
        ws = self.workbook.get_sheet_by_name(sheet)
        # get Spec data object
        spec_data = ws[start:end]

        for row in spec_data:
            # delete category row
            if not row[1].value:
                continue
            # dict, key: sensor name, values: [sensor number, entity id, sensor type]
            # sensor number upper
            row[0].value = row[0].value[:-1].upper() + row[0].value[-1]
            # entity id: Hex data changed to Dec data
            spec_sdr[row[1].value] = [row[0].value, eval("0x" + row[5].value[:-1]), row[3].value]

            # dict, key: sensor name, values: threshold=[LC, LNC, UNC, UC]
            # X/None changed to na
            if sheet == "Threshold Sensors":
                # Innsbruck
                self.innsbruck(row, spec_sensor)
                # 650X+
                # self.hr650xplus(row, spec_sensor)
        return spec_sensor, spec_sdr

    def get_spec_data(self):
        """
        get spec_sdr and spec_sensor info
        spec_sdr: dict, {sensor name: [sensor number, entity id, sensor type], ...}
        spec_sensor: dict, {sensor name: [LC, LNC, UNC, UC], ...}
        :return:
        """
        print "Start get spec threshold data..."

        # get spec threshold data
        spec_threshold_sensor, spec_threshold_sdr = self.get_spec_threshold_discrete_data("Threshold Sensors",
                                                                                          conf.Start_SpecFile,
                                                                                          conf.End_SpecFile)
        # get spec discrete data
        spec_discrete_sensor, spec_discrete_sdr = self.get_spec_threshold_discrete_data("Discrete Sensors",
                                                                                        conf.Start_Discrete_SpecFile,
                                                                                        conf.End_Discrete_SpecFile)
        return spec_threshold_sensor, spec_threshold_sdr, spec_discrete_sdr

    def ipmi_exec(self, parameter):
        ipmi_command = "ipmitool -I lanplus -H " + conf.BMCIP + " -U " + conf.UserName + " -P " + conf.Password + \
                           " " + parameter + " > ../" + conf.SdrFileName
        os.system(ipmi_command)

    def sdr_data_processing(self, sdr_list, IsDiscrete):
        # deal with data
        ipmi_sdr = []
        sub_ipmi_sdr = []
        count = 1
        for each_sdr in sdr_list:
            each_sdr_str = [i.strip() for i in each_sdr.split(":")]
            each_sdr_str.pop(0)
            # print each_sdr_str
            sdr_value = each_sdr_str[0].rpartition(" ")
            sdr_value = list(sdr_value)
            # print sdr_value
            # append sensor name/sensor number
            if count == 1:
                sub_ipmi_sdr.append(sdr_value[0])
                if len(sdr_value[-1][3:-1]) == 1:
                    sensor_number = "0" + sdr_value[-1][3:-1]
                else:
                    sensor_number = sdr_value[-1][3:-1]
                sub_ipmi_sdr.append(sensor_number.upper() + "h")
            # append entity id
            if count == 2:
                if not IsDiscrete:
                    sub_ipmi_sdr.append(sdr_value[0].split(" ")[0])
                else:
                    sub_ipmi_sdr.append(sdr_value[0].split(".")[0])
            # append sensor type
            if count == 3:
                # sensor type.Temperature changed to Temp
                if sdr_value[0] == "Temperature":
                    sdr_value[0] = "Temp"
                # sensor type.low char changed to upper char
                sensor_type_id = sdr_value[-1][3:-1]
                if sensor_type_id.islower():
                    sensor_type_id = sensor_type_id.upper()

                sub_ipmi_sdr.append(sdr_value[0] + " (" + sensor_type_id + "h)")
                count = 0
                ipmi_sdr.append(sub_ipmi_sdr)
                sub_ipmi_sdr = []
            count += 1
        return ipmi_sdr

    def get_sdr(self):
        """
        sdr_ipmi_get
        :return: [[sensor name, sensor number, entity id, sensor type], ....]
        """
        print "Start get ipmi sdr data..."
        # get sdr data
        sdr_list = []
        sdr_valid_list = []
        discrete_sdr = []
        IsDiscrete = 0
        # use ipmi command get sdr, save as file
        # self.ipmi_exec("-v sdr list")

        with open("../" + conf.SdrFileName, "r") as sdr_read_file:
            while True:
                data = sdr_read_file.readline()
                # print data.__len__()
                if data:
                    sdr_list.append(data)
                else:
                    break
            # print sdr_list
            for i in sdr_list:
                # delete discrete sensor
                if self.SplitString in i or "Device ID" in i:
                    IsDiscrete += 1
                # get sensor name/sensor number/entity id/sensor type
                if "Sensor ID" in i or "Entity ID" in i or "Sensor Type" in i:
                    if IsDiscrete == 0:
                        sdr_valid_list.append(i)
                    elif IsDiscrete == 1:
                        discrete_sdr.append(i)
        # discrete_sdr/sdr_valid_list:
        # ['Sensor ID              : CPU0_Status (0x91)\n',
        # ' Entity ID             : 3.1 (Processor)\n',
        # ' Sensor Type (Discrete): Processor (0x07)\n', ...]

        # ipmi threshold sdr
        ipmi_threshold_sdr = self.sdr_data_processing(sdr_valid_list, IsDiscrete=0)
        # ipmi discrete sdr
        ipmi_discrete_sdr = self.sdr_data_processing(discrete_sdr, IsDiscrete=1)
        return ipmi_threshold_sdr, ipmi_discrete_sdr

    def get_sensor(self):
        """
        sensor_ipmi_get
        :return:
        """
        print "Start get ipmi sensor data..."
        # get sensor data save as file
        # self.ipmi_exec("sensor list all")

        sensor_list = []
        sensor_valid_list = []
        # read sensor file get data save into list
        # [[sensor name, LC, LNC, UNC, UC], ....]
        with open("../" + conf.SensorFileName, "r") as sensor_read_file:
            while True:
                data = sensor_read_file.readline()
                if data:
                    sensor_list.append(data)
                else:
                    break
            # deal with data
            for i in sensor_list:
                i_list = i.split("|")
                # delete whitespace at both ends
                for j in range(len(i_list)):
                    i_list[j] = i_list[j].strip()
                # delete field units/status/lnr/unr
                for _ in range(3):
                    if _ == 0:
                        i_list.pop(len(i_list)-1)
                        # get threshold and discrete split string
                        if i_list[2] == "discrete":
                            self.SplitString = i_list[0]
                    pop_data = i_list.pop(2)

                # delete discrete sensor
                # print SplitString
                try:
                    if self.SplitString in i_list:
                        break
                except Exception:
                    pass
                # transferred sensor reading to list last
                i_list.append(i_list.pop(1))
                sensor_valid_list.append(i_list)
        return sensor_valid_list, self.SplitString

