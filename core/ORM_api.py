#!/usr/bin/env python
# coding:utf-8
# Author:Yang

from core import ORM_Create
from sqlalchemy.orm import sessionmaker


# Ssssion_class=sessionmaker(bind=ORM_Create.engine)
# session=Ssssion_class()


'''教师 ORM API'''




class ORM_API(object):
    def __init__(self):
        self.Session_class=sessionmaker(bind=ORM_Create.engine)
        self.session=self.Session_class()



    def init_insert(self):
        '''初始化插入数据'''

        '''创建老师'''
        t1=  ORM_Create.Teacher(tch_name='张三')
        t2 = ORM_Create.Teacher(tch_name='李四')
        t3 = ORM_Create.Teacher(tch_name='王五')
        self.session.add_all([t1,t2,t3])


        '''创建学生'''
        s1 = ORM_Create.Student(stu_name='杨浩然',stu_qq='562605133')
        s2 = ORM_Create.Student(stu_name='吴彦祖',stu_qq='123456789')
        s3 = ORM_Create.Student(stu_name='彭于晏',stu_qq='987654321')
        self.session.add_all([s1,s2,s3])

        '''创建账户'''
        u1 = ORM_Create.User(user_name='zs123',user_pwd='123456',user_type=1,user_tch_id=1)
        u2 = ORM_Create.User(user_name='ls123', user_pwd='123456', user_type=1, user_tch_id=2)
        u3 = ORM_Create.User(user_name='ww123', user_pwd='123456', user_type=1, user_tch_id=3)
        u4 = ORM_Create.User(user_name='yhr123', user_pwd='960314', user_type=2, user_stu_id=1)
        u5 = ORM_Create.User(user_name='pyy123', user_pwd='123456', user_type=2, user_stu_id=2)
        u6 = ORM_Create.User(user_name='wyz123', user_pwd='123456', user_type=2, user_stu_id=3)
        self.session.add_all([u1,u2,u3,u4,u5,u6])


        self.session.commit()



