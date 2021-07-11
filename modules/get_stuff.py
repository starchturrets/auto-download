from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def get_weeks(browser):

    def wait_and_click(selector):
        el = WebDriverWait(browser, 90).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, selector)))
        el.click()

    wait_and_click(
        '[ng-class="{selected: documentsCtrl.selectCurrentTermWeek}"]')

    browser.implicitly_wait(10)

    term = WebDriverWait(browser, 90).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.filter.data b.ng-binding'))).text

    week = browser.find_elements_by_css_selector(
        'div.filter.data b.ng-binding')[1].text

    term = term.split('Term')[1].strip()

    term = int(term)

    wait_and_click("""[ng-click="documentsCtrl.filterSelection('Week');"]""")

    wait_and_click('.all-week-label span')

    weeks_length = int(len(browser.find_elements_by_css_selector(
        'div.week-label [ng-repeat="week in documentsCtrl.allWeeks"]'))) / 2

    container_div = browser.find_elements_by_css_selector(
        'div.panel.ng-scope')

    shuld_wait = True
    weeks = browser.find_elements_by_css_selector(
        'div.panel.ng-scope')

    while shuld_wait == True:
        browser.implicitly_wait(10)
        weeks = browser.find_elements_by_css_selector(
            'div.panel.ng-scope')

        if len(weeks) > weeks_length:
            shuld_wait = False

    arr = []
    # Filter out those mysterious invisible elements
    for week in weeks:
        heading = week.find_element_by_css_selector('.panel-heading').text
        if len(heading) > 0:
            arr.append(week)

    return [arr, term]


def get_grid(browser, term):
    browser.get(
        'https://digitalplatform.sabis.net/pages/grid/grid?scid=q7x6PiPCfek%3D')

    items = WebDriverWait(browser, 90).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.panel > ul.list-group li:not(.ng-hide)')))

    return items


def get_books(browser, subject):
    books = subject.find_elements_by_css_selector('ebook-bookshelf-item')

    for book in books:
        # info_btn = book.find_element_by_css_selector(
        #     'span.item-info-button')
        info_btn = WebDriverWait(browser, 90).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.item-info-button')))
        # if EC.visibility_of_element_located()
        browser.execute_script('arguments[0].click()', info_btn)
        # info_btn.click()

        title_div = WebDriverWait(browser, 90).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.title')))

        title = title_div.get_attribute('innerText')
        print(title)

        close_btn = browser.find_element_by_css_selector(
            'button[aria-label="Close"]')
        close_btn.click()
        book.click()
        canvas = WebDriverWait(browser, 90).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'canvas')))
        browser.get('https://master-cms.sabis.net/ebook/bookshelf')
        # [...document.querySelectorAll('canvas.upper-canvas')].filter(item => item.clientHeight > 0)
