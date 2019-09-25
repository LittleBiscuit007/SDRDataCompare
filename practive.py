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

# asc = "b0"
# print asc.islower()
#
# if asc.islower():
#     asc = asc.upper()
#
# print asc

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


string = ""
makeup_string = "123"

string += makeup_string
print string


