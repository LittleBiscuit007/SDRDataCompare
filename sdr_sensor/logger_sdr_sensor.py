import logging.handlers

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

rf_handler = logging.FileHandler(filename='log_sdr_sensor.log')
rf_handler.setFormatter(logging.Formatter("%(levelname)s - %(asctime)s - %(message)s"))

logger.addHandler(rf_handler)

# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warning message')
# logger.error('error message')
# logger.critical('critical message')
