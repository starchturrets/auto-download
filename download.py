import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import login
import glob


def main():
    print('Downloading teh files!!!')

    options = webdriver.ChromeOptions()
    prefs = {
        'download.default_directory': '/home/james/programming/python-fun/files'}
    options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(
        executable_path="chromedriver", port=0, options=options)

    url = 'https://sdpauth.sabis.net/'

    browser.get(url)

    def logged_in():
        if len(browser.find_elements_by_css_selector('.exampreparation-tile')) == 0:
            return False
        else:
            return True

    if logged_in() == False:
        login.login(browser)

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

    items = container_div[1]

    heading = items.find_element_by_css_selector('.panel-heading')

    heading = heading.get_attribute('id')

    week = heading.split('Week')[1]

    term = browser.find_element_by_css_selector(
        'div.filter.data').find_element_by_css_selector('b.ng-binding')

    term = term.text.split('Term')[1].strip()
    current = 'T' + term + 'WK' + week

    items = items.find_elements_by_css_selector('li div.col-sm-4 span')

    items = items[1::2]

    for item in items:
        browser.execute_script('arguments[0].scrollIntoView(true)', item)
        browser.implicitly_wait(10)
        item.click()
        print(item.get_attribute('innerText'))

        hm = False

        while hm == False:
            fileList = glob.glob('./files/*.crdownload')
            print(fileList)
            if(len(fileList) == 0):
                hm = True
            else:
                print('Still downloading!')
                browser.implicitly_wait(10)

    browser.close()

    return current
    # hmm = element.find_elements_by_css_selector('ul.list ')
