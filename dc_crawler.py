from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from config import headers, url
import time


class DCinsideCrawler:

    def __init__(self):
        driver_dir = "C:/Dev/tools/chromedriver.exe"

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('lang=ko_KR')
        options.add_argument("--disable-gpu")

        self.driver = webdriver.Chrome(driver_dir, options=options)
        self.driver.implicitly_wait(2)

    def __parse_content(self, no):

        # params = {
        #     'id': 'ssu',
        #     'no': no
        # }
        # req = requests.get(url, params=params, headers=headers)
        #
        # print(req.url, ":", req.status_code)
        # if req.status_code != 200:
        #     return None
        # bs = BeautifulSoup(req.text, 'lxml')

        # Build Webdriver


        self.driver.get(f"{url}/?id=ssu&no={no}")

        # Parse page_source to BeautifulSoup
        bs = BeautifulSoup(self.driver.page_source, 'lxml')

        try:
            # Find component
            # 본문
            title = bs.find('span', class_="title_subject")
            title_text = title.text
            view_box = bs.find('div', class_="writing_view_box").find('div', attrs={'style': "overflow:hidden;width:900px"})
            content_text = view_box.text
            gall_date = bs.find('span', class_='gall_date').text


            # 댓글
            cmt_list = bs.find('ul', class_="cmt_list")

            nicknames = cmt_list.find_all('span', class_="gall_writer ub-writer")
            comment_contents = cmt_list.find_all('p', class_="usertxt ub-word")

            cmts = []
            for nickname, content in zip(nicknames, comment_contents):
                cmts.append({
                    "nickname": nickname.text,
                    "content": content.text
                })

            info = {
                "title": title_text,
                "content": content_text,
                "gallery_date": gall_date,
                "comments": cmts
            }

            return info
        except Exception as ex:
            print("Exception", ex)
            return None

    def get_data(self, min_gall_no=1, max_gall_no=10):
        data = {}
        for no in range(min_gall_no, max_gall_no + 1):
            info = self.__parse_content(no)

            if info is None:
                continue

            data[no] = info
        return data
