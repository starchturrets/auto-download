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
from modules.get_stuff import get_weeks
from modules.get_stuff import get_grid

# from selenium.webdriver.common.keys import Keys


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
        print(color)
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


def main():

    clear_files()

    browser = setup_browser(webdriver)

    browser.get('https://sdpauth.sabis.net/')

    login(browser)

    browser.get(
        'https://digitalplatform.sabis.net/Pages/ExamPreparation/ExamPreparation?a=&scid=q7x6PiPCfek%3D')

    [weeks, term] = get_weeks(browser)

    print('It is term: {term}'.format(term=term))

    for week in weeks:
        heading = week.find_element_by_css_selector('.panel-heading').text
        print(heading)
        items = week.find_elements_by_css_selector('li div.col-sm-4 span')
        items = items[1::2]

        click_pdf_links(browser, items)
        # Once all items in a week have been downloaded, upload

        upload(term, heading)

    browser.implicitly_wait(90)
    grid_items = get_grid(browser, term)
    click_pdf_links(browser, grid_items)
    browser.implicitly_wait(90)

    upload(term, 'Grid')

    browser.close()


if __name__ == '__main__':
    main()
    # # schedule.every(2).seconds.do(main)
    # schedule.every().day.at("00:25").do(main)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
