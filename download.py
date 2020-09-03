
import login
import glob
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC


def main(webdriver):

    print('Downloading teh files!!!')

 

   




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

        text = item.get_attribute('innerText')

        text = text.split('.pdf')

        if len(text) > 1:
            # item.click()

            print(item.get_attribute('innerText') + 'is a pdf!')

            hm = False

            while hm == False:
                fileList = glob.glob('./files/*.crdownload')
                print(fileList)
                if(len(fileList) == 0):
                    hm = True
                else:
                    print('Still downloading!')
                    browser.implicitly_wait(50)

    browser.close()

    return current
    # hmm = element.find_elements_by_css_selector('ul.list ')
