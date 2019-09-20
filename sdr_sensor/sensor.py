from logger_sdr_sensor import logger
import math


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


def sensor_compare(spec_sensor, ipmi_sensor):
    """
    exec spec/ipmi sensor data compare
    :param spec_sensor: dict, key: sensor name, values: threshold=[LC, LNC, UNC, UC], X changed to na
    :param ipmi_sensor: list, [sensor name, LC, LNC, UNC, UC]
    :return:
    """
    print "Start compare spec/ipmi sensor data..."
    # read ipmi list
    for ipmi_threshold_each in ipmi_sensor:
        # use ipmi.sensor name get values in spec
        sensor_name = ipmi_threshold_each[0]
        spec_threshold_each = []
        try:
            spec_threshold_each = spec_sensor[sensor_name]
        except KeyError as e:
            logger.error("spec don't have " + sensor_name + " sensor_name. \n\
                        sensor Threshold not compare.\n")
            continue
        else:
            logger.info(sensor_name + "'s field ( Sensor name ): pass.")

        # compare threshold
        threshold_compare(ipmi_threshold_each, spec_threshold_each, sensor_name)

