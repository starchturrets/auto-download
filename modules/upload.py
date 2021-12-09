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
            return '1hPz7QSpI1tAGGhn0OyBhv_iDPfuLTWrr'
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


def move_items_to_proper_folders():
    print('')


def list_all_files():
    def search():
        print()
# drive_service = login()

# results = drive_service.files.list()
