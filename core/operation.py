#!/usr/bin/env python
# coding:utf-8
# Author:Yang

from core import ORM_Create
from sqlalchemy.orm import sessionmaker

Session_class=sessionmaker(bind=ORM_Create.engine)
session=Session_class()

name_list=[]
class_list=[]
student_list=[]
day_list = []
user_obj_list=session.query(ORM_Create.User.user_name).all()
student_obj_list=session.query(ORM_Create.Student.stu_name,ORM_Create.Student.stu_qq).all()
for i in range(len(student_obj_list)):
    student_list.append(student_obj_list[i][0]+" qq:"+student_obj_list[i][1])

for i in range(len(user_obj_list)):
    name_list.append(user_obj_list[i][0])

def login(user_name,user_pwd):


     if user_name in name_list:
        user_obj=session.query(ORM_Create.User).filter(ORM_Create.User.user_name==user_name).first()
        if user_pwd==user_obj.user_pwd:
             if user_obj.user_type==1:
                 teacher_view(user_obj)
             else:
                 student_view(user_obj)
        else:
            print("密码错误")
     else:
         print("用户名错误")

def teacher_view(user_obj):
    teacher_obj=session.query(ORM_Create.Teacher).filter(ORM_Create.Teacher.tch_id==user_obj.user_tch_id).first()

    print('''-------Welcome teacher:%s----------
    1.创建班级
    2.将学员加入班级
    3.创建班级上课记录
    4.批改成绩
    '''%teacher_obj.tch_name)

    choice=int(input("请输入选项:"))
    if choice ==1:
        class_name=input("请输入要创建的班级名称:")
        c1=ORM_Create.Class(cls_name=class_name,cls_tch_id=teacher_obj.tch_id)
        session.add_all([c1])
        session.commit()
        print("创建成功")
        print("------班级列表------")
        class_obj_list=session.query(ORM_Create.Class.cls_name).all()
        for i in range(len(class_obj_list)):
            class_list.append(class_obj_list[i][0])
        for index,cls in enumerate(class_list):
            print(index+1,cls)
        teacher_view(user_obj)

    elif choice == 2:
        print("-----学生列表------")
        for index,stu in enumerate(student_list):
            print(index+1,stu)
        qq_number=int(input("请输入学生qq号"))
        stu_id=(session.query(ORM_Create.Student).filter(ORM_Create.Student.stu_qq==qq_number).first().stu_id)
        print("------班级列表------")
        class_obj_list = session.query(ORM_Create.Class.cls_name).all()
        for i in range(len(class_obj_list)):
            class_list.append(class_obj_list[i][0])
        for index, cls in enumerate(class_list):
            print(index + 1, cls)
        class_name=input("请输入要添加到的班级名称:")
        cls_id=(session.query(ORM_Create.Class).filter(ORM_Create.Class.cls_name==class_name).first().cls_id)
        cls1=ORM_Create.STU_CLS(stu_id=stu_id,cls_id=cls_id)
        session.add_all([cls1])
        session.commit()
        print("添加成功")
        teacher_view(user_obj)

    elif choice==3:
        print("------创建上课记录------")
        class_name=input("请输入当前课程名字:")
        day=input("请输入当前日期:")
        cls_obj=session.query(ORM_Create.Class).filter(ORM_Create.Class.cls_name == class_name).first()
        cls_id = cls_obj.cls_id
        stu_obj_list=cls_obj.student
        for stu_obj in stu_obj_list:
            stu_id=stu_obj.stu_id
            sr1=ORM_Create.StudentRecord(SR_status=1,SR_stu_id=stu_id,SR_hm_status="no")
            session.add_all([sr1])
            session.commit()
            sr_id=(session.query(ORM_Create.StudentRecord).filter(ORM_Create.StudentRecord.SR_stu_id==stu_id).first()).SR_id
            r1=ORM_Create.Record(R_cls_id=cls_id,R_SR_id=sr_id,R_tch_id=teacher_obj.tch_id,R_day=day)
            session.add_all([r1])
            session.commit()
        print("创建成功")
        teacher_view(user_obj)

    elif choice ==4:
        print("----修改成绩----")
        for index,stu in enumerate(student_list):
            print(index+1,stu)
        stu_choice=input("请输入姓名:")
        stu_obj=session.query(ORM_Create.Student).filter(ORM_Create.Student.stu_name==stu_choice).first()

        class_obj_list=stu_obj.classes
        print("-----课程列表-------")
        for index,cls_obj in enumerate(class_obj_list):
            print(index+1,cls_obj.cls_name)
        cls_choice=input("请选择课程:")

        for cls_obj in class_obj_list:
            if cls_obj.cls_name==cls_choice:
                R_obj_list=cls_obj.record
                for index,R_obj in enumerate(R_obj_list):
                    print(index+1,R_obj.R_day)
                day_choice = input("请输入day几:")
                score = input("请输入成绩：")
                for R_obj in R_obj_list:
                    if R_obj.R_day==day_choice:
                        SR_obj=R_obj.student_record
                        session.query(ORM_Create.StudentRecord).filter(ORM_Create.StudentRecord.SR_id == SR_obj.SR_id).update(
                            {ORM_Create.StudentRecord.SR_hm_score: score})
                        session.commit()
                        print("修改成功")
                        teacher_view(user_obj)


    else:
        print("输入错误")




def student_view(user_obj):
    student_obj = session.query(ORM_Create.Student).filter(ORM_Create.Student.stu_id == user_obj.user_stu_id).first()
    print('''-------Welcome student:%s----------
       1.提交作业
       2.查看作业成绩
       
       ''' % student_obj.stu_name)

    choice=int(input("请输入选项:"))
    if choice==1:
        print('''-------选择班级----------
              ''' )
        class_obj_list = session.query(ORM_Create.Class.cls_name).all()
        for i in range(len(class_obj_list)):
            class_list.append(class_obj_list[i][0])
        for index, cls in enumerate(class_list):
            print(index + 1, cls)
        class_choice=input("请选择班级:")
        class_obj_list=student_obj.classes
        for class_obj in class_obj_list:
            if class_obj.cls_name == class_choice:
                R_obj_list=class_obj.record
                for index,R_obj in enumerate(R_obj_list):
                    SR_obj=R_obj.student_record

                    print(index+1,R_obj.R_day+" 作业状态："+SR_obj.SR_hm_status)
                day_choice=input("请输入日期来提交作业:")
                R_obj_list=session.query(ORM_Create.Record).filter(ORM_Create.Record.R_day==day_choice).all()
                for R_obj in R_obj_list:
                    SR_obj=R_obj.student_record
                    session.query(ORM_Create.StudentRecord).filter(ORM_Create.StudentRecord.SR_id==SR_obj.SR_id,ORM_Create.StudentRecord.SR_stu_id==student_obj.stu_id).update({ORM_Create.StudentRecord.SR_hm_status:"yes"})
                    session.commit()
                    print("提交完成")
        student_view(user_obj)

    elif choice==2:
        print('''-------选择班级----------
                      ''')
        class_obj_list = session.query(ORM_Create.Class.cls_name).all()
        for i in range(len(class_obj_list)):
            class_list.append(class_obj_list[i][0])
        for index, cls in enumerate(class_list):
            print(index + 1, cls)
        class_choice = input("请选择班级:")
        class_obj_list = student_obj.classes
        for class_obj in class_obj_list:
            if class_obj.cls_name == class_choice:
                R_obj_list = class_obj.record
                for index, R_obj in enumerate(R_obj_list):
                    SR_obj = R_obj.student_record

                    print(index + 1, R_obj.R_day + " 作业成绩：" + str(SR_obj.SR_hm_score))

        student_view(user_obj)


