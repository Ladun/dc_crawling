from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from config import headers, url
import time
import json
import os


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
            view_box = bs.find('div', class_="writing_view_box").find('div',
                                                                      attrs={'style': "overflow:hidden;width:900px"})
            content_text = view_box.text
            gall_date = bs.find('span', class_='gall_date').text

            # 댓글
            cmt_list = bs.find('ul', class_="cmt_list")

            cmts = []
            if cmt_list != None:
                nicknames = cmt_list.find_all('span', class_="gall_writer ub-writer")
                comment_contents = cmt_list.find_all('p', class_="usertxt ub-word")
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

        json_data = {}
        for no in range(min_gall_no, max_gall_no):
            print(f"Parse {no} gallery")
            info = self.__parse_content(no)

            if info is None:
                continue

            json_data[no] = info
        return json_data

    def save_data(self, json_path, min_no=1, max_no=10, save_step=100):
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="UTF-8") as f:
                json_data = json.load(f)
        else:
            json_data = {}

        st = min_no

        while st < max_no:
            ed = min(st + save_step, max_no)
            info = self.get_data(st, ed)

            json_data.update(info)
            print(f"Save {json_path} ...")
            with open(json_path, "w", encoding="UTF-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent="\t")
            st = ed
