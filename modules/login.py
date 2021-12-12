
import json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def login(browser, username, password):

    def logged_in():
        if len(browser.find_elements_by_css_selector('.exampreparation-tile')) == 0:
            return False
        else:
            return True
    WebDriverWait(browser, 90).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#username')))

    def get_credentials():
        with open('./webschool_credentials.json') as file:
            credentials = json.loads(file.read())
            return [credentials['username'], credentials['password']]

    if logged_in() == False:
        # credentials = get_credentials()

        username_el = browser.find_element_by_css_selector('#username')

        password_el = browser.find_element_by_css_selector('#password')

        login_btn = browser.find_element_by_css_selector('#loginButton')
        username_el.send_keys(username)
        password_el.send_keys(password)
        browser.execute_script('arguments[0].scrollIntoView(true)', login_btn)

        login_btn.click()
        # browser.execute_script(
        # 'document.querySelector("#loginButton").click()')


def login_ebooks(browser):
    def logged_in():
        return len(browser.find_elements_by_css_selector('input.text-input')) != 2

    def get_credentials():
        with open('./webschool_credentials.json') as file:
            credentials = json.loads(file.read())
            return [credentials['username'], credentials['password']]

    WebDriverWait(browser, 90).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Username"]')))

    if logged_in() == False:
        [username, password] = get_credentials()
        username_input = browser.find_element_by_css_selector(
            'input[placeholder="Username"]')
        password_input = browser.find_element_by_css_selector(
            'input[placeholder="Password"]')
        username_input.send_keys(username)
        password_input.send_keys(password)
        browser.execute_script(
            "document.querySelector('a.accept.button').click()")
        login_btn = browser.find_element_by_css_selector('button.login-btn')
        browser.execute_script(
            'arguments[0].removeAttribute("disabled")', login_btn)
        # browser.execute_script(
        #     "document.querySelector('div.cookie-bar').style.display = 'none'")
        login_btn.click()
        print('Logging in!')
