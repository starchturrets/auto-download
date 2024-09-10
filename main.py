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
#from modules.upload import upload
#from modules.upload import list_all_files
from modules.get_stuff import get_weeks
from modules.get_stuff import get_grid
from webdriver_manager.chrome import ChromeDriverManager
#from modules.better_quiz_grabber import better_quiz_grabber
# from selenium.webdriver.common.keys import Keys
# from modules.submit_all_quizzes import submit_all_quizzes
#from modules.upload import move_items_to_proper_folders

#from submit_all_quizzes import submit_all_quizzes


def get_credentials():
    with open('./webschool_credentials.json') as file:
        credentials = json.loads(file.read())["credentials_prod"]
        print(credentials)
        return credentials


def clear_files():
    shutil.rmtree('files')

    os.makedirs('files')


def click_pdf_links(browser, items, all_files):
    arr = []
    browser.execute_script(
        'let bar=document.querySelector("div.no-print.cookie-bar");if(bar){bar.remove()}')
    for item in items:

        browser.execute_script('arguments[0].scrollIntoView(true)', item)
        browser.implicitly_wait(10)

        text = item.get_attribute('innerText')

        text = text.split('.pdf')

        color = item.value_of_css_property('color')
        # print(color)
        # 2122 Course Revision Questions History Level N (2yr course) - AK.pdf is a pdf!
# 2122 Course Revision Questions History Level N (2yr course).pdf is a pdf!
# 2122 Level NS Core Physics - Course Revision Questions Electricity -Solution.pdf is a pdf!

# 2122 Level NS Core Physics - Course Revision Questions Electricity.pdf is a pdf!
# 2122 Level NS Core Physics Course Revision Questions Kinematics and Mechanics Solution.pdf is a pdf!

        # print(color == 'rgb(0, 128, 187)')
        bool_thing = (color == 'rgba(0, 128, 187, 1)')
        # Temporary override
        bool_thing = True
        if len(text) > 1 and bool_thing == True:
            # rgb(0, 128, 187)

            # item = item.find_element_by_css_selector('span.ng-binding')
            if "".join(item.get_attribute('innerText').split('.pdf')[0].split()) not in all_files:
                print(item.get_attribute('innerText').split(
                    '.pdf')[0] + ' is a pdf!')
                item.click()
                all_files.append("".join(item.get_attribute(
                    'innerText').split('.pdf')[0].split()))
    hm = False

    while hm == False:
        def fileList():
            return glob.glob('/home/james/programming/auto-download/files/*.crdownload')

        if(len(fileList()) == 0):
            hm = True
        else:
            browser.implicitly_wait(30)
    return all_files


def main(username, password, all_files):

    clear_files()
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver = webdriver.Chrome('/usr/local/share/chromedriver~')
    # driver = webdriver.Chrome()
    browser = setup_browser()

    browser.get('https://sdpauth.sabis.net/')

    login(browser, username, password)

    browser.get(
        'https://digitalplatform.sabis.net/Pages/ExamPreparation/ExamPreparation?a=&scid=q7x6PiPCfek%3D')

    term = 2
    weeks = get_weeks(browser)

    print('It is term: {term}'.format(term=term))

    for week in weeks:
        heading = week.find_element_by_css_selector('.panel-heading').text
        print(heading)
        items = week.find_elements_by_css_selector('li div.col-sm-4 span')
        items = items[1::2]

        all_files = click_pdf_links(browser, items, all_files)
        # Once all items in a week have been downloaded, upload
        hm = False

        while hm == False:
            browser.implicitly_wait(10)
            time.sleep(5)

            def fileList():
                return glob.glob('./files/*.crdownload')
            print(len(fileList()))
            if(len(fileList()) == 0):
                hm = True
            else:
                time.sleep(5)
                browser.implicitly_wait(10)
        upload(term, heading)

    browser.implicitly_wait(90)
    grid_items = get_grid(browser, term)
    all_files = click_pdf_links(browser, grid_items, all_files)
    browser.implicitly_wait(90)

 #   upload(term, 'Grid')

    browser.close()
    return all_files


if __name__ == '__main__':
    # def do():
    #     try:
    #         credentials = get_credentials()
    #         all_files = list_all_files(2)
    #         for file in all_files:
    #             print(file)

    #         for credential in credentials:
    #             username = credential["username"]
    #             password = credential["password"]
    #             account_id = credential["account_id"]
    #             # [username, password, account_id] = credential
    #             print(username)
    #             # submit_all_quizzes(username, password)
    #             all_files = main(username, password, all_files)
    #             all_files = better_quiz_grabber(
    #                 username, password, account_id, all_files)
    #             move_items_to_proper_folders(2)

    #             # schedule.every(5).minutes.do(main)
    #             # while True:
    #             #     schedule.run_pending()
    #             #     time.sleep(1)
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
    #   all_files = list_all_files(2)
#    os.system(
#        'xdg-user-dirs-update --set DOWNLOAD /home/james/programming/auto-download/files')
    # for credential in credentials:
    #     username = credential["username"]
    #     password = credential["password"]
    #     submit_all_quizzes(username, password)
    for credential in credentials:
        username = credential["username"]
        password = credential["password"]
        account_id = credential["account_id"]
        # [username, password, account_id] = credential
        print(username)
        all_files = main(username, password, all_files)
        all_files = better_quiz_grabber(
            username, password, account_id, all_files)
        move_items_to_proper_folders(2)

#   os.system('xdg-user-dirs-update --set DOWNLOAD /home/james/Downloads')
