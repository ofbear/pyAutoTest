import argparse
import glob
import json
import os
import sys

from lib.logwrapper import LOG_LEVEL
from lib.logwrapper import LogWrapper
from lib.pyautoguiwrapper import MOUSE_SPEED
from lib.pyautoguiwrapper import PyAutoGuiWrapper
from lib.seleniumwrapper import SeleniumWrapper
from lib.systemspecific import SystemSpecific

class PyAutoTest():

    #######################################
    #   constructor
    #######################################
    def __init__(self, scenario_dir, result_dir):
        if not os.path.isdir(scenario_dir):
            print("scenario dir doesn't exist")
            sys.exit(1)

        if not os.path.isdir(result_dir):
            print("result dir doesn't exist")
            sys.exit(1)

        self.__scenario_dir = scenario_dir

        self.__result_dir   = result_dir

    #######################################
    #   main
    #######################################
    def main(self):
        # search scenario files from scenario dir
        scenario_files = glob.glob(f"{self.__scenario_dir}/**/*.json", recursive = True)
        for scenario_file in scenario_files:
            # set point
            start = len(self.__scenario_dir)+1
            end = len(scenario_file) - len('.json')

            # make result dir
            result_dir = f"{self.__result_dir}/{scenario_file[start:end]}"
            os.makedirs(result_dir, exist_ok=True)

            self.__play(scenario_file, result_dir)

    #######################################
    #   play scenario
    #######################################
    def __play(self, scenario_file, result_dir):
        # get scenario conf
        with open(scenario_file, "r", encoding="utf-8") as f:
            conf = json.load(f)

        # make instance
        log = LogWrapper(result_dir)
        pag = PyAutoGuiWrapper(log)
        ss = SystemSpecific(log, conf["BROWSE_CONF"], pag, result_dir)
        cmd_list = ss.get_cmd_list()

        for cmd in conf["CMDS"]:
            ss.normal(cmd)

            if cmd in cmd_list:
                if cmd in conf["PARAMETERS"]:
                    arg = conf["PARAMETERS"][cmd]
                    ok_flg = cmd_list[cmd](arg)

                else:
                    ok_flg = cmd_list[cmd]()

                if not ok_flg:
                    # irregular root
                    ss.irregular(cmd)
                    return False

        return True
