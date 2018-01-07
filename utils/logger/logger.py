import multiprocessing
import logging
import logging.handlers
from datetime import datetime
import sys, traceback

def loggingConfigurer():
    root = logging.getLogger()
    logFileName = "log/runlog" + datetime.now().strftime('%Y.%m.%d-%H.%M.%S')+".log"
    h = logging.handlers.RotatingFileHandler(logFileName, 'a', 10*1024*1024, 10)
    f = logging.Formatter('%(asctime)s %(name)-15s %(levelname)-8s %(message)s')
    h.setFormatter(f)
    root.addHandler(h)

def loggerInit(queue):
    h = logging.handlers.QueueHandler(queue)  # Just the one handler needed
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(logging.DEBUG)
    processName = multiprocessing.current_process().name
    logger = logging.getLogger(processName)
    return logger

def loggingProcess(queue):
    loggingConfigurer()
    while True:
        try:
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)  # No level or filter logic applied - just do it!
        except Exception:
            print("Failed to run Humidifier Process: exception={})".format(e))
            continue
