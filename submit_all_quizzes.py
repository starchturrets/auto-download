import schedule
import time
import shutil
import os
import glob
import selenium
from selenium import webdriver
import json
from modules.setup_browser import setup_browser
from modules.login import login
from modules.download import download
from modules.upload import upload
from modules.upload import list_all_files
# from get_stuff import get_weeks
from modules.get_stuff import get_grid
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def submit_all_quizzes(username, password):
    def get_weeks(browser):

        def wait_and_click(selector):
            el = WebDriverWait(browser, 900).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, selector)))
            el.click()

        wait_and_click(
            """[ng-click="documentsCtrl.filterSelection('Week');"]""")

        index = browser.find_elements_by_css_selector(
            'div.filter.data.open b.ng-binding')[0].get_attribute('innerText').split('Week')[1]

        index = int(index)

        checkboxes = browser.find_elements_by_css_selector(
            'div[ng-show="documentsCtrl.weekFilter"].row div.col-sm-10.label-filter.week-label input[name="weekCheckbox"]')
        print(len(checkboxes))
        print(index)
        # while index < len(checkboxes):

        browser.implicitly_wait(2)
        browser.execute_script('arguments[0].click()', checkboxes[index])
        # browser.implicitly_wait(30)

        # index = index + 1
        # wait_and_click('.all-week-label span')

        # weeks_length = int(len(browser.find_elements_by_css_selector(
        # 'div.week-label [ng-repeat="week in documentsCtrl.allWeeks"]'))) / 2

        container_div = browser.find_elements_by_css_selector(
            'div.panel.ng-scope')
        WebDriverWait(browser, 900).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div#loading-bar')))
        browser.implicitly_wait(20)
        shuld_wait = True
        # weeks = browser.find_elements_by_css_selector(
        #     'div.panel.ng-scope')

        # elements = browser.find_elements_by_css_selector(
        # '.panel-heading:not(.collapsed)')
        print('hmm')
        # while shuld_wait == True:
        #     print(len(elements))
        #     browser.implicitly_wait(10)

        #     if len(elements) == week:
        #         shuld_wait = False

        weeks = browser.find_elements_by_css_selector(
            'div.panel.ng-scope')

        arr = []
        # Filter out those mysterious invisible elements
        for week in weeks:
            heading = week.find_element_by_css_selector('.panel-heading').text
            if len(heading) > 0:
                arr.append(week)

        # return [arr, term]
        browser.implicitly_wait(15)
        return arr

    def submit_quiz(browser, title):
        print()

    browser = setup_browser()

    browser.get('https://sdpauth.sabis.net/')
    login(browser, username, password)

    def load_all_weeks(browser):

        browser.get(
            'https://digitalplatform.sabis.net/Pages/ExamPreparation/ExamPreparation?a=&scid=q7x6PiPCfek%3D')

        term = 2
        weeks = get_weeks(browser)
        weeks.pop(0)
        quiz_list = []
        for week in weeks:
            list_items = week.find_elements_by_css_selector(
                'li[ng-repeat="document in subject"]')
            for list_item in list_items:
                col = list_item.find_element_by_css_selector(
                    'div.col-sm-6')
                # print(col.rect['height'])
                if col.rect['height'] > 1:
                    # image = list_item.find_element_by_css_selector('img.download-quiz-icon').is_displayed()
                    # print(len(images))
                    print(col.text)
                    if 'taken' not in col.text:
                        quiz_list.append(list_item)
            print(f'length of quiz_list variable is {len(quiz_list)}')
        return quiz_list
    # load_all_weeks(browser)
    quizzes = load_all_weeks(browser)

    while len(quizzes) > 0:

        browser.execute_script(
            'arguments[0].scrollIntoView()', quizzes[0])
        div = quizzes[0].find_element_by_css_selector('div')
        div.click()
        WebDriverWait(browser, 90).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#QuizDescription')))
        browser.find_element_by_css_selector('#activeOkBtn').click()

        def confirm():
            WebDriverWait(browser, 900).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div#loading-bar')))

            button = browser.find_element_by_css_selector(
                '[ng-click="onlineQuizNavigationCtrl.submitQuiz(true)"]')
            browser.execute_script(
                'angular.element(arguments[0]).scope().onlineQuizNavigationCtrl.submitQuiz(true)', button)
            WebDriverWait(browser, 90).until(EC.alert_is_present())

            browser.switch_to.alert.accept()

        confirm()
        time.sleep(2)
        browser.implicitly_wait(15)
        confirm()
        time.sleep(2)
        browser.implicitly_wait(15)
        WebDriverWait(browser, 900).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div#loading-bar')))
        quizzes = load_all_weeks(browser)

    browser.close()

# submit_all_quizzes("Jim", "password")
