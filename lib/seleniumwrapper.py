import os
import pickle
import sys
import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from lib.logwrapper import LOG_LEVEL
from lib.logwrapper import LogWrapper
from lib.pyautoguiwrapper import MOUSE_SPEED
from lib.pyautoguiwrapper import PyAutoGuiWrapper

class SeleniumWrapper():

    #######################################
    #   constructor
    #######################################
    def __init__(self, log, conf, pag=None, path=os.getcwd()):
        # set log obj
        self.__log = log

        # set pyautogui obj
        self.__pag = pag

        # check path
        ok_flag  = self.__init_path(path)

        # init browse
        ok_flag &= self.__init_browse(conf)

        # init for cookie
        ok_flag &= self.__init_cookie()

        # init for screen shot
        ok_flag &= self.__init_screenshot()

        # exist error
        if not ok_flag:
            sys.exit(1)

    #######################################
    #   check path
    #######################################
    def __init_path(self, path=os.getcwd()):
        # check path
        if not os.path.isdir(path):
            print("not exists path")
            return False

        # set path
        self.__path = path

        return True

    # # # # # # # # # # # # # # # # # # # #
    #   General functions
    # # # # # # # # # # # # # # # # # # # #

    __DRIVER_WAIT_SECONDS = 3

    #######################################
    #   wait
    #######################################
    def __wait(self, cond=EC.presence_of_all_elements_located, option=""):
        try:
            if option:
                WebDriverWait(self.__driver, self.__DRIVER_WAIT_SECONDS).until(cond(option))
            else:
                WebDriverWait(self.__driver, self.__DRIVER_WAIT_SECONDS).until(cond)

        except:
            return False

        return True

    #######################################
    #   get element
    #######################################
    def get_element(self, name="", driver=None):
        if not name:
            self.__log.printLog(LOG_LEVEL.EEROR, "failed to setting")
            return None, False

        if not driver:
            driver = self.__driver

        funcs = [
            driver.find_element_by_id,
            driver.find_element_by_class_name,
            driver.find_element_by_link_text,
            driver.find_element_by_tag_name,
            driver.find_element_by_name,
            driver.find_element_by_xpath,
            driver.find_element_by_css_selector
        ]

        if not self.__wait():
            return None, False

        for func in funcs:
            elm = None
            try:
                elm = func(name)

            except:
                pass

            if elm:
                return elm, True

        return None, False

    #######################################
    #   get elements
    #######################################
    def get_elements(self, name="", driver=None):
        if not name:
            self.__log.printLog(LOG_LEVEL.EEROR, "failed to setting")
            return None, False

        if not driver:
            driver = self.__driver

        funcs = [
            driver.find_elements_by_id,
            driver.find_elements_by_class_name,
            driver.find_elements_by_link_text,
            driver.find_elements_by_tag_name,
            driver.find_elements_by_name,
            driver.find_elements_by_xpath,
            driver.find_elements_by_css_selector
        ]

        if not self.__wait():
            return None, False

        for func in funcs:
            elms = func(name)

            if elms:
                return elms, True

        return None, False

    #######################################
    #   get windows
    #######################################
    def switch_window(self, cmd):
        if cmd != "first" and cmd != "last" and not cmd.isdecimal():
            self.__log.printLog(LOG_LEVEL.EEROR, f"cmd is irregular:{cmd}")
            return False

        # wait for new window opened
        if not self.__wait(EC.new_window_is_opened):
            return False

        # wait for switchable to new window
        time.sleep(0.5)

        handle_array = self.__driver.window_handles

        if cmd == "first":
            self.__driver.switch_to.window(handle_array[0])

        elif cmd == "last":
            self.__driver.switch_to.window(handle_array[len(handle_array)-1])

        elif cmd.isdecimal():
            self.__driver.switch_to.window(int(cmd))

        return True

    #######################################
    #   click target
    #######################################
    def click(self, name):
        elm, ok_flg = self.get_element(name)
        if ok_flg:
            elm.click()

        return ok_flg

    #######################################
    #   input target
    #######################################
    def input(self, name, txt):
        elm, ok_flg = self.get_element(name)
        if ok_flg:
            if not txt:
                elm.clear()
            else:
                elm.send_keys(txt)

        return ok_flg

    #######################################
    #   move and click
    #######################################
    def __move_click(self, img_path, x=0, y=0, seconds=MOUSE_SPEED):
        ok_flg = self.__pag.move_click(img_path, x, y, seconds)

        return ok_flg

    # # # # # # # # # # # # # # # # # # # #
    #   cookie
    # # # # # # # # # # # # # # # # # # # #

    __COOKIE_FILE_NAME = "cookie.pkl"

    #######################################
    #   cookie setting
    #######################################
    def __init_cookie(self):
        self.__cookie_path = f"{self.__path}/{self.__COOKIE_FILE_NAME}"

        return True

    #######################################
    #   import cookie data
    #######################################
    def __import_cookie(self):
        if not self.__wait():
            return False

        # import
        if os.path.isfile(self.__cookie_path):
            with open(self.__cookie_path, "rb") as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    # expiry of "driver.get_cookies" is float
                    # but, expiry of "driver.add_cookie" is int
                    # so, round converts float to int
                    # but, edge's expiry appear error
                    # maybe edge's expiry is float?
                    if "expiry" in cookie:
                        if self.__conf["browse_type"] != "edge":
                            cookie["expiry"] = round(cookie["expiry"])

                    self.__driver.add_cookie(cookie)

        return True

    #######################################
    #   export cookie data
    #######################################
    def __export_cookie(self):
        if not self.__wait():
            return False

        # export
        with open(self.__cookie_path, "wb") as f:
            pickle.dump(self.__driver.get_cookies() , f)

        return True

    # # # # # # # # # # # # # # # # # # # #
    #   screen shot
    # # # # # # # # # # # # # # # # # # # #

    __SCREEN_SHOT_DIGITS = 4
    __SCREEN_SHOT_MAX = 10 ** __SCREEN_SHOT_DIGITS

    #######################################
    #   screen shot setting
    #######################################
    def __init_screenshot(self):
        self.__screen_shot_count = 0

        return True

    #######################################
    #   make screen shot
    #######################################
    def make_screenshot(self):
        start = self.__screen_shot_count

        for n in range(start, self.__SCREEN_SHOT_MAX):
            # 0 fill to left
            cnt_zfill = str(n).zfill(self.__SCREEN_SHOT_DIGITS)
            screenshot_path = f"{self.__path}/{cnt_zfill}.png"

            # if exist file, counter increments to end
            if not os.path.isfile(screenshot_path):
                time.sleep(0.5)
                self.__driver.save_screenshot(screenshot_path)
                self.__screen_shot_count = n + 1
                break

        return True

    # # # # # # # # # # # # # # # # # # # #
    #   General functions
    # # # # # # # # # # # # # # # # # # # #

    #######################################
    #   open url
    #######################################
    def access(self, url):
        # open
        self.__driver.get(url)

        # avoid ssl
        ok_flg  = self.avoid_security_check()

        # import cookie
        ok_flg &= self.__import_cookie()

        return ok_flg

    #######################################
    #   close browse
    #######################################
    def close(self):
        # export cookie
        ok_flg = self.__export_cookie()
        # close
        self.__driver.quit()
        return ok_flg

    # # # # # # # # # # # # # # # # # # # #
    #   Browser specific
    # # # # # # # # # # # # # # # # # # # #

    #######################################
    #   browse setting
    #######################################
    def __init_browse(self, conf):
        # init
        if "browse_type" not in conf:
            conf["browse_type"] = "chrome"

        if "headless" not in conf:
            conf["headless"] = False

        if "profile_path" not in conf:
            conf["profile_path"] = ""

        if "profile_user" not in conf:
            conf["profile_user"] = ""

        # save
        self.__conf = conf

        # chrome
        if conf["browse_type"] == "chrome":
            # headless
            options = webdriver.ChromeOptions()
            if conf["headless"]:
                options.add_argument("--headless")

            # user profile
            if conf["profile_path"] != "" and conf["profile_user"] != "":
                # check directory
                if not os.path.isdir(conf["profile_path"]):
                    self.__log.printLog(LOG_LEVEL.EEROR, "not exists profile_path")
                    return False
                if not os.path.isfile(conf["profile_path"] + conf["profile_user"]):
                    self.__log.printLog(LOG_LEVEL.EEROR, "not exists profile_user")
                    return False

                options.add_argument("--user-data-dir=" + conf["profile_path"])
                options.add_argument("--profile-directory=" + conf["profile_user"])

            self.__driver = webdriver.Chrome(chrome_options=options)

        # firefox
        elif conf["browse_type"] == "firefox":
            # headless
            options = webdriver.FirefoxOptions()
            if conf["headless"]:
                options.add_argument("--headless")

            # user profile
            if conf["profile_path"] != "":
                # check directory
                if not os.path.isdir(conf["profile_path"]):
                    self.__log.printLog(LOG_LEVEL.EEROR, "not exists profile_path")
                    return False

                profile = webdriver.FirefoxProfile(conf["profile_path"])

            self.__driver = webdriver.Firefox(firefox_options=options, firefox_profile=profile)

        # ie
        elif conf["browse_type"] == "ie":
            # headless
            if conf["headless"]:
                self.__log.printLog(LOG_LEVEL.EEROR, "ie can't use headless")
                return False

            # user profile
            if conf["profile_path"] != "" or conf["profile_user"] != "":
                self.__log.printLog(LOG_LEVEL.EEROR, "ie can't use user profile")
                return False

            self.__driver = webdriver.Ie()

        # edge
        elif conf["browse_type"] == "edge":
            # headless
            if conf["headless"]:
                self.__log.printLog(LOG_LEVEL.EEROR, "edge can't use headless")
                return False

            # user profile
            if conf["profile_path"] != "" or conf["profile_user"] != "":
                self.__log.printLog(LOG_LEVEL.EEROR, "edge can't use user profile")
                return False

            self.__driver = webdriver.Edge()

        # other
        else:
            self.__log.printLog(LOG_LEVEL.EEROR, "browse type is irregular:{conf['browse_type']}")
            return False

        return True

    #######################################
    #   avoid security check
    #######################################
    def avoid_security_check(self):
        ok_flg = True

        if self.__driver.title:
            # ie
            if self.__driver.title == "このサイトは安全ではありません":
                ok_flg  = self.click("moreInfoContainer")

                ok_flg &= self.click("overridelink")

                time.sleep(0.5)

            # edge
            elif self.__driver.title == "証明書エラー: ナビゲーションはブロックされました":
                ok_flg  = self.click("moreInformationDropdownSpan")

                ok_flg &= self.click("invalidcert_continue")

                time.sleep(0.5)

        return ok_flg

    #######################################
    #   post cert
    #######################################
    def post_cert(self, cmd):
        # check cmd
        if cmd != "ok" and cmd != "cancel" and not cmd.isdecimal():
            self.__log.printLog(LOG_LEVEL.EEROR, f"cmd is irregular:{cmd}")
            return False

        # browse type check is practiced
        funcs = {
            "chrome"  : self.__post_cert_chrome,
            "firefox" : self.__post_cert_firefox,
            "ie"      : self.__post_cert_ms,
            "edge"    : self.__post_cert_ms
        }
        ok_flg = funcs[self.__conf["browse_type"]](cmd)

        return ok_flg

    #######################################
    #   post cert for chrome
    #######################################
    def __post_cert_chrome(self, cmd):
        # cmd check is practiced
        if cmd == "ok":
            ok_flg = self.__move_click("img/chrome/ok.png")

        elif cmd == "cancel":
            ok_flg = self.__move_click("img/chrome/cancel.png")

        elif cmd.isdecimal():
            diff = 80 + (int(cmd) * 40)
            ok_flg  = self.__move_click("img/chrome/next.png", 0, diff)

            ok_flg &= self.__move_click("img/chrome/ok.png")

        return ok_flg

    #######################################
    #   post cert for firefox
    #######################################
    def __post_cert_firefox(self, cmd):
        # cmd check is practiced
        if cmd == "ok":
            ok_flg  = self.__move_click("img/firefox/must.png", -70)

            ok_flg &= self.__move_click("img/firefox/ok.png")

        elif cmd == "cancel":
            ok_flg  = self.__move_click("img/firefox/must.png", -70)

            ok_flg &= self.__move_click("img/firefox/cancel.png")

        elif cmd.isdecimal():
            ok_flg  = self.__move_click("img/firefox/next.png", 0, 100)

            diff = 130 + (20 * int(cmd))
            ok_flg &= self.__move_click("img/firefox/next.png", 0, diff)

            ok_flg &= self.__move_click("img/firefox/must.png", -70)

            ok_flg &= self.__move_click("img/firefox/ok.png")

        return ok_flg

    #######################################
    #   post cert for ms
    #######################################
    def __post_cert_ms(self, cmd):
        # cmd check is practiced
        if cmd == "ok":
            ok_flg  = self.__move_click("img/ms/ok.png")

        elif cmd == "cancel":
            ok_flg &= self.__move_click("img/ms/cancel.png")

        elif cmd.isdecimal():
            ok_flg  = self.__move_click("img/ms/next.png")

            diff = 60 * int(cmd)
            ok_flg &= self.__move_click("img/ms/next.png", 0, diff)

            ok_flg &= self.__move_click("img/ms/ok.png")

        return ok_flg

