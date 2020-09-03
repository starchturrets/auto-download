import download
import upload
import schedule
import time
import shutil
import os
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import login
# from selenium.webdriver.common.keys import Keys


def clear_files():
    shutil.rmtree('files')

    os.makedirs('files')


def find_weeks():

    # Move the week logic here, have ./download.py only do downloading
    print('Nulll here')


def setup_browser(webdriver):
    options = webdriver.ChromeOptions()

    options.add_experimental_option('prefs',  {
        'download.default_directory': '/home/james/programming/auto-download/files'})

    browser = webdriver.Chrome(
        executable_path="chromedriver", port=0, options=options)

    return browser


def navigate_to_exams(browser):
    exam_prep_link = browser.find_element_by_css_selector(
        '.exampreparation-tile')

    url = "https://digitalplatform.sabis.net" + \
        str(exam_prep_link.get_attribute('ng-href'))

    browser.get(url)

    element = WebDriverWait(browser, 90).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[ng-class="{selected: documentsCtrl.selectCurrentTermWeek}"]')))
    element.click()

    def wait():
        browser.implicitly_wait(10)
        container_div = browser.find_elements_by_css_selector(
            'div.panel.ng-scope')

        if len(container_div) < 2:
            wait()
        else:
            print(container_div)
            return container_div

    shuld_wait = False
    container_div = browser.find_elements_by_css_selector(
        'div.panel.ng-scope')

    while shuld_wait == False:
        browser.implicitly_wait(10)
        container_div = browser.find_elements_by_css_selector(
            'div.panel.ng-scope')

        if len(container_div) > 2:
            shuld_wait = True


def main():

    clear_files()

    browser = setup_browser(webdriver)

    browser.get('https://sdpauth.sabis.net/')

    login.main(browser)

    current = download.main()
    print(current)

    upload.main(current)


if __name__ == '__main__':
    main()
    # # schedule.every(2).seconds.do(main)
    # schedule.every().day.at("00:25").do(main)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
