from logger_sdr_sensor import logger


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

        # compare sensor number
        if ipmi_fru_each[1] == spec_fru_each[0]:
            logger.info(sensor_name + "'s sensor number is pass.")
        else:
            logger.error(ipmi_fru_each[1] + " and " + spec_fru_each[0] + " are different.\n\
                        " + sensor_name + "'s sensor number is fail.")

        # compare entity id
        if eval(ipmi_fru_each[2]) == spec_fru_each[1]:
            logger.info(sensor_name + "'s entity id is pass.")
        else:
            logger.error(ipmi_fru_each[2] + " and " + str(spec_fru_each[1]) + " are different.\n\
                        " + sensor_name + "'s entity id is fail.")

        # compare sensor type
        if ipmi_fru_each[3] == spec_fru_each[2]:
            logger.info(sensor_name + "'s sensor type is pass.\n")
        else:
            logger.error(ipmi_fru_each[3] + " and " + spec_fru_each[2] + " are different.\n\
                        " + sensor_name + "'s sensor type is fail.\n")


