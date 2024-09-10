import os.path
from selenium.common.exceptions import WebDriverException
import re
import time
import shutil
import os
import glob
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import img2pdf
from PIL import Image
from modules.setup_browser import setup_browser
from modules.login import login_ebooks

from modules.get_stuff import get_books
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import natsort
from PIL import ImageFile
import shutil
from selenium.webdriver.common.keys import Keys
ImageFile.LOAD_TRUNCATED_IMAGES = True


def sorted_alphanumeric(data):
    def convert(text): return int(text) if text.isdigit() else text.lower()
    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9+])', key)]
    return sorted(data, key=alphanum_key)


def clear_files():
    shutil.rmtree('files')

    os.makedirs('files')


def create_folder(name, parent_dir):
    print(name)


def main():

    # clear_files()

    # os.makedirs('files/' + 'test_directory')
 #   browser = setup_browser(webdriver)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()                          
    browser.get('https://master-cms.sabis.net/login')
    
    print('y u no login?')
    login_ebooks(browser)

    def subjects_list():
        WebDriverWait(browser, 90).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.bookshlef-body > div.ng-star-inserted > ebook-bookshelf-item-slider')))
        return browser.find_elements(By.CSS_SELECTOR,   
            '.bookshlef-body > div.ng-star-inserted > ebook-bookshelf-item-slider')

    index_subjects = 1
    while index_subjects < len(subjects_list()):
        subject = subjects_list()[index_subjects]
        browser.execute_script(
            'arguments[0].scrollIntoView(true)', subject)

        subject_name = subject.find_element(By.CSS_SELECTOR,'.slider-title')
        subject_name = subject_name.get_attribute('innerText')

        print('Subject: ' + subject_name)
        if os.path.exists('files/' + subject_name) == False:
            os.makedirs('files/' + subject_name)

        books = subject.find_elements(By.CSS_SELECTOR,  
            'ebook-bookshelf-item')

        def books_list():
            return subjects_list()[index_subjects].find_elements(By.CSS_SELECTOR,   'ebook-bookshelf-item')

        index_books = 1 
        while index_books < len(books_list()):
            def book():
                return books_list()[index_books]

            def await_page_load():
                WebDriverWait(browser, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe#master.hidden')))

                browser.implicitly_wait(1)
                iframe_elements = browser.find_elements(By.CSS_SELECTOR,    
                    'div.page-view-wrapper.twoPages')

                if len(iframe_elements) == 2:
                    # print('Two pages!')

                    WebDriverWait(browser, 15).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, 'iframe#slave:not(.hidden)')))
                    WebDriverWait(browser, 15).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, 'iframe#master:not(.hidden)')))
                elif len(iframe_elements) == 0:
                    # print('Only one page!')

                    WebDriverWait(browser, 15).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, 'iframe#master:not(.hidden)')))

            def screenshot_pages(index_canvas, index_pages):
                def canvas_list():
                    return browser.find_elements(By.CSS_SELECTOR,   
                        'canvas.upper-canvas')

                def filter_function(item):
                    if item.size['height'] > 0:
                        return True
                    else:
                        return False
                # canvas_list = filter(filter_function, canvas_list())
                # print(len(canvas_list()))
                while index_canvas < len(canvas_list()):
                    # print('yesyomh')
                    if canvas_list()[index_canvas].size['height'] > 0:
                        canvas_list()[index_canvas].screenshot('files/' + subject_name +
                                                               '/' + title + '/' + str(index_pages) + '.png')
                        index_pages = index_pages + 1
                    index_canvas = index_canvas + 1
                return index_pages

            def load_next():
                # print('Loading next!')

                next_btn = browser.find_elements(By.CSS_SELECTOR,   
                    'div.navigationButton.next')[1]
                next_btn.click()

            info_btn = book().find_element(By.CSS_SELECTOR,
                'span.item-info-button')
            browser.execute_script('arguments[0].click()', info_btn)

            title_div = WebDriverWait(browser, 90).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.title')))

            title = title_div.get_attribute('innerText')
            print(title)

            close_btn = browser.find_element(By.CSS_SELECTOR,
                'button[aria-label="Close"]')
            close_btn.click()

            browser.execute_script('arguments[0].scrollIntoView(true)', book())
            os.makedirs('files/' + subject_name + '/' + title)

            book().click()  
    #       load first page
    #       Improve await function
            # WebDriverWait(browser, 90).until(
            #     EC.visibility_of_element_located((By.CSS_SELECTOR, 'iframe#master')))
            index_pages = 0

            index_canvas = 0

            def jump_to_last_page(await_load):
                # browser.execute_script(
                #     'document.querySelector(".lastPage").click()')
                browser.execute_script(
                    "document.querySelectorAll('div.page-view-wrapper')[1].click()")
                # browser.execute_script("")
                input_element = WebDriverWait(browser, 90).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='number']")))
                input_element.send_keys('1047' + Keys.ENTER)
                await_load()
                browser.execute_script(
                    "document.querySelectorAll('div.page-view-wrapper')[0].click()")

            # to_continue = True

            def end_reached():
                # browser.implicitly_wait(1)
                hmm = len(browser.find_elements(By.CSS_SELECTOR,    
                    'div.navigationButton.next[hidden]')) == 2
                # print(hmm)
                return hmm
                # return len(browser.find_elements(By.CSS_SELECTOR, 'div.navigationButton.next[hidden]')) == 2

            def reopen_book(book):
                browser.get(
                    'https://master-cms.sabis.net/ebook/bookshelf')
                book().click()
                # screenshot_pages()

            # def screenshot_pages():

            # await_page_load()
            # print('WAITED FOR FIRST PAGE')
            # jump_to_last_page(await_page_load)

            # load_next()
            while True:

                try:
                    # print('Trying...')
                    await_page_load()
                    # print(str(end_reached()) + 'hmm')

                    if end_reached() == True:
                        # print('BREAK BREAK BREAK')
                        browser.implicitly_wait(1)
                        # print('Simulating screenshots')
                        index_pages = screenshot_pages(
                            index_canvas, index_pages)
                        break

                    elif end_reached() == False:
                        # print('Simulating screenshots')
                        index_pages = screenshot_pages(
                            index_canvas, index_pages)
                        load_next()
                except:
                    # print('FAILURE')
                    try:
                        # print('Trying again...')
                        reopen_book(book)
                        await_page_load()
                        # print(str(end_reached()) + 'hmm')

                        if end_reached() == True:
                            # print('BREAK BREAK BREAK')
                            browser.implicitly_wait(1)
                            # print('Simulating screenshots')
                            index_pages = screenshot_pages(
                                index_canvas, index_pages)
                            break

                        elif end_reached() == False:
                            # print('Simulating screenshots')
                            index_pages = screenshot_pages(
                                index_canvas, index_pages)
                            load_next()
                    except:
                        # print('FAILURE AGAIN')
                        reopen_book(book)
                        try:
                            # print('TRYING AGAIN')
                            await_page_load()
                            # print(str(end_reached()) + 'hmm')

                            if end_reached() == True:
                                # print('BREAK BREAK BREAK')
                                browser.implicitly_wait(1)
                                # print('Simulating screenshots')
                                index_pages = screenshot_pages(
                                    index_canvas, index_pages)
                                break

                            elif end_reached() == False:
                                # print('Simulating screenshots')
                                index_pages = screenshot_pages(
                                    index_canvas, index_pages)
                                load_next()
                        except:
                            # print('ANOTHER FAILURE')
                            reopen_book(book)
                            try:
                                # print('LET US DO THIS AGAIN')
                                await_page_load()
                                # print(str(end_reached()) + 'hmm')

                                if end_reached() == True:
                                    # print('BREAK BREAK BREAK')
                                    browser.implicitly_wait(1)
                                    # print('Simulating screenshots')
                                    index_pages = screenshot_pages(
                                        index_canvas, index_pages)
                                    break

                                elif end_reached() == False:
                                    # print('Simulating screenshots')
                                    index_pages = screenshot_pages(
                                        index_canvas, index_pages)
                                    load_next()
                            except:
                                # print('AHHH')
                                reopen_book(book)
                                await_page_load()
                                # print(str(end_reached()) + 'hmm')

                                if end_reached() == True:
                                    # print('BREAK BREAK BREAK')
                                    browser.implicitly_wait(1)
                                    # print('Simulating screenshots')
                                    index_pages = screenshot_pages(
                                        index_canvas, index_pages)
                                    break

                                elif end_reached() == False:
                                    # print('Simulating screenshots')
                                    index_pages = screenshot_pages(
                                        index_canvas, index_pages)
                                    load_next()

            print('Book finished')

            def create_pdf():
                print('Creating PDF')
                dirname = 'files/' + subject_name + '/' + title + '/'

                imgs = []
                for fname in natsort.natsorted(os.listdir(dirname)):
                    # print(fname)
                    if not fname.endswith('.png'):
                        continue
                    path = os.path.join(dirname, fname)
                    if os.path.isdir(path):
                        continue
                    im = Image.open(path)

                    if im.mode == 'RGBA':
                        # print('Converting!')
                        im = im.convert('RGB')
                    imgs.append(im)
                imgs[0].save('files/' + subject_name + '/' + title + '.pdf', save_all=True,
                             quality=100, append_images=imgs[1:])
                shutil.rmtree(dirname)

            create_pdf()
            browser.get('https://master-cms.sabis.net/ebook/bookshelf')
            index_books = index_books + 1

        index_subjects = index_subjects + 1


if __name__ == '__main__':
    main()
