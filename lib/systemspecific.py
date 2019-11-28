import time

import concurrent.futures

from lib.logwrapper import LOG_LEVEL
from lib.logwrapper import LogWrapper
from lib.pyautoguiwrapper import MOUSE_SPEED
from lib.pyautoguiwrapper import PyAutoGuiWrapper
from lib.seleniumwrapper import SeleniumWrapper

class SystemSpecific(SeleniumWrapper):

    #######################################
    #   constructor
    #######################################
    def __init__(self, log, conf, pag, path):
        super().__init__(log, conf, pag, path)

        self.__log = log
        self.__cnt_password = 0
        self.__cnt_sso = 0

    #######################################
    #   get cmd list
    #######################################
    def get_cmd_list(self):
        __CMD_LIST = {
            # input
            "uid" : self.uid,
            "password" : self.password,
            # click
            "submit" : self.submit,
            "toggle" : self.toggle,
            "logout" : self.logout,
            # other
            "access" : self.access,
            "close" : self.close,
        }

        return __CMD_LIST

    # # # # # # # # # # # # # # # # # # # #
    #   root
    # # # # # # # # # # # # # # # # # # # #

    #######################################
    #   normal
    #######################################
    def normal(self, cmd):
        # cmd to be executed
        self.__log.printLog(LOG_LEVEL.NOCTICE, f"play {cmd}")

        # make screen shot
        if cmd != "access":
            self.make_screenshot()

        return True

    #######################################
    #   irregular
    #######################################
    def irregular(self, cmd):
        # make screen shot
        self.__log.printLog(LOG_LEVEL.WARNING, f"irregular {cmd}")

        # make screen shot
        ok_flg  = self.make_screenshot()

        # close
        ok_flg &= self.close()

        return ok_flg

    # # # # # # # # # # # # # # # # # # # #
    #   General functions
    # # # # # # # # # # # # # # # # # # # #

    #######################################
    #   open url
    #######################################
    def access(self, url):
        return super().access(url)

    #######################################
    #   close browse
    #######################################
    def close(self):
        return super().close()

    #######################################
    #   make screen shot
    #######################################
    def make_screenshot(self):
        return super().make_screenshot()

    # # # # # # # # # # # # # # # # # # # #
    #   input
    # # # # # # # # # # # # # # # # # # # #

    #######################################
    #   uid
    #######################################
    def uid(self, uid):
        ok_flg  = super().input("loginForm[username]", "")
        ok_flg &= super().input("loginForm[username]", uid)
        return ok_flg

    #######################################
    #   password
    #######################################
    def password(self, password):
        ok_flg  = super().input("loginForm[password]", "")
        ok_flg &= super().input("loginForm[password]", password)
        return ok_flg

    # # # # # # # # # # # # # # # # # # # #
    #   click
    # # # # # # # # # # # # # # # # # # # #

    #######################################
    #   toggle
    #######################################
    def toggle(self):
        ok_flg  = super().click("user-name")

        return ok_flg

    #######################################
    #   submit
    #######################################
    def submit(self):
        ok_flg  = super().click("btn-login")

        return ok_flg

    #######################################
    #   logout
    #######################################
    def logout(self):
        ok_flg = super().click("icon-power")

        return ok_flg

