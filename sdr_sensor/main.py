import ResultLogToExcel
import DataCompare
from GetData import GetThresholdData


class MainEnter(object):
    def run(self):
        SplitString = ""
        # GetData instance
        getdata = GetThresholdData(SplitString)
        # get spec data
        spec_threshold_sensor, spec_threshold_sdr, spec_discrete_sdr = getdata.get_spec_data()
        # get ipmi data
        ipmi_threshold_sensor, SplitString = getdata.get_sensor()
        ipmi_threshold_sdr, ipmi_discrete_sdr = getdata.get_sdr()
        # print discrete_sdr

        # send threshold sdr to DataCompare.py, exec sdr/sensor data compare
        DataCompare.sdrandsensor_compare(spec_threshold_sdr,
                                         ipmi_threshold_sdr,
                                         spec_threshold_sensor,
                                         ipmi_threshold_sensor)

        print "Threshold Sensor and Discrete Sensor split string: ", SplitString

        from LoggerSdrAndSensor import logger
        logger.info("-----------------Discrete Compare-----------------")

        # send discrete sdr to DataCompare.py, exec sdr data compare
        DataCompare.sdrandsensor_compare(spec_discrete_sdr,
                                         ipmi_discrete_sdr,
                                         spec_sensor=None,
                                         ipmi_sensor=None)

        print "Start read .log file test result save to Excel..."
        ResultLogToExcel.run(ipmi_threshold_sdr, ipmi_discrete_sdr)


if __name__ == '__main__':
    mainenter = MainEnter()
    mainenter.run()


