#!/usr/bin/env python
# coding:utf-8
# Author:Yang


from sqlalchemy import Column,Table,Integer,String,DATE,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config.setting import DB_URL

engine=create_engine(DB_URL,echo=False)

Base=declarative_base(bind=engine)



'''教师表'''
class Teacher(Base):
    __tablename__='teacher'
    tch_id=Column(Integer,primary_key=True)  # 老师id
    tch_name=Column(String(64),nullable=False) # 老师姓名


'''学生-课程中间表'''
# stu_cls=Table("stu_cls",Base.metadata,
#               Column('stu_id',Integer,ForeignKey('student.stu_id')),
#               Column('cls_id',Integer,ForeignKey('class.cls_id')),
#               )
class STU_CLS(Base):
    __tablename__='stu_cls'
    id=Column(Integer,primary_key=True)
    stu_id=Column(Integer,ForeignKey('student.stu_id'))
    cls_id=Column(Integer,ForeignKey('class.cls_id'))


'''学生表'''
class Student(Base):
    __tablename__='student'
    stu_id=Column(Integer,primary_key=True) # 学生id
    stu_name=Column(String(64),nullable=False) # 学生姓名
    stu_qq=Column(String(64),nullable=False)  # 学生qq号


'''班级表'''
class Class(Base):
    __tablename__='class'
    cls_id=Column(Integer,primary_key=True) # 班级id
    cls_name=Column(String(64),nullable=False) # 班级名称
    cls_tch_id=Column(Integer,ForeignKey("teacher.tch_id")) # 老师id

    teacher = relationship('Teacher', backref='classes')
    student = relationship('Student', secondary='stu_cls', backref='classes')


'''学生上课记录表'''
class StudentRecord(Base):
    __tablename__='student_record'
    SR_id=Column(Integer,primary_key=True)
    SR_status=Column(String(64),nullable=False) # 上课状态：上课为yes 缺勤为no
    SR_stu_id=Column(Integer,ForeignKey('student.stu_id'))
    SR_hm_status=Column(String(64),nullable=False) # 作业状态：交了为yes 没交为no
    SR_hm_score=Column(Integer) #  作业分数

    student=relationship("Student",backref='student_record')


'''总上课记录表'''
class Record(Base):
    __tablename__='record'
    R_id=Column(Integer,primary_key=True)
    R_cls_id=Column(Integer,ForeignKey('class.cls_id')) # 班级id
    R_SR_id=Column(Integer,ForeignKey('student_record.SR_id')) # 学生课程记录表id
    R_tch_id=Column(Integer,ForeignKey('teacher.tch_id')) # 教师id
    R_day=Column(String(64),nullable=False) # 上课天数

    classes = relationship('Class',backref='record')
    student_record = relationship('StudentRecord',backref='record')
    teacher = relationship('Teacher',backref='record')


'''用户表'''
class User(Base):
    __tablename__='user'
    user_id=Column(Integer,primary_key=True)
    user_name=Column(String(64),nullable=False) # 用户名
    user_pwd=Column(String(64),nullable=False) # 密码
    user_type=Column(Integer,nullable=False) # 用户类型（1老师 2学生）
    user_stu_id=Column(Integer,ForeignKey("student.stu_id"))
    user_tch_id=Column(Integer,ForeignKey("teacher.tch_id"))


    teacher = relationship('Teacher',backref='user')
    student = relationship('Student',backref='user')




Base.metadata.create_all(engine)
