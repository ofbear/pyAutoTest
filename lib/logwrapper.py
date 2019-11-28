import datetime
from enum import Enum
import inspect
import os
import sys

#######################################
#   define
#######################################

class LOG_LEVEL(Enum):
    EEROR = 0
    WARNING = 1
    NOCTICE = 2

class LogWrapper():
    __LOG_LEVEL_STR = {
        LOG_LEVEL.EEROR   : "EEROR  ",
        LOG_LEVEL.WARNING : "WARNING",
        LOG_LEVEL.NOCTICE : "NOCTICE"
    }


    #######################################
    #   constructor
    #######################################
    def __init__(self, path=os.getcwd()):
        self.__log_file = f"{path}/result.log"

    #######################################
    #   log
    #######################################
    def printLog(self, level=LOG_LEVEL.NOCTICE, message=""):
        # make format text
        now = datetime.datetime.now()
        level_str = self.__LOG_LEVEL_STR[level]
        func_name = inspect.stack()[1][3]
        txt = f"{now}:{level_str}:{func_name}:{message}\n"

        # write log file
        with open(self.__log_file, "a") as log_file:
            log_file.write(txt)

        # write console
        print(txt)