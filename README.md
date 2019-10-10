# data_compare
Compare spec/ipmi sdr_sensor data info   
Execution environment is python2
1. Modify the relevant parameters in the configuration file
2. Place the `SDR spec` file in the data_compare directory
3. Run the "main.py" file and save the results in the "log_sdr_sensor.log" file.
4. Auto save test result into "test_result.xls" file.

Note:   
    1. Record string "Sensor name, " test items in "test_result.xls", its sensor number/entity id/sensor type no compare.  
    2. Need manual see whether no sensor reading but has threshold.  
    3. When spec tjreshold has Tjmax, ipmi threshold has value then pass.


