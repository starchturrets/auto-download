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
from modules.get_stuff import get_weeks
from modules.get_stuff import get_grid
from webdriver_manager.chrome import ChromeDriverManager
from modules.better_quiz_grabber import better_quiz_grabber
# from selenium.webdriver.common.keys import Keys


def get_credentials():
    with open('./webschool_credentials.json') as file:
        credentials = json.loads(file.read()).credentials_test
        return credentials


def clear_files():
    shutil.rmtree('files')

    os.makedirs('files')


def click_pdf_links(browser, items):

    for item in items:

        browser.execute_script('arguments[0].scrollIntoView(true)', item)
        browser.implicitly_wait(10)

        text = item.get_attribute('innerText')

        text = text.split('.pdf')

        color = item.value_of_css_property('color')
        # print(color)
        # print(color == 'rgb(0, 128, 187)')
        bool_thing = (color == 'rgba(0, 128, 187, 1)')
        # Temporary override
        # bool_thing = True
        if len(text) > 1 and bool_thing == True:
            print(item.get_attribute('innerText') + ' is a pdf!')
            # rgb(0, 128, 187)

            item.click()
            hm = False

            while hm == False:
                def fileList():
                    return glob.glob('./files/*.crdownload')

                if(len(fileList()) == 0):
                    hm = True
                else:
                    browser.implicitly_wait(10)


def main(username, password):

    clear_files()
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver = webdriver.Chrome('/usr/local/share/chromedriver~')
    # driver = webdriver.Chrome()
    browser = setup_browser()
    # os.system(
    #     'xdg-user-dirs-update --set DOWNLOAD /home/james/programming/auto-download/files')
    browser.get('https://sdpauth.sabis.net/')

    login(browser, username, password)

    browser.get(
        'https://digitalplatform.sabis.net/Pages/ExamPreparation/ExamPreparation?a=&scid=q7x6PiPCfek%3D')

    term = 1
    weeks = get_weeks(browser)

    print('It is term: {term}'.format(term=term))

    for week in weeks:
        heading = week.find_element_by_css_selector('.panel-heading').text
        print(heading)
        items = week.find_elements_by_css_selector('li div.col-sm-4 span')
        items = items[1::2]

        click_pdf_links(browser, items)
        # Once all items in a week have been downloaded, upload
        hm = False

        while hm == False:
            browser.implicitly_wait(3)

            def fileList():
                return glob.glob('./files/*.crdownload')

            if(len(fileList()) == 0):
                hm = True
            else:
                browser.implicitly_wait(10)
        upload(term, heading)

    browser.implicitly_wait(90)
    grid_items = get_grid(browser, term)
    click_pdf_links(browser, grid_items)
    browser.implicitly_wait(90)

    upload(term, 'Grid')
    # os.system('xdg-user-dirs-update --set DOWNLOAD /home/james/Downloads')

    browser.close()


if __name__ == '__main__':
    # def do():
    #     try:
    #         credentials = get_credentials()
    #         for credential in credentials:
    #             [username ,password] = credential
    #             main(username, password)
    #             schedule.every(5).minutes.do(main)
    #             while True:
    #                 schedule.run_pending()
    #                 time.sleep(1)
    #     except:
    #         print('TIMEOUT FAILURE TRYING AGAIN')
    #         do()
    # do()
    # try:
    #     do()
    # # except selenium.common.exceptions.TimeoutException:
    # except:
    #     print('TIMEOUT FAILURE TRYING AGAIN')
    #     do()
    # print(len(glob.glob('./files/*.crdownload')))

    credentials = get_credentials()
    for credential in credentials:
        [username, password, account_id] = credential
        main(username, password)
        better_quiz_grabber(username, account_id)
