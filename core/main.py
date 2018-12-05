#!/usr/bin/env python
# coding:utf-8
# Author:Yang

from core.operation import login

class View(object):
    def __init__(self):
        pass
    def main_view(self):
        print('''------student manage-------
        ''')
        while True:
            user_name=input("请输入用户名：")
            user_pwd=input("请输入密码：")
            login(user_name,user_pwd)





def run():
    view=View()
    view.main_view()
