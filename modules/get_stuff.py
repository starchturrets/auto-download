from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def get_weeks(browser):

    def wait_and_click(selector):
        el = WebDriverWait(browser, 90).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, selector)))
        el.click()

    # element = WebDriverWait(browser, 90).until(
    #     EC.element_to_be_clickable(
    #         (By.CSS_SELECTOR, '[ng-class="{selected: documentsCtrl.selectCurrentTermWeek}"]')))
    # element.click()

    wait_and_click(
        '[ng-class="{selected: documentsCtrl.selectCurrentTermWeek}"]')

    browser.implicitly_wait(10)

    term = WebDriverWait(browser, 90).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.filter.data b.ng-binding'))).text

    week = browser.find_elements_by_css_selector(
        'div.filter.data b.ng-binding')[1].text

    # week = int(week.split('Week')[1].strip())

    # term = browser.find_element_by_css_selector(
    #     'div.filter.data').find_element_by_css_selector('b.ng-binding').text
    # document.querySelector('.all-week-label label').click()
    # //click this
    print(term)
    term = term.split('Term')[1].strip()

    term = int(term)
    # browser.refresh()
    # WebDriverWait(browser, 90).until(
    # EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.filter.data b.ng-binding'))).text

    wait_and_click("""[ng-click="documentsCtrl.filterSelection('Week');"]""")

    wait_and_click('.all-week-label span')

    weeks_length = int(len(browser.find_elements_by_css_selector(
        'div.week-label [ng-repeat="week in documentsCtrl.allWeeks"]'))) / 2

    # browser.find_element_by_css_selector('.all-week-label label').click()
    # browser.execute_script(
    #     'document.querySelector(".all-week-label label").click()')
    # # def wait():
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
