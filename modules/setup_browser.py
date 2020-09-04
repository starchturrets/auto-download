def setup_browser(webdriver):
    options = webdriver.ChromeOptions()

    options.add_experimental_option('prefs',  {
        'download.default_directory': '/home/james/programming/auto-download/files'})

    browser = webdriver.Chrome(
        executable_path="chromedriver", port=0, options=options)

    return browser
