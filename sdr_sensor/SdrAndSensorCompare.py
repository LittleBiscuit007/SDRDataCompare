import math

from logger_sdr_sensor import logger


def diff_rate(ipmi, spec):
    """
    return a diff_rate between ipmi_threshold and spec_threshold
    :return:
    """
    # print ipmi, spec, type(str(spec))
    ipmi_int = eval(ipmi)
    spec_int = eval(str(spec))
    ipmi_spec_diff_rate = math.fabs(ipmi_int-spec_int) / spec_int
    return ipmi_spec_diff_rate


def threshold_compare(ipmi_threshold_each, spec_threshold_each, sensor_name):
    """
    compare threshold
    :return:
    """
    threshold_name_list = ["LC", "LNC", "UNC", "UC"]
    for i in range(1, 5):
        if ipmi_threshold_each[i] == spec_threshold_each[i-1]:
            logger.info(sensor_name + "'s " + threshold_name_list[i-1] + " is pass.")
        elif ipmi_threshold_each[i] == "na" or spec_threshold_each[i-1] == "na":
            logger.error(sensor_name + "'s " + threshold_name_list[i-1] + " is fail.")
        else:
            ipmi_spec_diff_rate = diff_rate(ipmi_threshold_each[i], spec_threshold_each[i-1])
            if ipmi_spec_diff_rate <= 0.01:
                logger.info(sensor_name + "'s " + threshold_name_list[i-1] + " is pass.")
            else:
                logger.error(sensor_name + "'s " + threshold_name_list[i-1] + " is fail.")


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


def sdrandsensor_compare(spec_sdr, ipmi_sdr, spec_sensor, ipmi_sensor):
    """
    exec spec/ipmi sdr/sensor data compare
    :param spec_sdr: dict, key: sensor name, values: [sensor number, entity id(Dec), sensor type]
    :param ipmi_sdr: list, [sensor name/sensor number/entity id/sensor type]
    :param spec_sensor: dict, key: sensor name, values: threshold=[LC, LNC, UNC, UC], X changed to na
    :param ipmi_sensor: list, [sensor name, LC, LNC, UNC, UC]
    :return:
    """
    if len(ipmi_sdr) != len(ipmi_sensor):
        logger.error("get ipmi data error")
        return 0
    print "Start compare spec/ipmi sdr/sensor data..."
    sensor_index = 0
    # read ipmi list
    for ipmi_fru_each in ipmi_sdr:
        sensor_name = ipmi_fru_each[0]
        spec_fru_each = []
        spec_threshold_each = []
        # use sensor name get sdr values in spec
        try:
            spec_fru_each = spec_sdr[sensor_name]
            spec_threshold_each = spec_sensor[sensor_name]
        except KeyError as e:
            logger.error("spec don't have " + sensor_name + " sensor_name. \n\
                        sensor number/entity id/sensor type not compare.\n")
            continue
        else:
            logger.info(sensor_name + "'s field ( Sensor name ): pass.")

        # fru compare
        fru_compare(ipmi_fru_each, spec_fru_each, sensor_name)

        # print "len(ipmi_sdr/ipmi_sensor)", len(ipmi_sdr), len(ipmi_sensor)

        # print "Start compare spec/ipmi sensor data..."
        # compare threshold
        threshold_compare(ipmi_sensor[sensor_index], spec_threshold_each, sensor_name)


