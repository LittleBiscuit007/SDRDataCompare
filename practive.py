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

ipmi = eval("50")
spec = eval("49.00")

rate = math.fabs(ipmi-spec) / spec

print rate

# if eval(ipmi) == eval(spec):
#     print "pass"


