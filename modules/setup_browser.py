from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager


def setup_browser():
    driver: webdriver = webdriver.Chrome(ChromeDriverManager().install())

    # opt = webdriver.c
    options: Options = webdriver.ChromeOptions()
    # options = webdriver.opt
    # options.add_argument(
    #     'download.default_directory=/home/james/programming/auto-download/files')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--headless')
    options.add_argument('--start-fullscreen')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_argument('window-size=1400,200')
    options.add_argument('--remote-debugging-port=9322')
    options.add_argument('--hide-scrollbars')
    # prefs = {
    #     'download': {'default_directory': '/home/james/programming/auto-download/files', 'directory_upgrade': True}}
    # options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(
        executable_path="chromedriver", port=0, options=options)

    return browser
