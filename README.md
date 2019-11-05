# data_compare
Compare spec/ipmi sdr_sensor data info   
Execution environment is python2
1. Modify the relevant parameters in the configuration file
2. Place the `SDR spec` file in the data_compare directory
3. Run the "main.py" file， then generate the "log_sdr_sensor.log" and "test_result.xls" files to save test result.

Note:   
   1. Record string "Sensor name, " test items in "test_result.xls", its sensor number/entity id/sensor type/threshold aren't compare.  
   2. When spec threshold has Tjmax, ipmi threshold has value then pass.  
   3. When sensor reading is "na", if threshold is also "na" then pass.  
   4. If sensor name capitalized not same(not all upper or all lower in spec), remain record test result as "Fail".


