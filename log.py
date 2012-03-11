import logging
import settings
import os
import util
import multiprocessing

global_log_queue = multiprocessing.Queue()

class QueueHandler(logging.Handler):
    '''
    '''
    def __init__(self, queue):
        logging.Handler.__init__(self)
        self.queue = queue
        
    def emit(self, record):
        self.queue.put(record)

def setup_logger():
    '''
    '''
    handler = QueueHandler(global_log_queue)
    handler.setLevel(settings.APP_LOG_LEVEL)

    logger = logging.getLogger()
    logger.setLevel(settings.APP_LOG_LEVEL)
    logger.addHandler(handler)

@ util.ensure_directory(settings.APP_LOG_DIR)
def run_log_listener(log_queue):
    '''
    '''
    logger = logging.getLogger()
    logger.setLevel(settings.APP_LOG_LEVEL)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    fh = logging.FileHandler(os.path.join(settings.APP_LOG_DIR, settings.APP_LOG_FILENAME))
    fh.setLevel(settings.APP_LOG_LEVEL)
    fh.setFormatter(formatter)

    sh = logging.StreamHandler()
    sh.setLevel(settings.APP_LOG_LEVEL)
    sh.setFormatter(formatter)

    # Don't remove this line
    logger.handlers = []
    logger.addHandler(sh)
    logger.addHandler(fh)

    while True:
       record = log_queue.get()
       logger.handle(record)
