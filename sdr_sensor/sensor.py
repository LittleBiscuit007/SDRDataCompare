# spec
#     dict, key: sensor name, values: threshold=[LC, LNC, UNC, UC], X changed to na
# ipmi
#     list, [sensor name, LC, LNC, UNC, UC]
# data compare
#     read ipmi list
#     use ipmi.sensor name get values in spec
#     compare LC
#     compare LNC
#     compare UNC
#     compare UC


def sensor_compare(spec_sensor, ipmi_sensor):
    pass

