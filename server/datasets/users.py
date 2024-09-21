import random
from datetime import datetime, timedelta

from sqlalchemy import create_engine, Column, String, DateTime, Text, Float
from sqlalchemy.orm import declarative_base, sessionmaker

users_engine = create_engine(
    'sqlite:////home/wsx/remote/NewsInsightX/server/datasets/UsersDatabase.db?check_same_thread=False',
    echo=False
)

Base = declarative_base()


def create_token():
    s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choices(s, k=16))


# 用户登录数据表
class UserLoginData(Base):
    __tablename__ = 'user_login_data'

    username = Column(String, primary_key=True)
    password = Column(String)

    token = Column(String)
    token_store_time = Column(DateTime, default=datetime.now())
    token_store_hours = Column(Float)


# 用户信息表
class UserInfo(Base):
    __tablename__ = 'user_info'

    username = Column(String, primary_key=True)
    intro = Column(Text)

    def to_dict(self):
        return {
            'username': self.username,
            'intro': self.intro
        }


def add_user(username, password):
    session = sessionmaker(bind=users_engine)()
    try:
        Base.metadata.create_all(users_engine)
        exist_user = session.query(UserLoginData).filter_by(username=username).first()
        if exist_user:
            return 1, None
        token = create_token()
        new_user = UserLoginData(
            username=username,
            password=password,
            token=token,
            token_store_hours=24 * 7
        )
        new_user_info = UserInfo(
            username=username,
            intro=""
        )

        session.add(new_user)
        session.add(new_user_info)
        session.commit()
        session.close()
        return 0, token
    except Exception as e:
        print(e)
        session.rollback()
        session.close()
        return 100, None


# noinspection PyBroadException
def delete_user(username: str, password: str) -> int:
    session = sessionmaker(bind=users_engine)()
    try:
        Base.metadata.create_all(users_engine)

        exist_user = session.query(UserLoginData).filter_by(username=username).first()
        if not exist_user:
            return 2
        if exist_user.password != password:
            return 1
        session.delete(exist_user)
        session.commit()

        user_info = session.query(UserInfo).filter_by(username=username).first()
        if not user_info:
            return 2

        session.delete(user_info)
        session.commit()

        session.close()
        return 0
    except Exception as e:
        session.rollback()
        session.close()
        return 100


def check_user_token(token: str, update: bool = False) -> tuple:
    """
    检查用户传入的token
    token正确，code=0，user_info为用户数据
    token错误，code=1
    token过期，code=2
    其他未知错误，code=100
    """
    session = sessionmaker(bind=users_engine)()
    user = session.query(UserLoginData).filter_by(token=token).first()

    # token错误，返回1
    if not user:
        session.close()
        return 1, None

    # token过期，返回2
    if datetime.now() > user.token_store_time + timedelta(hours=user.token_store_hours):
        session.close()
        return 2, None

    # token验证成功，返回0
    # 更新token
    if update:
        user.token_store_time = datetime.now()
        session.commit()

    user_info = session.query(UserInfo).filter_by(username=user.username).first()
    if not user_info:
        session.close()
        return 100, None

    data = user_info.to_dict()
    session.close()
    return 0, data


# noinspection PyBroadException
def query_user(username: str, password: str, token_store_hours: float = 7 * 24) -> tuple:
    """
    根据用户名和密码查询用户，生成新的token
    正确，code=0
    密码错误，code=1
    用户不存在，code=2
    其他未知错误，code=100
    """
    session = sessionmaker(bind=users_engine)()
    try:
        Base.metadata.create_all(users_engine)
        exist_user = session.query(UserLoginData).filter_by(username=username).first()
        if not exist_user:
            session.close()
            return 2, None, None
        if exist_user.password != password:
            session.close()
            return 1, None, None

        # 生成新的token
        exist_user.token = create_token()
        exist_user.token_store_time = datetime.now()
        exist_user.token_store_hours = token_store_hours
        session.commit()

        # 查询用户信息
        user_info = session.query(UserInfo).filter_by(username=username).first()
        if not user_info:
            session.close()
            return 2, None, None

        data = user_info.to_dict()
        token = exist_user.token
        session.close()
        return 0, data, token
    except Exception as e:
        print(e)
        session.close()
        return 100, None, None
