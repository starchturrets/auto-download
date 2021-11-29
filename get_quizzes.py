# import schedule
import time
import shutil
import os
import glob
import selenium
from selenium import webdriver

from modules.setup_browser import setup_browser
from modules.login import login
from modules.download import download
from modules.upload import upload
from modules.get_stuff import get_weeks
from modules.get_stuff import get_grid
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import natsort
from PIL import Image
import ocrmypdf
import os.path


def clear_files():
    shutil.rmtree('files')

    os.makedirs('files')

    shutil.rmtree('screenshots')
    os.makedirs('screenshots')


def open_quiz(browser, item):
    title = item.get_attribute('innerText')
    print("the title is:")
    print(title)
    print('opening quiz!')
    browser.execute_script('arguments[0].scrollIntoView(true)', item)

    item.click()
    WebDriverWait(browser, 90).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#QuizDescription')))

    radio_btn = browser.find_element_by_css_selector(
        'input[type="radio"][value="viewHistoryRdb"]')  # ng-hide="!documentsCtrl.popupOnlineQuizModelCenter.hasHistory"
    if(radio_btn.is_displayed()):
        # browser.find_element_by
        radio_btn.click()
        browser.find_element_by_css_selector(
            'button#activeOkBtn').click()

        table = WebDriverWait(browser, 90).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'table.quiz-result-table')))
        table.find_elements_by_css_selector('tr')[1].click()

        ans = WebDriverWait(browser, 90).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.student-answer-image')))

        ans.click()

        def wait_for_answer():
            print('')
            WebDriverWait(browser, 90).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.questionHolder')))

        def next_btn_exists():
            return browser.find_element_by_css_selector('div.next-tabs').is_displayed()
        index_questions = 0
        while next_btn_exists() == True:
            browser.execute_script(
                "document.querySelector('iframe#correctQuizQuestionActivity').style.marginLeft = '10px'")
            browser.execute_script(
                "document.querySelector('iframe#correctQuizQuestionActivity').style.paddingLeft = '10px'")
            # WebDriverWait(browser, 90).until(
            #     EC.NoSuchElementException((By.CSS_SELECTOR, 'div.questionHolder')))
            # while len(browser.find_elements_by_css_selector('div#preview > *')) != 1:
            #     browser.implicitly_wait(1)
            correct = WebDriverWait(browser, 90).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.correct-answer-image')))
            # correct = browser.find_elements_by_css_selector(
            #     'div.correct-answer-image')
            correct.click()
            WebDriverWait(browser, 90).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#showCorrectAnswerContent.odt-panel-hidden-remove')))
            panel = WebDriverWait(browser, 90).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#showCorrectAnswerContent.animate-right-content')))
            # EC.NoSuchElementException
            browser.implicitly_wait(1)
            # browser.find_element_by_css_selector('iframe#correctQuizQuestionActivity').screenshot(
            # 'screenshots' + '/' + title + '/' + str(index_questions) + '.png')
            path = 'screenshots/' + str(index_questions) + '.png'
            # browser.find_element_by_css_selector(

            def sus():
                browser.switch_to.frame("correctQuizQuestionActivity")
                p = browser.find_elements_by_css_selector('p.MsoNormal')
                if len(p) > 0:
                    browser.execute_script(
                        "arguments[0].setAttribute('style', 'padding: 20px;')", p[0])
                # browser.execute_script(
                #     "document.querySelector('p.MsoNormal').setAttribute('style', 'padding:20px')")
                # browser.execute_script(
                browser.switch_to.default_content()
                #     "let style = document.createElement('style');style.innerHTML='div::-webkit-scrollbar {display:none !important}p.MsoNormal{padding:15px}';document.head.appendChild(style);")
            #     'iframe#correctQuizQuestionActivity').screenshot(path)
            sus()
            browser.implicitly_wait(2)

            # browser.execute_script(
            #     "document.querySelector('p.MsoNormal').style.padding = '15px'")
            browser.save_screenshot(path)
            # print('Simulating screenshot of question')
            index_questions = index_questions + 1
            browser.find_element_by_css_selector('div.next-tabs').click()
        # print('Simulating screenshot of final question!')
        correct.click()
        WebDriverWait(browser, 90).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div#showCorrectAnswerContent.odt-panel-hidden-remove')))
        panel = WebDriverWait(browser, 90).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#showCorrectAnswerContent.animate-right-content')))
        browser.implicitly_wait(1)
        browser.execute_script(
            "document.querySelector('iframe#correctQuizQuestionActivity').style.marginLeft = '10px'")
        browser.implicitly_wait(2)
        # browser.find_element_by_css_selector(
        #     'iframe#correctQuizQuestionActivity').screenshot(path)

        sus()
        # browser.execute_script(
        #     "document.querySelector('p.MsoNormal').style.padding = '15px'")
        browser.save_screenshot(path)
        browser.implicitly_wait(5)

        def create_pdf():
            print('Creating PDF')
            dirname = 'screenshots/'

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
            imgs[0].save('files/' + title + '.pdf', save_all=True,
                         quality=100, append_images=imgs[1:])
            # shutil.rmtree(dirname)
            # os.makedirs('screenshots')
        create_pdf()

        for filename in os.listdir('/home/james/programming/auto-download/files'):
            print(filename)
            # print('Simulating conversion...')
            ocrmypdf.ocr(
                '/home/james/programming/auto-download/files/' + filename, '/home/james/programming/auto-download/files' + '/' + filename)

        browser.find_element_by_css_selector(
            'div[title="Finish Quiz"] button').click()
        browser.implicitly_wait(3)
        browser.get(
            'https://digitalplatform.sabis.net/Pages/ExamPreparation/ExamPreparation?a=&scid=q7x6PiPCfek%3D')
        WebDriverWait(browser, 900).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, """[ng-click="documentsCtrl.filterSelection('Week');"]""")))
    elif(radio_btn.is_displayed() == False):
        print('Quiz has not yet been attempted')
        browser.find_element_by_css_selector('button#activeCancelBtn').click()
        browser.implicitly_wait(1)
    # for item in items:

        # browser.execute_script('arguments[0].scrollIntoView(true)', item)
    #     browser.implicitly_wait(10)

    #     text = item.get_attribute('innerText')

    #     text = text.split('.pdf')

    #     color = item.value_of_css_property('color')
    #     # print(color)
    #     # print(color == 'rgb(0, 128, 187)')
    #     bool_thing = (color == 'rgba(0, 128, 187, 1)')
    #     # Temporary override
    #     # bool_thing = True
    #     if len(text) == 0 and bool_thing == True:
    #         print(item.get_attribute('innerText') + ' is a quiz!')
    #         # rgb(0, 128, 187)
    # WebDriverWait(browser, 90).until(
    #     EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#QuizDescription')))
    # radio_btns = browser.find_elements_by_css_selector(
    #     'input[type="radio"][value="viewHistoryRdb"]')
    # if(len(radio_btns) == 1):
    #     browser.find_element_by_css_selector(
    #         'button#activeOkBtn').click()
    #     WebDriverWait(browser, 90).until(
    #         EC.visibility_of_element_located((By.CSS_SELECTOR, 'table.quiz-result-table')))
    # elif(len(radio_btns) == 0):
    #     print('Quiz has not yet been attempted')


def main():
    print('getting quizzes')
    clear_files()
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver = webdriver.Chrome('/usr/local/share/chromedriver~')
    # driver = webdriver.Chrome()
    browser = setup_browser()
    # os.system(
    #     'xdg-user-dirs-update --set DOWNLOAD /home/james/programming/auto-download/files')
    browser.get('https://sdpauth.sabis.net/')

    login(browser)

    browser.get(
        'https://digitalplatform.sabis.net/Pages/ExamPreparation/ExamPreparation?a=&scid=q7x6PiPCfek%3D')

    # [weeks, term] = get_weeks(browser)

    term = 1
    print('It is term: {term}'.format(term=term))
    # def get_term():
    # WebDriverWait(browser, 900).until(
    #     EC.element_to_be_clickable(
    #         (By.CSS_SELECTOR, """[ng-click="documentsCtrl.filterSelection('Week');"]""")))
    # browser.find_element_by_css_selector('a.accept.button').click()

    def weeks_list():
        browser.implicitly_wait(10)
        # get_weeks(browser)
        weeks = get_weeks(browser)
        # weeks = browser.find_elements_by_css_selector(
        #     'div.panel.ng-scope')
        arr = []
        # Filter out those mysterious invisible elements
        for week in weeks:
            heading = week.find_element_by_css_selector('.panel-heading').text
            if len(heading) > 0:
                arr.append(week)

        # return [arr, term]
        return arr

    def quiz_list(week_element):
        # quizzes = week_element.find_elements_by_css_selector(
        # 'li div.col-sm-4 span')
        quizzes = week_element.find_elements_by_css_selector(
            'span.ng-binding[ng-bind-html*="document.Name"]')
        index = 0
        arr = []
        # print(len(quizzes))
        while index < len(quizzes):
            text = quizzes[index].get_attribute('innerText')  # .split('.pdf')
            # print(text)
            # print(text.find('pdf'))
            if text.find('pdf') == -1:
                # print('QUIZ FOUND')
                # quizzes.remove(quizzes[index])
                arr.append(quizzes[index])
            index = index + 1
        # for (quiz, index) in quizzes:
        #     text = quiz.getAttribute('innerText').split('.pdf')
        # print(len(arr))
        return arr
    a = browser.find_element_by_css_selector('a.accept.button')
    a.click()
    # print(len(weeks_list()))
    week_index = 0  # len(weeks_list())  # -1

    while week_index < len(weeks_list()):
        # week = weeks_list()[week_index]
        print(week_index)
        quiz_index = 0
        # quiz = quiz_list(week)[quiz_index]

        while quiz_index < len(quiz_list(weeks_list()[week_index])):
            print(term, weeks_list()[week_index].find_element_by_css_selector(
                '.panel-heading').text)
            open_quiz(browser, quiz_list(weeks_list()[week_index])[quiz_index])
            quiz_index = quiz_index + 1

            # upload(term, weeks_list()[week_index].find_element_by_css_selector(
            #     '.panel-heading').text)
            clear_files()
        week_index = week_index + 1


if __name__ == '__main__':
    main()
