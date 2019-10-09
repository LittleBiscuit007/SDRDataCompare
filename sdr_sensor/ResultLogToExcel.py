import os
import conf
import xlwt


def write_excel(ipmi_sdr, excel_result_list):
    """
    save test result into excel file, and set specify color to cell
    :param ipmi_sdr:
    :param excel_result_list:
    :return:
    """
    # if test result excel exists, then remove it
    if os.path.exists("../" + conf.TestPlanName):
        os.remove("../" + conf.TestPlanName)

    # create excel workbook
    w = xlwt.Workbook(encoding="utf-8")
    # create a worksheet
    ws = w.add_sheet('Sheet1')

    # new a style object
    style_red = xlwt.easyxf('pattern: pattern solid, fore_colour red')
    style_green = xlwt.easyxf('pattern: pattern solid, fore_colour green')
    style_gold = xlwt.easyxf('pattern: pattern solid, fore_colour gold')

    # write sensor name into excel
    for row in range(len(ipmi_sdr)):
        ws.write(row, 0, ipmi_sdr[row][0])
        if excel_result_list[row] == "reading is 'na', no compare threshold":
            ws.write(row, 1, excel_result_list[row], style_gold)
        elif excel_result_list[row]:
            ws.write(row, 1, excel_result_list[row], style_red)
        else:
            ws.write(row, 1, excel_result_list[row], style_green)

    # print result_str

    # save modify file, parameter is saved file name
    w.save("../" + conf.TestPlanName)


def run(ipmi_sdr):
    """
    exec this script's main function
    read log_sdr_sensor.log file
    if first read string is "ERROR",
    every three row data as a test item result, set a skip_flag as "three loop", skip write excel
    every eight keyword save as a test item result,
    make up String data, then write specify cell into excel
    write into excel
    :return:
    """
    # read log_sdr_sensor.log file
    with open("log_sdr_sensor.log") as log_file:
        skip_flag = 0
        loop_flag = 1
        result_list = ["Sensor name, ", "sensor number, ", "entity id, ", "sensor type, ", "LC, ", "LNC, ", "UNC, ", "UC"]
        result_str = ""
        excel_result_list = []
        while True:
            log_file_data = log_file.readline()
            # read file end, exit loop
            if not log_file_data:
                break
            # if first read string is "ERROR - ",
            # every three row data as a test item result, set a skip_flag as "three loop", skip write excel
            if "spec don't have" in log_file_data:
                excel_result_list.append("Sensor name, ")
                skip_flag = 2
                continue
            # if sensor reading is "na", no compare threshold
            # every five row data as a test item result
            if "no compare threshold" in log_file_data:
                excel_result_list.append("reading is 'na', no compare threshold")
                skip_flag = 4
                continue
            if skip_flag:
                skip_flag -= 1
                continue

            # every eight keyword save as a test item result, make up String data
            if "ERROR" in log_file_data:
                result_str += result_list[loop_flag-1]
            if loop_flag == 8:
                excel_result_list.append(result_str)
                result_str = ""
                loop_flag = 0
            loop_flag += 1

        # print excel_result_list
        # write specify cell into excel
        write_excel(ipmi_sdr, excel_result_list)



