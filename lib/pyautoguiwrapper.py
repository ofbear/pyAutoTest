import os
import time

import pyautogui

from lib.logwrapper import LOG_LEVEL
from lib.logwrapper import LogWrapper

#######################################
#   define
#######################################

MOUSE_SPEED = 0.5
WAIT_COUNTER = 30
WAIT_SECONDS = 0.1

class PyAutoGuiWrapper():

    #######################################
    #   constructor
    #######################################
    def __init__(self, log):
        self.__log = log

    #######################################
    #   search from image
    #######################################
    def __search_from_image(self, img_path):
        # check image
        if not os.path.isfile(img_path):
            self.__log.printLog(LOG_LEVEL.EEROR, "failed to setting")
            return None, False

        i = WAIT_COUNTER
        while i > 0:
            i -= 1

            # get position
            pos = pyautogui.locateCenterOnScreen(img_path)

            if pos:
                break

            time.sleep(WAIT_SECONDS)

        if not pos:
            return None, False

        return pos, True

    #######################################
    #   move & click
    #######################################
    def move_click(self, img_path, x=0, y=0, seconds=MOUSE_SPEED):
        # search from image
        pos, ok_flg = self.__search_from_image(img_path)
        if ok_flg:
            # move mouse
            pyautogui.moveTo(pos.x + x, pos.y + y, seconds)
            # click
            pyautogui.click()

        return ok_flg

    #######################################
    #   click
    #######################################
    def click(self, img_path, x=0, y=0):
        # search from image
        pos, ok_flg = self.__search_from_image(img_path)
        if ok_flg:
            # click
            pyautogui.click(pos.x + x, pos.y + y)

        return ok_flg
