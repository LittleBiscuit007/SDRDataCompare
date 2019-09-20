import sdr
import sensor
import conf
import openpyxl
# read spec file
#     sdr
#         dict, key: sensor name, values: [sensor number, entity id, sensor type]
#         entity id: Hex data changed to Dec data
#         send sdr to sdr.py, exec sdr data compare
#     sensor
#         dict, key: sensor name, values: threshold=[LC, LNC, UNC, UC],
#         X/None changed to na
#         send sensor data to sensor.py, exec sensor data compare


def get_spec_data():
    """
    get spec_sdr and spec_sensor info
    :return:
    """
    spec_sdr = {}
    spec_sensor = {}
    # get excel workbook
    workbook = openpyxl.load_workbook("../PF05008957_HR650X+_BMC_BMC SDR Spec_V0.01.xlsx")
    # get valid workobject
    ws = workbook.get_sheet_by_name("Threshold Sensors")
    # get Spec data object
    spec_data = ws[conf.Start_SpecFile:conf.End_SpecFile]

    for row in spec_data:
        # delete category row
        if not row[1].value:
            continue
        # dict, key: sensor name, values: [sensor number, entity id, sensor type]
        # entity id: Hex data changed to Dec data
        spec_sdr[row[1].value] = [row[0].value, eval("0x" + row[5].value[:-1]), row[3].value]
        # dict, key: sensor name, values: threshold=[LC, LNC, UNC, UC]
        # X/None changed to na
        for i in range(8, 12):
            if row[i].value == "X" or row[i].value is None:
                row[i].value = "na"
        spec_sensor[row[1].value] = [row[8].value, row[9].value, row[10].value, row[11].value]
    return spec_sensor, spec_sdr


def get_sdr():
    """
    sdr_ipmi_get
    :return:
    [[sensor name, sensor number, entity id, sensor type], ....]
    """
    # get sdr data
    sdr_list = []
    sdr_valid_list = []
    # use ipmi command get sdr, save as file
    # sdr_file = os.system("ipmitool -I lanplus -H 10.245.45.169 -U root -P 0penBmc -v sdr list > 169_sdr.txt")
    with open("../169_sdr.txt", "r") as sdr_read_file:
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
            if i == conf.SplitString:
                break
            # get sensor name/sensor number/entity id/sensor type
            if "Sensor ID" in i or "Entity ID" in i or "Sensor Type" in i:
                sdr_valid_list.append(i)
    # deal with data
    ipmi_sdr = []
    sub_ipmi_sdr = []
    count = 1
    for each_sdr in sdr_valid_list:
        each_sdr_str = [i.strip() for i in each_sdr.split(":")]
        each_sdr_str.pop(0)
        # print each_sdr_str
        sdr_value = each_sdr_str[0].split(" ", 1)
        # print sdr_value
        # append sensor name/sensor number
        if count == 1:
            sub_ipmi_sdr.append(sdr_value[0])
            if len(sdr_value[1][3:-1]) == 1:
                sensor_number = "0" + sdr_value[1][3:-1]
            sub_ipmi_sdr.append(sensor_number + "h")
        # append entity id
        if count == 2:
            sub_ipmi_sdr.append(sdr_value[0])
        # append sensor type
        if count == 3:
            # sensor type.Temperature changed to Temp
            if sdr_value[0] == "Temperature":
                sdr_value[0] = "Temp"
            # sensor type.low char changed to upper char
            sensor_type_id = sdr_value[1][3:-1]
            if sensor_type_id.islower():
                sensor_type_id = sensor_type_id.upper()

            sub_ipmi_sdr.append(sdr_value[0] + " (" + sensor_type_id + "h)")
            count = 0
            ipmi_sdr.append(sub_ipmi_sdr)
            sub_ipmi_sdr = []
        count += 1
    return ipmi_sdr


def get_sensor():
    """
    sensor_ipmi_get
    :return:
    """
    # get sensor data save as file
    # sensor_ipmi_command = "ipmitool -I lanplus -H " + conf.BMCIP + "-U " + conf.UserName +" -P " + conf.Password + \
    #                       " sensor list all  > 169_sensor.txt"
    # sensor_file = os.system(sensor_ipmi_command)
    sensor_list = []
    sensor_valid_list = []
    # read sensor file get data save into list
    # [[sensor name, LC, LNC, UNC, UC], ....]
    with open("../169_sensor.txt", "r") as sensor_read_file:
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
    return sensor_valid_list


if __name__ == '__main__':
    spec_sensor, spec_sdr = get_spec_data()

    ipmi_sensor = get_sensor()
    # print 'spec_sensor: ', spec_sensor
    # print 'ipmi_sensor: ', ipmi_sensor
    # send sensor data to sensor.py, exec sensor data compare
    sensor.sensor_compare(spec_sensor, ipmi_sensor)

    ipmi_sdr = get_sdr()
    # print 'spec_sdr: ', spec_sdr
    # print 'ipmi_sdr: ', ipmi_sdr
    # send sdr to sdr.py, exec sdr data compare
    sdr.sdr_compare(spec_sdr, ipmi_sdr)


