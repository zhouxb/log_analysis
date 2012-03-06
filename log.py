from multiprocessing import Queue
import logging
import settings
import os
import util

global_log_queue = Queue()

class QueueLogger:
    def __init__(self, log_queue):
        self.log_queue = log_queue
    def info(self, msg):
        self.log_queue.put(("INFO", msg))
    def warning(self, msg):
        self.log_queue.put(("WARNING", msg))
    def error(self, msg):
        self.log_queue.put(("ERROR", msg))

def get_global_logger():
    return QueueLogger(global_log_queue)

@ util.ensure_directory(settings.APP_LOG_DIR)
def run_log(log_queue):

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    fh = logging.FileHandler(os.path.join(settings.APP_LOG_DIR, settings.APP_LOG_FILENAME))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    log_table = {
        "INFO"     : lambda msg: logger.info(msg),
        "WARNING"  : lambda msg: logger.warning(msg),
        "ERROR"    : lambda msg: logger.error(msg),
    }
    while True:
       level, msg = log_queue.get()
       log_table[level](msg)
