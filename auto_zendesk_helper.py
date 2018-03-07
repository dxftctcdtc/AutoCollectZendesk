#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Copyright 2018 Francis Xufan Du - BEYONDSOFT INC.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Created on Thu Jan 18 14:06:16 2018

@author: Francis Xufan Du - BEYONDSOFT INC.
@email: duxufan@beyondsoft.com xufan.du@gmail.com
@Version: 	03/2018 0.6-Beta:   1. update the tool to only collect the necessary data
                                2. change database updating logic (old way: delete all and re-create new table,
                                new way: update or insert)
                                3. fix bugs
            02/2018 0.5-Beta: separate crawling logic and database logic
            02/2018 0.4-Beta: add database update recording
            02/2018 0.3-Beta: add users and topics data collecting
            01/2018 0.2-Beta: add database storage
            01/2018 0.1-Beta: build zendesk auto collect function

"""

# core mods
import time
import os
import re
import shutil
import xlrd


class AutoZendeskHelper(object):
    def __init__(self):
        """
        initial method
        """
        self._save_path = os.path.abspath('.') + '\\'
        self._shared_folder = '\\\\192.168.8.55\\ISV-Share\\FrancisDu\\sourcecode\\'
        self._ISV_POSTS_LIST_PATH = r'D:\workspace_Francis_Du\PycharmProjects\zendesk\ISV SDK Support_Posts List.xlsx'

    def read_xlsx(self):
        workbook = xlrd.open_workbook(self._ISV_POSTS_LIST_PATH)
        book_sheet = workbook.sheet_by_name('OXPdNetJava Posts')
        p = list()

        for row in range(book_sheet.nrows):
            row_data = []
            for col in range(book_sheet.ncols):
                cel = book_sheet.cell(row, col)
                try:
                    val = cel.value
                    val = re.sub(r'\s+', '', val)
                except:
                    pass

                if type(val) == float:
                    val = int(val)
                else:
                    val = str(val)
                row_data.append(val)
            p.append([row_data[0][1:], row_data[4]])
        return p

    def _remove_json_posts_files(self):
        """
        remove generated json file(s)
        """
        for root, dirs, files in os.walk(self._save_path):
            for file in files:
                if file[:3] == 'pos':
                    os.remove(file)
        print("removing posts json files ...")

    def _remove_json_comments_files(self):
        """
        remove generated json file(s)
        """
        for root, dirs, files in os.walk(self._save_path):
            for file in files:
                if file[:3] == 'com':
                    os.remove(file)
        print("removing comments json files ...")

    def _remove_json_users_topics_files(self):
        """
        remove generated json file(s)
        """
        for root, dirs, files in os.walk(self._save_path):
            for file in files:
                if file[:3] == 'use':
                    os.remove(file)
        if os.path.exists(self._save_path + 'topics.json'):
            os.remove(self._save_path + 'topics.json')

    def remove_all_json_files(self):
        for r in os.listdir(self._save_path):
            if os.path.isfile(r):
                if re.match('^post.*.json', r) or re.match('^comment.*.json', r) or\
                        re.match('^user.*.json', r) or re.match('^topic.*.json', r):
                    os.remove(r)

    def move_json_from_shared_folder(self):
        for file in os.listdir(self._shared_folder):
            source = os.path.join(self._shared_folder, file)
            if os.path.isfile(source) and re.match(r'^.*.json', file):
                shutil.copyfile(source, os.path.join(self._save_path, file))
                os.remove(source)

    def move_json_to_shared_folder(self):
        for file in os.listdir(self._save_path):
            source = os.path.join(self._save_path, file)
            if os.path.isfile(source) and re.match(r'^.*.json', file):
                shutil.copyfile(source, os.path.join(self._shared_folder, file))
                os.remove(source)

    def move_excel(self):
        des1 = 'D:\\workspace_Francis_Du\\PycharmProjects\\mysite\\static\\docs\\'
        des2 = '\\\\192.168.8.55\\ISV-Share\\FrancisDu\\zendeskRecords\\'

        t = time.localtime()
        year = str(t.tm_year)
        month = str(t.tm_mon)
        if len(month) < 2:
            month = '0' + month
        day = str(t.tm_mday)
        if len(day) < 2:
            day = '0' + day

        post_name = '_'.join((str(year), str(month), str(day)))
        post_name = ''.join(('posts_', post_name, '.xls'))
        com_name = '_'.join((str(year), str(month), str(day)))
        com_name = ''.join(('comments_', com_name, '.xls'))

        shutil.copyfile(self._save_path + post_name, des1 + post_name)
        shutil.copyfile(self._save_path + post_name, des2 + post_name)
        shutil.copyfile(self._save_path + com_name, des1 + com_name)
        shutil.copyfile(self._save_path + com_name, des2 + com_name)
        os.remove(self._save_path + post_name)
        os.remove(self._save_path + com_name)

    def run_remove_json_files(self):
        self._remove_json_posts_files()
        self._remove_json_comments_files()
        self._remove_json_users_topics_files()
