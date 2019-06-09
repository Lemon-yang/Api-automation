import  sys
import logging
from datetime import date
from logging.handlers import RotatingFileHandler
from logging import handlers
from src.read_settings import *

log_file =  LOG_FILE_PATH + "logs-" + str(date.today()) + ".log"
logging.basicConfig(filename = log_file,level=logging.DEBUG, format = '%(asctime)s %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p') 


log = logging.getLogger('')
log.setLevel(logging.INFO)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)

fh = handlers.RotatingFileHandler(log_file, maxBytes=(1048576*5), backupCount=7)
fh.setFormatter(format)
log.addHandler(fh)