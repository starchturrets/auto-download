import download
import upload
import shutil
import os
import schedule
import time


def main():
    print('I am the main file! None shall stand my wrath!')

    shutil.rmtree('files')

    os.makedirs('files')

    current = download.main()
    print(current)

    upload.main(current)


if __name__ == '__main__':
    schedule.every().day.at("00:30").do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
