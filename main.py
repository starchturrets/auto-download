import schedule
import time
import shutil
import os
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


from modules.setup_browser import setup_browser
from modules.login import login
from modules.download import download
from modules.upload import upload
# from selenium.webdriver.common.keys import Keys


def clear_files():
    shutil.rmtree('files')

    os.makedirs('files')


def main():

    clear_files()

    browser = setup_browser(webdriver)

    browser.get('https://sdpauth.sabis.net/')

    login(browser)

    # current = download.main()
    # print(current)

    # upload.main(current)


if __name__ == '__main__':
    main()
    # # schedule.every(2).seconds.do(main)
    # schedule.every().day.at("00:25").do(main)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
