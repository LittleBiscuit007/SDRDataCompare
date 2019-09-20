from logger_sdr_sensor import logger
import math


def diff_rate(ipmi, spec):
    """
    return a diff_rate between ipmi_threshold and spec_threshold
    :return:
    """
    ipmi_int = eval(ipmi)
    spec_int = eval(spec)
    ipmi_spec_diff_rate = math.fabs(ipmi_int-spec_int) / spec_int
    return ipmi_spec_diff_rate


def threshold_compare():
    pass


def sensor_compare(spec_sensor, ipmi_sensor):
    """
    exec spec/ipmi sensor data compare
    :param spec_sensor: dict, key: sensor name, values: threshold=[LC, LNC, UNC, UC], X changed to na
    :param ipmi_sensor: list, [sensor name, LC, LNC, UNC, UC]
    :return:
    """
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
        # compare LC
        if ipmi_threshold_each[1] == spec_threshold_each[0]:
            logger.info(sensor_name + "'s " + "LC is pass.")
        else:
            ipmi_spec_diff_rate = diff_rate(ipmi_threshold_each[1], spec_threshold_each[0])
            if ipmi_spec_diff_rate <= 0.01:
                logger.info(sensor_name + "'s " + "LC is pass.")
            else:
                logger.error(sensor_name + "'s " + "LC is fail.")
        # compare LNC
        if ipmi_threshold_each[2] == spec_threshold_each[1]:
            logger.info(sensor_name + "'s " + "LNC is pass.")
        else:
            ipmi_spec_diff_rate = diff_rate(ipmi_threshold_each[2], spec_threshold_each[1])
            if ipmi_spec_diff_rate <= 0.01:
                logger.info(sensor_name + "'s " + "LNC is pass.")
            else:
                logger.error(sensor_name + "'s " + "LNC is fail.")
        # compare UNC
        if ipmi_threshold_each[3] == spec_threshold_each[2]:
            logger.info(sensor_name + "'s " + "UC is pass.")
        else:
            ipmi_spec_diff_rate = diff_rate(ipmi_threshold_each[3], spec_threshold_each[2])
            if ipmi_spec_diff_rate <= 0.01:
                logger.info(sensor_name + "'s " + "UC is pass.")
            else:
                logger.error(sensor_name + "'s " + "UC is fail.")
        # compare UC
        if ipmi_threshold_each[4] == spec_threshold_each[3]:
            logger.info(sensor_name + "'s " + "UNC is pass.\n")
        else:
            ipmi_spec_diff_rate = diff_rate(ipmi_threshold_each[4], spec_threshold_each[3])
            if ipmi_spec_diff_rate <= 0.01:
                logger.info(sensor_name + "'s " + "UNC is pass.\n")
            else:
                logger.error(sensor_name + "'s " + "UNC is fail.\n")

