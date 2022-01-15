from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
# import schedule
import os.path
import ocrmypdf
from PIL import Image
import natsort
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import shutil
import os
import glob
import selenium
# from selenium import webdriver

from modules.setup_browser import setup_browser
from modules.login import login
from modules.download import download
from modules.upload import upload
from modules.upload import get_files
from modules.get_stuff import get_weeks
from modules.get_stuff import get_grid
from webdriver_manager.chrome import ChromeDriverManager
import json


def setup_browser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    # # opt = webdriver.c
    # options: Options = webdriver.ChromeOptions()
    # # options = webdriver.opt
    # # options.add_argument(
    # #     'download.default_directory=/home/james/programming/auto-download/files')
    # # options.add_argument('--no-sandbox')
    # # options.add_argument('--headless')
    # options.add_argument('--start-fullscreen')
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # # options.add_argument('window-size=1400,200')
    # options.add_argument('--remote-debugging-port=9322')
    # options.add_argument('--hide-scrollbars')
    # # prefs = {
    # #     'download': {'default_directory': '/home/james/programming/auto-download/files', 'directory_upgrade': True}}
    # # options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(
        executable_path='/home/james/.wdm/drivers/chromedriver/linux64/97.0.4692.71/chromedriver', port=0, options=options)

    return browser


browser = setup_browser()
print(browser.title)
# function: wait for page to finish loading, then initiate submit button, then click aert
# angular.element(document.querySelector('[ng-click="onlineQuizNavigationCtrl.submitQuiz(true)"]')).scope().onlineQuizNavigationCtrl.submitQuiz(true)


def submit_btn():
    return WebDriverWait(browser, 90).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[ng-click="onlineQuizNavigationCtrl.submitQuiz(true)"]')))


# submit_btn().click()
# browser.implicitly_wait(10)
# browser.implicitly_wait(10)

# submit_btn().click()
# browser.implicitly_wait(10)

# WebDriverWait(browser, 90).until(EC.alert_is_present())
# browser.implicitly_wait(10)

# browser.switch_to.alert.accept()
