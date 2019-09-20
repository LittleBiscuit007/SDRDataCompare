from logger_sdr_sensor import logger


def fru_compare(ipmi_fru_each, spec_fru_each, sensor_name):
    """
    exec sensor number/entity id/sensor type compare
    :return:
    """
    fru_name_list = ["sensor number", "entity id", "sensor type"]
    for i in range(1, 4):
        if i == 2:
            ipmi_fru_each[i] = eval(ipmi_fru_each[i])
        if ipmi_fru_each[i] == spec_fru_each[i-1]:
            logger.info(sensor_name + "'s " + str(fru_name_list[i-1]) + " is pass.")
        else:
            # print i, ipmi_fru_each[i], spec_fru_each[i-1], sensor_name, type(ipmi_fru_each[i]), \
            #     type(spec_fru_each[i-1])
            logger.error(str(ipmi_fru_each[i]) + " and " + str(spec_fru_each[i-1]) + " are different.\n\
                                " + sensor_name + "'s " + fru_name_list[i-1] + " is fail.")


def sdr_compare(spec_sdr, ipmi_sdr):
    """
    exec spec/ipmi sdr data compare
    :param spec_sdr: dict, key: sensor name, values: [sensor number, entity id(Dec), sensor type]
    :param ipmi_sdr: list, [sensor name/sensor number/entity id/sensor type]
    :return:
    """
    print "Start compare spec/ipmi sdr data..."
    # read ipmi list
    logger.info("=" * 50)
    for ipmi_fru_each in ipmi_sdr:
        sensor_name = ipmi_fru_each[0]
        spec_fru_each = []
        # use sensor name get sdr values in spec
        try:
            spec_fru_each = spec_sdr[sensor_name]
        except KeyError as e:
            logger.error("spec don't have " + sensor_name + " sensor_name. \n\
                        sensor number/entity id/sensor type not compare.\n")
            continue
        else:
            logger.info(sensor_name + "'s field ( Sensor name ): pass.")
        # fru compare
        fru_compare(ipmi_fru_each, spec_fru_each, sensor_name)


