import schedule
import time
import shutil
import os
import glob
import selenium
from selenium import webdriver


from modules.setup_browser import setup_browser
from modules.login import login
from modules.download import download
from modules.upload import upload
from modules.get_weeks import get_weeks
# from selenium.webdriver.common.keys import Keys


def clear_files():
    shutil.rmtree('files')

    os.makedirs('files')


def main():

    clear_files()

    browser = setup_browser(webdriver)

    browser.get('https://sdpauth.sabis.net/')

    login(browser)

    browser.get(
        'https://digitalplatform.sabis.net/Pages/ExamPreparation/ExamPreparation?a=&scid=q7x6PiPCfek%3D')

    weeks = get_weeks(browser)

    term = browser.find_element_by_css_selector(
        'div.filter.data').find_element_by_css_selector('b.ng-binding').text

    term = term.split('Term')[1].strip()

    term = int(term)

    print('It is term: {term}'.format(term=term))

    for week in weeks:
        heading = week.find_element_by_css_selector('.panel-heading').text
        print(heading)
        items = week.find_elements_by_css_selector('li div.col-sm-4 span')
        items = items[1::2]

        print(items)
        for item in items:
            browser.execute_script('arguments[0].scrollIntoView(true)', item)
            browser.implicitly_wait(10)

            text = item.get_attribute('innerText')

            text = text.split('.pdf')

            if len(text) > 1:
                print(item.get_attribute('innerText') + ' is a pdf!')
                item.click()
                hm = False

                while hm == False:
                    fileList = glob.glob('./files/*.crdownload')
                    if(len(fileList) == 0):
                        hm = True
                    else:
                        print('Still downloading!')
                        browser.implicitly_wait(50)

            Once all items in a week have been downloaded, upload

        upload(term, heading)

    browser.close()
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
