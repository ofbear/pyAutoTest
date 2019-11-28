import argparse
import os
import sys

from configparser import ConfigParser

from lib.logwrapper import LOG_LEVEL
from lib.logwrapper import LogWrapper
from lib.pyautoguiwrapper import MOUSE_SPEED
from lib.pyautoguiwrapper import PyAutoGuiWrapper
from lib.pyautotest import PyAutoTest
from lib.seleniumwrapper import SeleniumWrapper
from lib.systemspecific import SystemSpecific

#######################################
#   parse args
#######################################

# init
parser = argparse.ArgumentParser(description="auto test tool")
parser.add_argument("-s", "--scenario_dir", help="directory for scenario files")
parser.add_argument("-r", "--result_dir", help="directory for result files")

# parse
args = parser.parse_args()

#######################################
#   get ini file
#######################################

# check ini file
if not os.path.isfile("setting.ini"):
    print("ini file doesn't exist")
    sys.exit(1)

# read ini file
config = ConfigParser()
config.read("setting.ini")

#######################################
#   set ini file
#######################################

# priority arg > ini file

if args.scenario_dir:
    scenario_dir = args.scenario_dir
else:
    scenario_dir = config.get("paths", "scenario_dir")

if args.result_dir:
    result_dir = args.result_dir
else:
    result_dir = config.get("paths", "result_dir")

#######################################
#   start
#######################################
pat = PyAutoTest(scenario_dir, result_dir)
pat.main()

