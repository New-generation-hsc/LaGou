import logging

# create logger
logger_name = 'example'
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

# create file handler
log_path = 'recruit.log'
fh = logging.FileHandler(log_path, encoding='utf-8')
fh.setLevel(logging.DEBUG)

# crate formatter
fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)

# add handler and formatter to logger
fh.setFormatter(formatter)
logger.addHandler(fh)