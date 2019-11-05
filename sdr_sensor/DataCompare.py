import math

from LoggerSdrAndSensor import logger


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


def na_threshold_compare(ipmi_threshold_each, threshold_name_list, sensor_name):
    """
    when sensor reading is na, compare LC/LNC/UNC/UC whether is na
    :return:
    """
    for i in range(1, 5):
        if ipmi_threshold_each[i] == "na":
            logger.info(sensor_name + "'s " + threshold_name_list[i-1] + " is pass.")
        else:
            logger.error(sensor_name + "'s sensor reading is 'na', but " + threshold_name_list[i-1] + " is not 'na'.")


def threshold_compare(ipmi_threshold_each, spec_threshold_each, sensor_name):
    """
    compare threshold
    ipmi_threshold_each: [sensor_name, LC, LNC, UNC, UC, sensor reading]
    spec_threshold_each: [LC, LNC, UNC, UC]
    :return:
    """
    threshold_name_list = ["LC", "LNC", "UNC", "UC"]

    # judge whether sensor has reading
    if ipmi_threshold_each[-1] == "na":
        na_threshold_compare(ipmi_threshold_each, threshold_name_list, sensor_name)
        return

    for i in range(1, 5):
        # if spec_threshold_each has "Tjmax" string, once threshold has value, then record log -- pass
        if "Tjmax" in str(spec_threshold_each[i-1]):
            if ipmi_threshold_each[i] != "na":
                logger.info(sensor_name + "'s " + threshold_name_list[i-1] + " is pass.")
                continue
            else:
                logger.error(ipmi_threshold_each[i] + " and " + str(spec_threshold_each[i-1]) + " are different. \
                            " + sensor_name + "'s " + threshold_name_list[i-1] + " is fail.")
                continue

        if ipmi_threshold_each[i] == spec_threshold_each[i-1]:
            logger.info(sensor_name + "'s " + threshold_name_list[i-1] + " is pass.")
        elif ipmi_threshold_each[i] == "na" or spec_threshold_each[i-1] == "na":
            # print type(ipmi_threshold_each[i]), type(spec_threshold_each[i-1])
            logger.error(ipmi_threshold_each[i] + " and " + str(spec_threshold_each[i-1]) + " are different. \
                         " + sensor_name + "'s " + threshold_name_list[i-1] + " is fail.")
        else:
            ipmi_spec_diff_rate = diff_rate(ipmi_threshold_each[i], spec_threshold_each[i-1])
            if ipmi_spec_diff_rate <= 0.01:
                logger.info(sensor_name + "'s " + threshold_name_list[i-1] + " is pass.")
            else:
                logger.error(ipmi_threshold_each[i] + " and " + str(spec_threshold_each[i-1]) + " are different. \
                            " + sensor_name + "'s " + threshold_name_list[i-1] + " is fail.")


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
            logger.error(str(ipmi_fru_each[i]) + " and " + str(spec_fru_each[i-1]) + " are different.\
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
    if spec_sensor and ipmi_sensor:
        if len(ipmi_sdr) != len(ipmi_sensor):
            print "get ipmi sdr/sensor data info error"
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
            if spec_sensor and ipmi_sensor:
                spec_threshold_each = spec_sensor[sensor_name]
        except KeyError as e:
            try:
                # judge sensor name whether only because capitalized not same (all upper or all lower in spec)
                if spec_sdr[sensor_name.upper()] or spec_sdr[sensor_name.lower()]:
                    logger.warning(sensor_name + "'s field ( Sensor name ): warning.")
                    fru_compare(ipmi_fru_each, spec_fru_each, sensor_name)
                    if spec_sensor and ipmi_sensor:
                        threshold_compare(ipmi_sensor[sensor_index], spec_threshold_each, sensor_name)
                        sensor_index += 1
            except KeyError:
                logger.error("spec don't have " + sensor_name + " sensor_name. \n\
                        sensor number/entity id/sensor type/threshold not compare.\n")
            continue
        else:
            logger.info(sensor_name + "'s field ( Sensor name ): pass.")

        # fru compare
        fru_compare(ipmi_fru_each, spec_fru_each, sensor_name)

        if spec_sensor and ipmi_sensor:
            # compare threshold
            threshold_compare(ipmi_sensor[sensor_index], spec_threshold_each, sensor_name)
            sensor_index += 1


