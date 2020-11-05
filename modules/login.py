
import json


def login(browser):

    def logged_in():
        if len(browser.find_elements_by_css_selector('.exampreparation-tile')) == 0:
            return False
        else:
            return True

    def get_credentials():
        with open('./webschool_credentials.json') as file:
            credentials = json.loads(file.read())
            return [credentials['username'], credentials['password']]

    if logged_in() == False:
        credentials = get_credentials()

        username = browser.find_element_by_css_selector('#username')

        password = browser.find_element_by_css_selector('#password')

        login_btn = browser.find_element_by_css_selector('#loginButton')
        username.send_keys(credentials[0])
        password.send_keys(credentials[1])

        login_btn.click()
        # browser.execute_script(
            # 'document.querySelector("#loginButton").click()')
