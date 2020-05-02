# _*_coding:utf-8_*_
# @Time     : 2020/5/2 下午2:01
# @Author   : Arics
# @Email    : 739386753@qq.com
# @File     : quequ_mysql.py.py
# @Software : PyCharm
# @IDE      : PyCharm

from sqlalchemy import Column, String, INTEGER, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class success(Base):
    __tablename__ = 'success'

    id = Column(INTEGER, primary_key=True)
    Url = Column(String(500), default="Opps")
    Type = Column(String(50), default="Opps")

engine = create_engine("mysql+pymysql://root:shashimima2013@localhost:3306/konachan")

DBSession = sessionmaker(bind=engine)


if __name__ == "__main__":
    session = DBSession()

    newSu = success(Url="https://www.baidu.com", Type="baidu")
    session.add(newSu)
    session.commit()

    session.close()
