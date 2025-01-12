
# logger_config.py
import logging,datetime
from logging.handlers import TimedRotatingFileHandler

# The level here is the threshold level. If set to INFO, only INFO level and above will be written to the log file
# Log levels from lowest to highest: DEBUG < INFO < WARNING < ERROR < CRITICAL
def setup_logger(logger_name, log_file, level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Create file handler to write to log file
    #handler = logging.FileHandler(log_file, encoding='utf-8')
    
    # Generate a new log file every 8 hours and retain logs for one month
    #handler = TimedRotatingFileHandler(log_file, when="H", interval=8, backupCount=300, encoding='utf-8')

    # Generate a new log file daily and retain logs for two months
    handler = TimedRotatingFileHandler(log_file, when="midnight", backupCount=60, encoding='utf-8')
    handler.setLevel(level)

    # Create log formatter
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S') # 

    handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(stream_handler)
    
    return logger