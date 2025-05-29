import logging
import bcolors

RECORD_FORMAT = "%(asctime)s - %(levelname)s (%(filename)s:%(lineno)d) %(message)s"
RECORD_FORMAT_CONSOLE = "%(asctime)s - {color}%(levelname)s{end_color} (%(filename)s:%(lineno)d) %(message)s"

class CustomFormatter(logging.Formatter): 
    formats = {
        logging.INFO: bcolors.GREEN,
        logging.WARNING: bcolors.YELLOW,
        logging.ERROR: bcolors.RED,
        logging.CRITICAL: bcolors.MAGENTA
    }
    
    def format(self, record):
        logColor = self.formats.get(record.levelno)
        formatter = logging.Formatter(RECORD_FORMAT_CONSOLE.format(color=logColor, end_color=bcolors.ENDC))
        return formatter.format(record)

def fileHandler():
    fileHandler = logging.FileHandler(filename='.log', encoding='utf-8')
    fileHandler.setLevel(logging.INFO)
    fileHandler.setFormatter(logging.Formatter(RECORD_FORMAT, "%Y-%m-%d %H:%M:%S"))
    return fileHandler

def streamHandler():
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.INFO)
    streamHandler.setFormatter(CustomFormatter())
    return streamHandler

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(fileHandler())
    logger.addHandler(streamHandler())
    return logger