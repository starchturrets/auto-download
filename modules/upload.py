from __future__ import print_function
import requests
import shutil
import os
from os import walk
import pickle
import os.path
import googleapiclient
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def get_files(folder_title):
    term = 1
    print()
    terms = ['1uHWkp3CT4P5TtxH3NRG6wcXyJAwyhMNi',
             '1uIfZd7ytmW2Lw4KleyQYu9eNqh11QZKe',
             '1uNFUVkqp6Sf8HaRrlesZFurXf34RYfKh']
    # Where the downloaded files will be uploaded

    term_folder_id = terms[term - 1]

    def login():
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/drive']

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        drive_service = build('drive', 'v3', credentials=creds)
        return drive_service

    drive_service = login()

    # query_2 = query
    query = "mimeType = 'application/vnd.google-apps.folder' and '{term_folder_id}' in parents and trashed = False and name = '{query}'".format(
        term_folder_id=term_folder_id, query=folder_title)

    page_token = None

    try:
        while True:
            response = drive_service.files().list(q=query, spaces='drive',
                                                  fields='nextPageToken, files(id, name)', pageToken=page_token).execute()

            response_arr = response.get('files', [])

            if len(response_arr) == 0:
                print('Folder not found')
                return []

            elif len(response_arr) == 1:
                folder_id = response_arr[0].get('id')
                print('folder found!')
                # return folder_id
                items = []
                pageToken = None
                query = "'{folder_id}' in parents and trashed = False".format(
                        folder_id=folder_id)
                while True:
                    response = drive_service.files().list(q=query, spaces='drive',
                                                          fields='nextPageToken, files(id, name)', pageToken=pageToken).execute()

                    response_arr = response.get('files', [])
                    return response_arr
            # elif len(response_arr) > 1:
            #     print(
            #         'Something is not right. There are multiple duplicates of the folder!')
            #     folder_id = None

            # page_token = response.get('nextPageToken', None)
            # if page_token is None:
            #     return folder_id
            #     break
    except googleapiclient.errors.HttpError:
        print("ERROR")
        return None


def upload(term, heading):
    def login():
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/drive']

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        drive_service = build('drive', 'v3', credentials=creds)
        return drive_service

    drive_service = login()

    # terms = ['1HTJK3mwReWfJ0eXjfmsi8M7Hi9IvAglq',
    #          '12jnRx5q55rD4RLyE2GzPst8maYY4kEqC',
    #          '1aZtNfhjQnqGmG3WinT93HFUFvL204kmh']
    terms = ['1uHWkp3CT4P5TtxH3NRG6wcXyJAwyhMNi',
             '1uIfZd7ytmW2Lw4KleyQYu9eNqh11QZKe',
             '1uNFUVkqp6Sf8HaRrlesZFurXf34RYfKh']
    # Where the downloaded files will be uploaded

    term_folder_id = terms[term - 1]

    def find_folder(query, term_folder):
        if query == 'All Weeks':
            print('ALL WEEKS')
            return '1M_mH5chqKtZ1OBuw8bwbbHLTWYIxdMR7'
        elif query == 'Grid':
            print('GRID')
            return '1FN5avWUtt_b7lG1jfoFnwumIoD3oEYzs'
        query_2 = query
        query = "mimeType = 'application/vnd.google-apps.folder' and '{term_folder_id}' in parents and trashed = False and name = '{query}'".format(
            term_folder_id=term_folder_id, query=query)

        page_token = None

        def create_folder(item_name, id):
            body = {
                'name': item_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [id]
            }
            root_folder = drive_service.files().create(body=body).execute()
            print('Folder created!')
            return root_folder["id"]

        try:
            while True:
                response = drive_service.files().list(q=query, spaces='drive',
                                                      fields='nextPageToken, files(id, name)', pageToken=page_token).execute()

                response_arr = response.get('files', [])

                if len(response_arr) == 0:
                    print('Folder not found! Creating...')
                    folder_id = create_folder(query_2, term_folder)
                    return folder_id
                elif len(response_arr) == 1:
                    folder_id = response_arr[0].get('id')
                    print('folder found!')
                    return folder_id
                elif len(response_arr) > 1:
                    print(
                        'Something is not right. There are multiple duplicates of the folder!')
                    folder_id = None

                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    return folder_id
                    break
        except googleapiclient.errors.HttpError:
            return None

    target_id = find_folder(heading, term_folder_id)

    files = []
    for (dirpath, dirnames, filenames) in walk('./files'):
        files.extend(filenames)
        break

    if len(files) > 0:
        print(files)

    def upload_file(file_name, parent_id):
        print('Uploading file...')
        print(file_name)
        metadata = {
            "name": file_name,
            "parents": [parent_id]
        }
        location = './files/{file}'.format(file=file_name)
        media = googleapiclient.http.MediaFileUpload(
            location, mimetype='application/pdf')

        file = drive_service.files().create(body=metadata,
                                            media_body=media,
                                            fields='id').execute()
        print('File ID: %s' % file.get('id'))

    for file in files:
        upload_file(str(file), target_id)

    shutil.rmtree('files')

    os.makedirs('files')


def login():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/drive']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../token.pickle'):
        with open('../token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service


def move_all_weeks_to_proper_folders():
    print()
    all_weeks = []
    MONDAY = ''
    TUESDAY = ''
    WEDNESDAY = ''
    THURSDAY = ''
    FRIDAY = ''


def move_items_to_proper_folders(term):

    def login():
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/drive']

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('/home/james/programming/auto-download/token.pickle'):
            with open('/home/james/programming/auto-download/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '../credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('../token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        drive_service = build('drive', 'v3', credentials=creds)
        return drive_service
    terms = ['1uHWkp3CT4P5TtxH3NRG6wcXyJAwyhMNi',
             '1uIfZd7ytmW2Lw4KleyQYu9eNqh11QZKe',
             '1uNFUVkqp6Sf8HaRrlesZFurXf34RYfKh']
    # Where the downloaded files will be uploaded

    term_folder_id = terms[term - 1]
    drive_service = login()
    arr = []

    def search(query):
        # print()
        response = None
        page_token = None
        # query_2 = "trashed = false " + ""
        query_2 = f'trashed = false and "{query}" in parents'
        while True:
            response = drive_service.files().list(
                q=query_2, spaces='drive', fields="nextPageToken, files(id, name, mimeType)", pageToken=page_token).execute()
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return response.get('files', [])

    weeks = search(term_folder_id)

    def find_folder(query, parent_folder):

        query_2 = query
        query = "mimeType = 'application/vnd.google-apps.folder' and '{parent_folder}' in parents and trashed = False and name = '{query}'".format(
            parent_folder=parent_folder, query=query)

        page_token = None

        def create_folder(item_name, id):
            body = {
                'name': item_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [id]
            }
            root_folder = drive_service.files().create(body=body).execute()
            print('Folder created!')
            return root_folder["id"]

        try:
            while True:
                response = drive_service.files().list(q=query, spaces='drive',
                                                      fields='nextPageToken, files(id, name)', pageToken=page_token).execute()

                response_arr = response.get('files', [])

                if len(response_arr) == 0:
                    print('Folder not found! Creating...')
                    folder_id = create_folder(query_2, parent_folder)
                    return folder_id
                elif len(response_arr) == 1:
                    folder_id = response_arr[0].get('id')
                    # print('folder found!')
                    return folder_id
                elif len(response_arr) > 1:
                    print(
                        'Something is not right. There are multiple duplicates of the folder!')
                    folder_id = None

                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    return folder_id
                    break
        except googleapiclient.errors.HttpError:
            return None
    for week in weeks:
        print(week['name'])
        id = week['id']
        # SUNDAY = find_folder('SUNDAY', id)
        MONDAY = find_folder('MONDAY', id)
        TUESDAY = find_folder('TUESDAY', id)
        WEDNESDAY = find_folder('WEDNESDAY', id)
        THURSDAY = find_folder('THURSDAY', id)
        FRIDAY = find_folder('FRIDAY', id)
        SATURDAY = find_folder('SATURDAY', id)

        files = search(id)

        def move(file_id, old_parent_id, new_parent_id):
            file = drive_service.files().update(
                fileId=file_id, addParents=new_parent_id, removeParents=old_parent_id, fields='id, parents').execute()

        for file in files:
            name = file['name']
            name = "".join(name.lower().split())
            id = file['id']
            if 'mock' not in name and 'final' not in name:
                if 'periodic' in name:
                    print('moving monday')
                    # previous_parents = ','.join(file.get('parents'))
                    if 'alevel' in ''.join(name.lower().split()):
                        print('saturday')
                        # file = drive_service.files().update(
                        #     fileId=file['id'], addParents=SATURDAY, removeParents=week['id'], fields='id, parents').execute()
                        move(file['id'], week['id'], SATURDAY)
                    else:
                        print('sunday')
                        file = drive_service.files().update(
                            fileId=file['id'], addParents=MONDAY, removeParents=week['id'], fields='id, parents').execute()
                elif 'math' in name or 'moral' in name  or 'apstatistics' in name:
                    print('tuesday')
                    move(file['id'], week['id'], TUESDAY)
                elif 'levelchemistry' in name or 'economics' in name or 'biology' in name:
                    print('wednesday')
                    move(file['id'], week['id'], WEDNESDAY)
                elif 'asstatistics' in name or 'nchemistry' in name or 'alevelphysics' in name or 'apcomputerscience' in name or 'apphysicsc' in name:
                    print('thursday')
                    move(file['id'], week['id'], THURSDAY)
                elif 'history' in name or 'physics' in name or 'business' in name:
                    print('friday')
                    move(file['id'], week['id'], FRIDAY)


def list_all_files(term):

    def login():
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/drive']

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('/home/james/programming/auto-download/token.pickle'):
            with open('/home/james/programming/auto-download/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '../credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('../token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        drive_service = build('drive', 'v3', credentials=creds)
        return drive_service
    terms = ['1uHWkp3CT4P5TtxH3NRG6wcXyJAwyhMNi',
             '1uIfZd7ytmW2Lw4KleyQYu9eNqh11QZKe',
             '1uNFUVkqp6Sf8HaRrlesZFurXf34RYfKh']
    # Where the downloaded files will be uploaded

    folder_id = terms[term - 1]
    drive_service = login()
    arr = []

    def search(query):
        # print()
        response = None
        page_token = None
        # query_2 = "trashed = false " + ""
        query_2 = f'trashed = false and "{query}" in parents'
        while True:
            response = drive_service.files().list(
                q=query_2, spaces='drive', fields="nextPageToken, files(id, name, mimeType)", pageToken=page_token).execute()
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return response.get('files', [])
    files = search(folder_id)
# when u forget recursion

    def recursion(files):
        for item in files:
            if item.get('mimeType') != 'application/vnd.google-apps.folder':
                arr.append(item.get('name'))
            elif item.get('mimeType') == 'application/vnd.google-apps.folder':
                sub_folder = search(item.get('id'))
                recursion(sub_folder)

    recursion(files)
    all_weeks = '1M_mH5chqKtZ1OBuw8bwbbHLTWYIxdMR7'
    schedules = '1wV3A0vvZFGy5ZsP5YlxBYsWE_N6Lg8Mq'
    grid = '1FN5avWUtt_b7lG1jfoFnwumIoD3oEYzs'
    other_folders = [all_weeks, schedules, grid]
    for other_folder in other_folders:
        recursion(search(other_folder))
    sus = []
    for file_name in arr:
        # print(file_name)
        str = file_name.split('.pdf')[0]
        sus.append("".join(str.split()))

    return sus
# drive_service = login()

# results = drive_service.files.list()


# list_all_files('1uHWkp3CT4P5TtxH3NRG6wcXyJAwyhMNi')
# move_items_to_proper_folders(1)
