# import subprocess
#
# p = subprocess.Popen("ls -l /root", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#
# print(p.stdout.readline())
# while True:
#     buff = p.stdout.readline()
#     print(buff)
#     if buff == '' or p.poll() != None:
#         break

import os


def exec_ipmi(data):
    ipmi = []
    for i in data:
        os.system(i)
    return ipmi


def exec_shell(data):
    pass


if __name__ == '__main__':
    ipmi = ["ipmitool raw 0x2e 0x30 0x79 0x2b 0x00 0x00 0x04 0x65 0x74 0x68 0x31",
            "ipmitool raw 0x2e 0x30 0x79 0x2b 0x00 0x01 0x04 0x65 0x74 0x68 0x31",
            "ipmitool raw 0x2e 0x30 0x79 0x2b 0x00 0x02 0x04 0x65 0x74 0x68 0x31",
            ]
    shell = ["cat /sys/class/net/eth1/statistics/rx_bytes",
             "cat /sys/class/net/eth1/statistics/rx_compressed",
             "cat /sys/class/net/eth1/statistics/rx_crc_errors",
             ]
    ipmi_value = exec_ipmi(ipmi)

