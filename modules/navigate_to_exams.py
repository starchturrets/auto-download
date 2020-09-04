from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def main(browser):
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
