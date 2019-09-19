import json
import os

import openpyxl


def get_sensor():
    # get sensor data
    # sensor_file = os.system("ipmitool -I lanplus -H 10.245.45.169 -U root -P 0penBmc sensor list all  > 169_sensor.txt")
    sensor_list = []
    sensor_valid_list = []
    with open("169_sensor.txt", "r") as sensor_read_file:
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
            # delete field reading/units/status/lnr/unr
            for _ in range(4):
                i_list.pop(1)
                if _ == 0:
                    i_list.pop(len(i_list)-1)
            # print i_list
            sensor_valid_list.append(i_list)
        # print sensor_valid_list
    return sensor_valid_list


def get_sdr():
    # get sdr data
    sdr_list = []
    sdr_valid_list = []
    count = 0
    # sdr_file = os.system("ipmitool -I lanplus -H 10.245.45.169 -U root -P 0penBmc -v sdr list > 169_sdr.txt")
    with open("169_sdr.txt", "r") as sdr_read_file:
        while True:
            data = sdr_read_file.readline()
            # print data.__len__()
            if data:
                sdr_list.append(data)
            else:
                break
        # print sdr_list
        for i in sdr_list:
            if i == "Sensor ID              : CPU1_DIMMA1 (0x42)\n":
                break
            if "Sensor ID" in i or "Entity ID" in i or "Sensor Type" in i:
                sdr_valid_list.append(i)
    for each_sdr in sdr_valid_list:
        each_sdr_str = ":".join([i.strip() for i in each_sdr.split(":")])
        sdr_valid_list[count] = each_sdr_str
        count += 1
    # print sdr_valid_list
    return sdr_valid_list


def get_combination_data(sdr_valid_list, sensor_valid_list):
    """
        [
            {
                "Sensor ID": "P12V (0x17)",
                "Entity ID": "7.0 (System Board)",
                "Sensor Type (Threshold)": "Voltage (0x02)",
                "LNR": "na",
                "LC": "na",
                "LNC": "na",
                "UNC": "na",
                "UC": "na",
                "UNR": "na"
            },
            ...
        ]
    """
    compare_data = {}
    sdr_index = 0
    for sensor in sensor_valid_list:
        compare_data[sensor[0]] = []
        # each sensor has three sdr records
        for j in range(3):
            compare_data[sensor[0]].append(sdr_valid_list[sdr_index])
            sdr_index += 1
        compare_data[sensor[0]].append(sensor[1:])
    # compare_data = []
    # sensor_dict = {}
    # for sensor in sensor_valid_list:
    #     sensor_dict[sensor[0]] = {}
    #     sensor_dict[sensor[0]]["LNR"] = sensor[1]
    #     sensor_dict[sensor[0]]["LC"] = sensor[2]
    #     sensor_dict[sensor[0]]["LNC"] = sensor[3]
    #     sensor_dict[sensor[0]]["UNC"] = sensor[4]
    #     sensor_dict[sensor[0]]["UC"] = sensor[5]
    #     sensor_dict[sensor[0]]["UNR"] = sensor[6]

    # print compare_data
    compare_data_json = json.dumps(compare_data, indent=4)
    # print compare_data_json
    with open("combination_data.txt", "w") as f:
        f.write(compare_data_json)
    return compare_data


def shift_json():
    pass


def get_spec_data():
    # get excel workbook
    workbook = openpyxl.load_workbook("PF05008957_HR650X+_BMC_BMC SDR Spec_V0.01.xlsx")
    # get valid workobject
    ws = workbook.get_sheet_by_name("Threshold Sensors")

    spec_data = ws["A3":"M49"]

    return spec_data


def compare_id():
    pass


def compare_threshold():
    pass


if __name__ == '__main__':
    # # get sdr data
    sdr_valid_list = get_sdr()
    print 'sdr: ', sdr_valid_list
    #
    print '='*20
    # # get sensor data
    sensor_valid_list = get_sensor()
    print 'sensor: ', sensor_valid_list
    #
    # # get combination data and write file
    # compare_data = get_combination_data(sdr_valid_list, sensor_valid_list)
    # print compare_data

    # spec_data = get_spec_data()
    # spec_row_data_list = []
    # spec_data_list = []
    # for row in spec_data:
    #     for each in row:
    #         spec_row_data_list.append(str(each.value))
    #         # print each.value,
    #         print spec_row_data_list
    #     spec_data_list.append(spec_row_data_list)
    #
    # print spec_data_list

