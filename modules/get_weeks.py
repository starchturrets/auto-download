from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def get_weeks(browser):

    element = WebDriverWait(browser, 90).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[ng-class="{selected: documentsCtrl.selectCurrentTermWeek}"]')))
    element.click()

    # def wait():
    browser.implicitly_wait(10)
    container_div = browser.find_elements_by_css_selector(
        'div.panel.ng-scope')

    # if len(container_div) < 2:
    #     wait()
    # else:
    #     return container_div

    shuld_wait = False
    weeks = browser.find_elements_by_css_selector(
        'div.panel.ng-scope')

    while shuld_wait == False:
        browser.implicitly_wait(10)
        weeks = browser.find_elements_by_css_selector(
            'div.panel.ng-scope')

        if len(weeks) > 2:
            shuld_wait = True

    return weeks
