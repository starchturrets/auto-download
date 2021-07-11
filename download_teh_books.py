# import schedule
import time
import shutil
import os
import glob
import selenium
from selenium import webdriver


from modules.setup_browser import setup_browser
from modules.login import login_ebooks
# from modules.download import download
# from modules.upload import upload
# from modules.get_stuff import get_weeks
# from modules.get_stuff import get_grid
from modules.get_stuff import get_books
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def clear_files():
    shutil.rmtree('files')

    os.makedirs('files')


def create_folder(name, parent_dir):
    print(name)


def main():

    clear_files()

    os.makedirs('files/' + 'test_directory')
    browser = setup_browser(webdriver)

    browser.get('https://master-cms.sabis.net/login')

    login_ebooks(browser)

    def subjects_list():
        WebDriverWait(browser, 90).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.bookshlef-body > div.ng-star-inserted > ebook-bookshelf-item-slider')))
        return browser.find_elements_by_css_selector(
            '.bookshlef-body > div.ng-star-inserted > ebook-bookshelf-item-slider')

    index_subjects = 0
    while index_subjects < len(subjects_list()):
        subject = subjects_list()[index_subjects]
        browser.execute_script(
            'arguments[0].scrollIntoView(true)', subject)

        subject_name = subject.find_element_by_css_selector('.slider-title')
        subject_name = subject_name.get_attribute('innerText')

        print('Subject: ' + subject_name)
        os.makedirs('files/' + subject_name)

        books = subject.find_elements_by_css_selector(
            'ebook-bookshelf-item')

        def books_list():
            return subjects_list()[index_subjects].find_elements_by_css_selector('ebook-bookshelf-item')

        index_books = 0
        while index_books < len(books_list()):
            book = books_list()[index_books]
            info_btn = book.find_element_by_css_selector(
                'span.item-info-button')
            browser.execute_script('arguments[0].click()', info_btn)

            title_div = WebDriverWait(browser, 90).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.title')))

            title = title_div.get_attribute('innerText')
            print(title)

            close_btn = browser.find_element_by_css_selector(
                'button[aria-label="Close"]')
            close_btn.click()

            browser.execute_script('arguments[0].scrollIntoView(true)', book)
            os.makedirs('files/' + subject_name + '/' + title)

            book.click()
            canvas = WebDriverWait(browser, 90).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'iframe#master')))

            canvas.screenshot('files/' + subject_name + '/' + title)
            browser.get('https://master-cms.sabis.net/ebook/bookshelf')
            index_books = index_books + 1

        index_subjects = index_subjects + 1


if __name__ == '__main__':
    main()
