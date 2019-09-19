# spec
#     dict, key: sensor name, values: [sensor number, entity id(Dec), sensor type]
# ipmi
#     list, [sensor name/sensor number/entity id/sensor type]


def sdr_compare(spec_sdr, ipmi_sdr):
    # read ipmi list
    for ipmi_fru_each in ipmi_sdr:
        # use sensor name get sdr values in spec
        pass
    # compare sensor number
    # compare sensor type
    # compare entity id
    pass

