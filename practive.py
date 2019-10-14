import json
import os
import math


# a = os.system("ls")
# print a
#
# print 60 == 60.00

# string = "(0x01)"
# print string[3:-1]

# hexdata = "37h"
# hexString = "0x" + hexdata[:-1]
#
# # print(hexString)
# print eval(hexString)
#
# print eval("55.0") == eval(hexString)

d = {"B_a0": 123}
asc = "b_a0"
print asc.islower()

# if asc.islower():
#     asc = asc.upper()
# print asc

print type(asc.split("_")[1:])
print "_".join([asc.split("_")[0].upper()] + asc.split("_")[1:])
if d["_".join([asc.split("_")[0].upper()] + asc.split("_")[1:])]:
    print d["_".join([asc.split("_")[0].upper()] + asc.split("_")[1:])]

# ipmi = eval("50")
# spec = eval("49.00")
#
# rate = math.fabs(ipmi-spec) / spec
#
# print rate

# if eval(ipmi) == eval(spec):
#     print "pass"


# with open("practive.txt", "r") as file:
#     while True:
#         file_data = file.readline()
#         if not file_data:
#             break
#         if file_data == "2\n":
#             print "False"
#             continue
#         if file_data == "\n":
#             print "True"
#             continue
#         if file_data == "1":
#             print "11111"
#             continue
#         print file_data
#         # print r'file_data'

# json_str = {"msg": {
#     "crc": 0,
#     "msg_body": "How are you ?",
#     "msg_len": 88,
#     "recv_id": 319371,
#     "send_id": 319371,
#     "send_time": 0,
#     "type": 96
#   },
# "msgLen":90
# }
#
# print json.dumps(json_str, indent=4)


# string = ""
# makeup_string = "123"
#
# string += makeup_string
# print string
# import conf
#
#
# def get_sdr():
#     """
#     sdr_ipmi_get
#     :return:
#     [[sensor name, sensor number, entity id, sensor type], ....]
#     """
#     print "Start get ipmi sdr data..."
#     # get sdr data
#     sdr_list = []
#     sdr_valid_list = []
#     # use ipmi command get sdr, save as file
#     # sdr_ipmi_command = "ipmitool -I lanplus -H " + conf.BMCIP + " -U " + conf.UserName + " -P " + conf.Password + \
#     #                    " -v sdr list > ../" + conf.SdrFileName
#     # os.system(sdr_ipmi_command)
#     with open(conf.SdrFileName, "r") as sdr_read_file:
#         while True:
#             data = sdr_read_file.readline()
#             # print data.__len__()
#             if data:
#                 sdr_list.append(data)
#             else:
#                 break
#         # print sdr_list
#         for i in sdr_list:
#             # delete discrete sensor
#             if SplitString in i:
#                 break
#             # get sensor name/sensor number/entity id/sensor type
#             if "Sensor ID" in i or "Entity ID" in i or "Sensor Type" in i:
#                 sdr_valid_list.append(i)
#     # deal with data
#     ipmi_sdr = []
#     sub_ipmi_sdr = []
#     # sensor name/sensor number ` entity id ` sensor type as a loop mark
#     count = 1
#     for each_sdr in sdr_valid_list:
#         each_sdr_str = [i.strip() for i in each_sdr.split(":")]
#         each_sdr_str.pop(0)
#         # print each_sdr_str
#         sdr_value = each_sdr_str[0].split(" ", 1)
#         # print sdr_value
#         # append sensor name/sensor number
#         if count == 1:
#             sub_ipmi_sdr.append(sdr_value[0])
#             if len(sdr_value[1][3:-1]) == 1:
#                 sensor_number = "0" + sdr_value[1][3:-1]
#             else:
#                 sensor_number = sdr_value[1][3:-1]
#             print sdr_value[1][3:-1], sensor_number
#             sub_ipmi_sdr.append(sensor_number.upper() + "h")
#         # append entity id
#         if count == 2:
#             sub_ipmi_sdr.append(sdr_value[0])
#         # append sensor type
#         if count == 3:
#             # sensor type.Temperature changed to Temp
#             if sdr_value[0] == "Temperature":
#                 sdr_value[0] = "Temp"
#             # sensor type.low char changed to upper char
#             sensor_type_id = sdr_value[1][3:-1]
#             if sensor_type_id.islower():
#                 sensor_type_id = sensor_type_id.upper()
#
#             sub_ipmi_sdr.append(sdr_value[0] + " (" + sensor_type_id + "h)")
#             count = 0
#             ipmi_sdr.append(sub_ipmi_sdr)
#             sub_ipmi_sdr = []
#         count += 1
#     return ipmi_sdr
#
#
# SplitString = "FAN1_Status"
#
# ipmi_sdr = get_sdr()
# for i in ipmi_sdr:
#     print i


# list1 = [1, 1, 3]
# print list1.index(1)

# list1 = [1, 1, 3]
# print type(list1[1])
#
# str(list1[1])
# print type(str(list1[1]))

#
# print 'this is a test of code path in try...except...else...finally'
# print '************************************************************'
#
#
# def exceptTest():
#     try:
#         print 'doing some work, and maybe exception will be raised'
#         # raise IndexError('index error')
#         print 'after exception raise'
#         return 0
#
#     except KeyError, e:
#         print 'in KeyError except'
#         print e
#         return 1
#     except IndexError, e:
#         print 'in IndexError except'
#         print e
#         return 2
#     except ZeroDivisionError, e:
#         print 'in ZeroDivisionError'
#         print e
#         return 3
#     else:
#         print 'no exception'
#         return 4
#     finally:
#         print 'in finally'
#         return 5
#
#
# resultCode = exceptTest()
# print resultCode



