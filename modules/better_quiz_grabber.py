# import schedule
import os.path
import ocrmypdf
from PIL import Image
import natsort
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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
from modules.upload import get_files
from modules.get_stuff import get_weeks
from modules.get_stuff import get_grid
from webdriver_manager.chrome import ChromeDriverManager
import json
# from selenium.webdriver.common.keys import Keys


def better_quiz_grabber(username, password, account_id):
    def get_credentials():
        with open('./webschool_credentials.json') as file:
            credentials = json.loads(file.read()).credentials[0]
            return [credentials['username'], credentials['password'], credentials['account_id']]

    def crop():
        path = '/home/james/programming/auto-download/screenshots'
        dirs = os.listdir(path)
        for item in dirs:
            # print(item)
            fullpath = os.path.join(path, item)
            if os.path.isfile(fullpath):
                im = Image.open(fullpath)
                f, e = os.path.splitext(fullpath)
                # print(item)
                imcrop = im.crop((447, 179, 1903, 1080))
                imcrop.save(f+'.png', 'PNG', quality=100)

    def get_questions(browser, title):
        print('')

        def sus():
            browser.switch_to.frame("correctQuizQuestionActivity")
            p = browser.find_elements_by_css_selector('p.MsoNormal')
            if len(p) > 0:
                if "NS Math" in title:
                    for item in p:
                        browser.execute_script(
                            "arguments[0].setAttribute('style', 'padding-bottom: 12px;')", item)
            browser.switch_to.default_content()
        table = WebDriverWait(browser, 90).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'table.quiz-result-table')))

        browser.execute_script(
            'angular.element(document.querySelector("div.quiz-result")).scope().onlineQuizResultCtrl.quizResultsEntries.forEach(ans=> ans.hasAnswer="enabled")')
        browser.implicitly_wait(10)

        # document.querySelectorAll('table.quiz-result-table tr')
        questions = browser.find_elements_by_css_selector(
            'table.quiz-result-table tr.ng-scope')

        for index, question in enumerate(questions):
            question.click()
            # if index == 0:
            #     print('wait one')
            #     WebDriverWait(browser, 90).until(
            #         EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.correct-answer-image')))
            WebDriverWait(browser, 900).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div#loading-bar')))

            browser.find_element_by_css_selector(
                'div.correct-answer-image').click()
            # wait for correct answer
            WebDriverWait(browser, 90).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#showCorrectAnswerContent.odt-panel-hidden-remove')))
            print(1)
            WebDriverWait(browser, 90).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#showCorrectAnswerContent.odt-panel-hidden-remove-active')))
            print(2)
            WebDriverWait(browser, 90).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#showCorrectAnswerContent.content.animate-right-content')))
            print(3)
            # screenshot
            browser.implicitly_wait(1)
            sus()
            print('screenshotting: ' + str(index))
            path = 'screenshots/' + str(index) + '.png'
            browser.implicitly_wait(1)
            browser.save_screenshot(path)
            browser.implicitly_wait(1)
            # click exit button
            close_btn = browser.find_element_by_css_selector(
                'div.quiz-panel-close-btn')
            close_btn.click()
            # wait again
            WebDriverWait(browser, 900).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div#loading-bar')))
            # WebDriverWait(browser, 90).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, 'div.correct-answer-selected-image-remove')))
            # WebDriverWait(browser, 90).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, 'div.content.animate-right-content.odt-panel-hidden')))

        crop()

    def clear_files():
        shutil.rmtree('files')

        os.makedirs('files')

        shutil.rmtree('screenshots')

        os.makedirs('screenshots')

    # angular.element(document.querySelector("div.quiz-result")).scope().onlineQuizResultCtrl.quizResultsEntries.forEach(ans=>ans.hasAnswer="enabled")

    def click_pdf_links(browser, items):

        for item in items:

            browser.execute_script('arguments[0].scrollIntoView(true)', item)
            browser.implicitly_wait(10)

            text = item.get_attribute('innerText')

            text = text.split('.pdf')

            color = item.value_of_css_property('color')
            # print(color)
            # print(color == 'rgb(0, 128, 187)')
            bool_thing = (color == 'rgba(0, 128, 187, 1)')
            # Temporary override
            # bool_thing = True
            if len(text) > 1 and bool_thing == True:
                print(item.get_attribute('innerText') + ' is a pdf!')
                # rgb(0, 128, 187)

                item.click()
                hm = False

                while hm == False:
                    def fileList():
                        return glob.glob('./files/*.crdownload')

                    if(len(fileList()) == 0):
                        hm = True
                    else:
                        browser.implicitly_wait(10)

    def open_quiz(browser, item):
        title = item.get_attribute('innerText')
        print("the title is:")
        print(title)
        print('opening quiz!')
        browser.execute_script('arguments[0].scrollIntoView(true)', item)

        def quiz_done():
            radio_btn = browser.find_element_by_css_selector(
                'input[type="radio"][value="viewHistoryRdb"]')
            # return radio_btn.is_displayed()
            return False
        item.click()
        WebDriverWait(browser, 90).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#QuizDescription')))

    # ng-hide="!documentsCtrl.popupOnlineQuizModelCenter.hasHistory"
        quizId = browser.execute_script(
            "return angular.element(document.querySelector('#activeOkBtn')).scope().documentsCtrl.popupOnlineQuizModelCenter.popupId")
        isDeleted = browser.execute_script(
            "return angular.element(document.querySelector('#activeOkBtn')).scope().documentsCtrl.popupOnlineQuizModelCenter.isDeleted")
        QuizLevelSectionId = browser.execute_script(
            "return angular.element(document.querySelector('#activeOkBtn')).scope().documentsCtrl.popupOnlineQuizModelCenter.popupQuizLevelSectionId")
        selectedQuizSessionId = browser.execute_script(
            "return angular.element(document.querySelector('#activeOkBtn')).scope().documentsCtrl.popupOnlineQuizModelCenter.popupSessionQuizId")
        # print(id) "&accountId=fsqh8%2Fu5ByQ%3D&selectedQuizSessionId="
        # https://digitalplatform.sabis.net/Pages/OnlineQuiz/OnlineQuizResult?quizId=cMfsocEJJZM%3D&isDeleted=0&quizLevelSectionId=XeffvsJs7zs%3D&accountId=fsqh8%2Fu5ByQ%3D&selectedQuizSessionId=9LSVbWcCJbhokrN%2FCOQORw%3D%3D&scid=q7x6PiPCfek%3D
        # account = '&accountId=makQjpBwEjI%3D&selectedQuizSessionId='
        account = '&accountId=fsqh8%2Fu5ByQ%3D&selectedQuizSessionId='

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
        if(quiz_done() == True):

            # https://digitalplatform.sabis.net/Pages/ExamPreparation/ExamPreparation?a=fsqh8%2Fu5ByQ%3D&scid=q7x6PiPCfek%3D
            # 9LSVbWcCJbhokrN%2FCOQORw%3D%3D
            url = "https://digitalplatform.sabis.net/Pages/OnlineQuiz/OnlineQuizResult?quizId=cMfsocEJJZM%3D&isDeleted=0&quizLevelSectionId=XeffvsJs7zs%3D&accountId=fsqh8%2Fu5ByQ%3D&selectedQuizSessionId=9LSVbWcCJbhokrN%2FCOQORw%3D%3D&scid=q7x6PiPCfek%3D"
            url = "https://digitalplatform.sabis.net/Pages/OnlineQuiz/OnlineQuizResult?quizId=" + \
                quizId + "&isDeleted=" + str(isDeleted) + "&quizLevelSectionId=" + \
                QuizLevelSectionId + account + \
                selectedQuizSessionId + "&scid=q7x6PiPCfek%3D"
            browser.execute_script("window.open()")
            browser.switch_to.window(browser.window_handles[1])
            browser.get(url)

            get_questions(browser, title)

            # shutil.rmtree(dirname)
            # os.makedirs('screenshots')
            create_pdf()

            for filename in os.listdir('/home/james/programming/auto-download/files'):
                print(filename)
                # print('Simulating conversion...')
                ocrmypdf.ocr(
                    '/home/james/programming/auto-download/files/' + filename, '/home/james/programming/auto-download/files' + '/' + filename)

            browser.close()
            browser.switch_to.window(browser.window_handles[0])

            browser.find_element_by_css_selector('#activeCancelBtn').click()

        elif(quiz_done() == False):
            print('Quiz has not yet been attempted')
            # popupid, popupquizlevelsectionid, scid, accountid, sessionid

            url = 'https://digitalplatform.sabis.net/Pages/OnlineQuiz/OnlineQuizNavigation?id=YbYsNsltrPE%3D&quizLevelSectionId=6wg49xZNvUI%3D&scid=q7x6PiPCfek%3D&accountId=fsqh8%2Fu5ByQ%3D&sessionId=ZwhGsEbWw81VA2ac%2Bhlbag%3D%3D'

            url = 'https://digitalplatform.sabis.net/Pages/OnlineQuiz/OnlineQuizNavigation?id=' + str(quizId) + '&quizLevelSectionId=' + str(
                QuizLevelSectionId) + '&scid=q7x6PiPCfek%3D&accountId=fsqh8%2Fu5ByQ%3D&sessionId=' + str(selectedQuizSessionId)
            browser.execute_script("window.open()")
            browser.switch_to.window(browser.window_handles[1])
            browser.get(url)
            # submit quiz (twice)

            def submit_btn():
                return WebDriverWait(browser, 90).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[ng-click="onlineQuizNavigationCtrl.submitQuiz(true)"]')))
            submit_btn().click()
            WebDriverWait(browser, 90).until(EC.alert_is_present())
            browser.switch_to.alert.accept()
            submit_btn().click()
            WebDriverWait(browser, 90).until(EC.alert_is_present())
            browser.switch_to.alert.accept()
            get_questions(browser, title)
            create_pdf()
            browser.close()
            browser.switch_to.window(browser.window_handles[0])

            browser.find_element_by_css_selector(
                'button#activeCancelBtn').click()
            browser.implicitly_wait(1)

    def main():

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

        term = 1
        weeks = get_weeks(browser)
        weeks.pop(0)
        weeks.pop(0)

        print('It is term: {term}'.format(term=term))
        browser.implicitly_wait(1)
        browser.execute_script(
            "document.querySelector('a.accept.button').click()")
        browser.implicitly_wait(15)
        print(len(weeks))
        for week in weeks:
            heading = week.find_element_by_css_selector('.panel-heading').text
            files = get_files(heading)
            file_list = []
            for file in files:
                file_list.append(str(file['name']).split('.pdf')[0])
            for file in file_list:
                print(file)
            print(heading)

            # Once all items in a week have been downloaded, upload
            hm = False
            arr = week.find_elements_by_css_selector(
                'span.ng-binding[ng-bind-html*="document.Name"]')
            quiz_list = []
            index = 0

            while index < len(arr):
                text = arr[index].get_attribute(
                    'innerText')  # .split('.pdf')
                # print(text)
                # print(text.find('pdf'))
                # angular.element(document.querySelector('#activeOkBtn')).scope().documentsCtrl.popupOnlineQuizModelCenter.popupSessionQuizId

                if text.find('pdf') == -1:
                    if text not in file_list:
                        # print('QUIZ FOUND')
                        # quizzes.remove(quizzes[index])

                        quiz_list.append(arr[index])
                        print("adding! " + text)

                index = index + 1
            for quiz in quiz_list:

                open_quiz(browser, quiz)
                upload(term, heading)
                clear_files()
                # browser.execute_script()

            # upload(term, heading)

        # os.system('xdg-user-dirs-update --set DOWNLOAD /home/james/Downloads')

        browser.close()


if __name__ == '__main__':
    main()
    # print(len(glob.glob('./files/*.crdownload')))
