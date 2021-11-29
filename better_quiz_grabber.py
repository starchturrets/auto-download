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
# from selenium.webdriver.common.keys import Keys


def crop():
    path = '/home/james/programming/auto-download/screenshots'
    dirs = os.listdir(path)
    for item in dirs:
        print(item)
        fullpath = os.path.join(path, item)
        if os.path.isfile(fullpath):
            im = Image.open(fullpath)
            f, e = os.path.splitext(fullpath)
            print(item)
            imcrop = im.crop((447, 179, 1903, 1080))
            imcrop.save(f+'.png', 'PNG', quality=100)


def clear_files():
    shutil.rmtree('files')

    os.makedirs('files')

    shutil.rmtree('screenshots')

    os.makedirs('screenshots')


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

    item.click()
    WebDriverWait(browser, 90).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#QuizDescription')))

    radio_btn = browser.find_element_by_css_selector(
        'input[type="radio"][value="viewHistoryRdb"]')  # ng-hide="!documentsCtrl.popupOnlineQuizModelCenter.hasHistory"
    if(radio_btn.is_displayed()):
        quizId = browser.execute_script(
            "return angular.element(document.querySelector('#activeOkBtn')).scope().documentsCtrl.popupOnlineQuizModelCenter.popupId")
        isDeleted = browser.execute_script(
            "return angular.element(document.querySelector('#activeOkBtn')).scope().documentsCtrl.popupOnlineQuizModelCenter.isDeleted")
        QuizLevelSectionId = browser.execute_script(
            "return angular.element(document.querySelector('#activeOkBtn')).scope().documentsCtrl.popupOnlineQuizModelCenter.popupQuizLevelSectionId")
        selectedQuizSessionId = browser.execute_script(
            "return angular.element(document.querySelector('#activeOkBtn')).scope().documentsCtrl.popupOnlineQuizModelCenter.popupSessionQuizId")
        # print(id)
        # https://digitalplatform.sabis.net/Pages/OnlineQuiz/OnlineQuizResult?quizId=cMfsocEJJZM%3D&isDeleted=0&quizLevelSectionId=XeffvsJs7zs%3D&accountId=fsqh8%2Fu5ByQ%3D&selectedQuizSessionId=9LSVbWcCJbhokrN%2FCOQORw%3D%3D&scid=q7x6PiPCfek%3D

        # https://digitalplatform.sabis.net/Pages/ExamPreparation/ExamPreparation?a=fsqh8%2Fu5ByQ%3D&scid=q7x6PiPCfek%3D
        # 9LSVbWcCJbhokrN%2FCOQORw%3D%3D
        url = "https://digitalplatform.sabis.net/Pages/OnlineQuiz/OnlineQuizResult?quizId=cMfsocEJJZM%3D&isDeleted=0&quizLevelSectionId=XeffvsJs7zs%3D&accountId=fsqh8%2Fu5ByQ%3D&selectedQuizSessionId=9LSVbWcCJbhokrN%2FCOQORw%3D%3D&scid=q7x6PiPCfek%3D"
        url = "https://digitalplatform.sabis.net/Pages/OnlineQuiz/OnlineQuizResult?quizId=" + \
            quizId + "&isDeleted=" + str(isDeleted) + "&quizLevelSectionId=" + \
            QuizLevelSectionId + "&accountId=fsqh8%2Fu5ByQ%3D&selectedQuizSessionId=" + \
            selectedQuizSessionId + "&scid=q7x6PiPCfek%3D"
        browser.execute_script("window.open()")
        browser.switch_to.window(browser.window_handles[1])
        browser.get(url)

        # browser.find_element_by
        # radio_btn.click()
        # browser.find_element_by_css_selector(
        #     'button#activeOkBtn').click()

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
        # browser.execute_script(
        #     "document.querySelector('div.cookie-bar').style.display = 'none'")
        while True:
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
                    if "Math" in title:
                        for item in p:
                            browser.execute_script(
                                "arguments[0].setAttribute('style', 'padding-bottom: 12px;')", item)
                    # elif "Math" not in title:
                    #     browser.execute_script(
                    #         "arguments[0].setAttribute('style', 'padding: 20px;')", p[0])
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
            print('screenshoting + ' + str(index_questions))
            # print('Simulating screenshot of question')
            index_questions = index_questions + 1
            browser.find_element_by_css_selector('div.next-tabs').click()
            if next_btn_exists() == False:
                correct = WebDriverWait(browser, 90).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.correct-answer-image')))
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
                # browser.find_element_by_css_selector('div.next-tabs').click()
                sus()
                browser.implicitly_wait(2)
                browser.save_screenshot(path)
                break
        # # print('Simulating screenshot of final question!')
        # correct.click()
        # # WebDriverWait(browser, 90).until(
        # #     EC.presence_of_element_located((By.CSS_SELECTOR, 'div#showCorrectAnswerContent.odt-panel-hidden-remove')))
        # # panel = WebDriverWait(browser, 90).until(
        # #     EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#showCorrectAnswerContent.animate-right-content')))
        # # browser.implicitly_wait(1)
        # # browser.execute_script(
        # #     "document.querySelector('iframe#correctQuizQuestionActivity').style.marginLeft = '10px'")
        # browser.implicitly_wait(5)
        # # browser.find_element_by_css_selector(
        # #     'iframe#correctQuizQuestionActivity').screenshot(path)

        # sus()
        # # browser.execute_script(
        # #     "document.querySelector('p.MsoNormal').style.padding = '15px'")
        # browser.save_screenshot(path)
        # browser.implicitly_wait(5)
        # crop()
        crop()

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

        browser.close()
        browser.switch_to.window(browser.window_handles[0])

        browser.find_element_by_css_selector('#activeCancelBtn').click()
        # browser.find_element_by_css_selector(
        #     'div[title="Finish Quiz"] button').click()
        # browser.implicitly_wait(3)
        # browser.get(
        #     'https://digitalplatform.sabis.net/Pages/ExamPreparation/ExamPreparation?a=&scid=q7x6PiPCfek%3D')
        # WebDriverWait(browser, 900).until(
        #     EC.element_to_be_clickable(
        #         (By.CSS_SELECTOR, """[ng-click="documentsCtrl.filterSelection('Week');"]""")))
    elif(radio_btn.is_displayed() == False):
        print('Quiz has not yet been attempted')
        browser.find_element_by_css_selector('button#activeCancelBtn').click()
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
    browser.execute_script(
        "document.querySelector('a.accept.button').click()")
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
