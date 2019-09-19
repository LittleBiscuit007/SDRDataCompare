import os


# a = os.system("ls")
# print a
#
# print 60 == 60.00

# string = "(0x01)"
# print string[3:-1]

hexdata = "37h"
hexString = "0x" + hexdata[:-1]

# print(hexString)
print eval(hexString)
