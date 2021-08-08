def setup_browser(webdriver):
    options = webdriver.ChromeOptions()

    options.add_experimental_option('prefs',  {
        'download.default_directory': '/home/james/programming/auto-download/files'})

    # options.add_argument('--no-sandbox')
    # options.add_argument('--headless')
    options.add_argument('--start-fullscreen')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_argument('window-size=1400,200')
    options.add_argument('--remote-debugging-port=9322')

    browser = webdriver.Chrome(
        executable_path="chromedriver", port=0, options=options)

    return browser
