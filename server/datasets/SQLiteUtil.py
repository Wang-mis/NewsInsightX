from collections import Counter
from operator import and_

import pandas as pd
from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# from server.utils.helper import get_event_root_code_explain, sort_dict_by_value
from utils.helper import get_event_root_code_explain, sort_dict_by_value

engine = create_engine(
    # 'sqlite:///D:\\Programs\\github\\pleasenews\\helper\\SQLiteTest.db?check_same_thread=False',
    # 'sqlite:///C:\\Programs\\github\\pleasenews\\helper\\SQLiteTest.db?check_same_thread=False',
    # 'sqlite:////home/wsx/remote/pleasenews/helper/SQLiteTest.db?check_same_thread=False',
    'sqlite:////home/wsx/pleasenews/helper/SQLiteTest.db?check_same_thread=False',
    echo=False
)

Base = declarative_base()


class MergeItem(Base):
    __tablename__ = 'merge_table'  # 表名

    GlobalEventID = Column(Integer)
    Day = Column(Integer)
    MonthYear = Column(Integer)
    Year = Column(Integer)
    FractionDate = Column(Float)

    Actor1Code = Column(String)
    Actor1Name = Column(String)
    Actor1CountryCode = Column(String)
    Actor1KnownGroupCode = Column(String)
    Actor1EthnicCode = Column(String)
    Actor1Religion1Code = Column(String)
    Actor1Religion2Code = Column(String)
    Actor1Type1Code = Column(String)
    Actor1Type2Code = Column(String)
    Actor1Type3Code = Column(String)

    Actor2Code = Column(String)
    Actor2Name = Column(String)
    Actor2CountryCode = Column(String)
    Actor2KnownGroupCode = Column(String)
    Actor2EthnicCode = Column(String)
    Actor2Religion1Code = Column(String)
    Actor2Religion2Code = Column(String)
    Actor2Type1Code = Column(String)
    Actor2Type2Code = Column(String)
    Actor2Type3Code = Column(String)

    IsRootEvent = Column(Integer)
    EventCode = Column(Integer)
    EventBaseCode = Column(Integer)
    EventRootCode = Column(Integer)
    QuadClass = Column(Integer)

    GoldsteinScale = Column(Float)

    NumMentions = Column(Integer)
    NumSources = Column(Integer)
    NumArticles = Column(Integer)

    AvgTone = Column(Float)

    Actor1Geo_Type = Column(Integer)
    Actor1Geo_Fullname = Column(String)
    Actor1Geo_CountryCode = Column(String)
    Actor1Geo_ADM1Code = Column(String)
    Actor1Geo_Lat = Column(String)
    Actor1Geo_Long = Column(String)
    Actor1Geo_FeatureID = Column(String)

    Actor2Geo_Type = Column(Integer)
    Actor2Geo_Fullname = Column(String)
    Actor2Geo_CountryCode = Column(String)
    Actor2Geo_ADM1Code = Column(String)
    Actor2Geo_Lat = Column(String)
    Actor2Geo_Long = Column(String)
    Actor2Geo_FeatureID = Column(String)

    ActionGeo_Type = Column(Integer)
    ActionGeo_Fullname = Column(String)
    ActionGeo_CountryCode = Column(String)
    ActionGeo_ADM1Code = Column(String)
    ActionGeo_Lat = Column(String)
    ActionGeo_Long = Column(String)
    ActionGeo_FeatureID = Column(String)

    DATEADDED = Column(Integer)
    SOURCEURL = Column(String)

    EventTimeDate = Column(Integer)
    MentionTimeDate = Column(Integer)
    MentionType = Column(Integer)

    MentionSourceName = Column(String)
    MentionIdentifier = Column(String)

    SentenceID = Column(Integer)
    Actor1CharOffset = Column(Integer)
    Actor2CharOffset = Column(Integer)
    ActionCharOffset = Column(Integer)
    InRawText = Column(Integer)
    Confidence = Column(Integer)
    MentionDocLen = Column(Integer)

    MentionDocTone = Column(Float)
    MentionDocTranslationInfo = Column(String)
    Extras = Column(String)

    # 为了唯一标记一篇新闻文章
    UniqueID = Column(String, primary_key=True)


# 新闻表
class NewItem(Base):
    __tablename__ = 'new_table'

    UniqueID = Column(String, primary_key=True)
    Title = Column(String)
    Author = Column(String)
    PTime = Column(String)
    DTime = Column(Integer)
    MentionSourceName = Column(String)
    MentionIdentifier = Column(String)
    Content = Column(Text)

    def to_dict(self):
        return {
            'UniqueID': self.UniqueID,
            'Title': self.Title,
            'Author': self.Author,
            'PTime': self.PTime,
            'DTime': self.DTime,
            'MentionSourceName': self.MentionSourceName,
            'MentionIdentifier': self.MentionIdentifier,
            'Content': self.Content
        }


# 关键词表
class KeywordItem(Base):
    __tablename__ = 'keyword_table'

    UniqueID = Column(String, primary_key=True)
    Keyword = Column(Text)


# 用户信息表
class UserItem(Base):
    __tablename__ = 'userinfo'

    username = Column(String, primary_key=True)
    password = Column(String)
    intro = Column(Text)


# noinspection PyUnresolvedReferences
def query_news_by_keyword(args):
    page = args["page"]
    limit = args["limit"]
    offset_data = (page - 1) * limit
    keyword = '%' + args["keyword"] + '%'
    timerange = args["date"]

    if isinstance(timerange, list):
        start_time = int(timerange[0])
        end_time = int(timerange[1])
    else:
        start_time = 00000000
        end_time = 99999999

    print("按关键词和时间段查找文章，"
          "Keyword = " + keyword +
          ", Start Time = " + str(start_time) +
          ", End Time = " + str(end_time) +
          ", Page = " + str(page) +
          ", Limit = " + str(limit))

    # 从数据库中查找相应记录
    session = sessionmaker(bind=engine)()
    query = (session.query(NewItem)
             .filter(NewItem.Content.ilike(keyword))  # 模糊搜索，不区分大小写
             .filter(and_(NewItem.DTime >= start_time, NewItem.DTime <= end_time)))  # 匹配日期

    total_records = len(query.all())  # 获取记录条数

    # 按日期降序排序，获取当前页面的所有记录，results为NewItem对象的数组
    results = query.order_by(NewItem.DTime.desc()).offset(offset_data).limit(limit).all()

    # 将NewItem对象数组转化为字典的数组，便于以json的格式传给前端
    news_list = []
    for newItem in results:
        news_list.append({
            'UniqueID': newItem.UniqueID,
            'Title': newItem.Title,
            'Author': newItem.Author,
            'PTime': newItem.PTime,
            'DTime': newItem.DTime,
            'MentionSourceName': newItem.MentionSourceName,
            'MentionIdentifier': newItem.MentionIdentifier,
            'Content': newItem.Content
        })

    session.commit()
    session.close()

    # 将总记录数和当前页面的所有记录数据传给前端
    return {
        "totalRecords": total_records,
        "newsList": news_list
    }


# 缓存统计数据
statistics_data = {
    'updated': False
}


# 返回首页统计信息
def query_statistics(force_update=False):
    global statistics_data

    if force_update:
        statistics_data['updated'] = False

    print("请求统计数据。")
    if statistics_data['updated']:
        print("已缓存统计数据。")
        return statistics_data

    print("未缓存统计数据，重新计算。")
    # merge和new两个表的区别：new表的数据是从网络上爬取来的，merge的数据从数据集中读取，new表中包含文章内容。
    df_merge = pd.read_sql_query("SELECT * FROM merge_table", engine)
    df_new = pd.read_sql_query("SELECT * FROM new_table", engine)
    # 使用内连接合并两个表，相当于扩充new表中的属性
    df_inner = pd.merge(df_merge, df_new, how='inner', on='UniqueID')

    # NewsProportion
    statistics_data["NewsProportion"] = []
    statistics_data["NewsProportion"].append({
        "value": len(df_new),
        "name": "With Content"
    })
    statistics_data["NewsProportion"].append({
        "value": len(df_merge) - len(df_new),
        "name": "Without Content"
    })

    # MentionSourceName 每个新闻媒体发表的文章数量
    count_sources = df_new.groupby("MentionSourceName").size().to_dict()  # 统计new中各个媒体发布的新闻数量
    statistics_data["MentionSourceName"] = []
    count_sources_sorted = sort_dict_by_value(count_sources, reverse=True)  # 按媒体发布新闻数量降序排序

    now_count = 0
    for key, value in count_sources_sorted.items():
        statistics_data["MentionSourceName"].append({
            "value": value,
            "name": key
        })
        now_count += value
        if len(statistics_data["MentionSourceName"]) > 6:  # 只统计前7个新闻媒体
            statistics_data["MentionSourceName"].append({
                "value": len(df_new) - now_count,
                "name": "others"
            })
            break

    # ActorCountryCode 事件发生的国家，若CountryCode == ''，说明该事件与国家无关
    countries = df_inner["Actor1CountryCode"].to_list() + df_inner["Actor2CountryCode"].to_list()
    count_countries_sorted = sort_dict_by_value(dict(Counter(countries)))
    statistics_data["ActorCountryCode"] = []

    now_count = 0
    for key, value in count_countries_sorted.items():
        name = key if key != "" else "NONE"
        statistics_data["ActorCountryCode"].append({
            "value": value,
            "name": name
        })
        now_count += value
        if len(statistics_data["ActorCountryCode"]) > 14:  # 只记录前15个国家（包括与国家无关）
            statistics_data["ActorCountryCode"].append({
                "value": len(countries) - now_count,
                "name": "OTHERS"
            })
            break

    # EventRootCode 每种事件类型的数量
    rootcodes = df_inner["EventRootCode"].to_list()
    count_rootcodes_sorted = sort_dict_by_value(dict(Counter(rootcodes)))
    statistics_data["EventRootCode"] = []

    now_count = 0
    for key, value in count_rootcodes_sorted.items():
        statistics_data["EventRootCode"].append({
            "value": value,
            "name": get_event_root_code_explain(int(key))["concise"]
        })
        now_count += value

        if len(statistics_data["EventRootCode"]) > 6:
            statistics_data["EventRootCode"].append({
                "value": len(rootcodes) - now_count,
                "name": "OTHERS"
            })
            break

    # MentionDocTone 积极和消极事件的数量
    positive_count = len(df_inner[df_inner['MentionDocTone'] > 0])
    negative_count = len(df_inner[df_inner['MentionDocTone'] < 0])
    neutral_count = len(df_inner) - positive_count - negative_count
    mention_doctone = {
        "POS": positive_count,
        "NEU": neutral_count,
        "NEG": negative_count,
    }
    count_doctone_sorted = sort_dict_by_value(mention_doctone)
    statistics_data["MentionDocTone"] = []
    for key, value in count_doctone_sorted.items():
        statistics_data["MentionDocTone"].append({
            "value": value,
            "name": key
        })

    # KeywordCloud
    df_keyword = pd.read_sql_query("SELECT * FROM keyword_table", engine)
    keywords_all = df_keyword["Keyword"].to_list()

    keywords = []
    for ele in keywords_all:
        keywords += ele.split("|")  # 每个事件可能有多个关键词，关键词之间用|分隔

    count_keywords_sorted = sort_dict_by_value(dict(Counter(keywords)))

    statistics_data["KeywordCloud"] = []
    for key, value in count_keywords_sorted.items():
        statistics_data["KeywordCloud"].append({
            "value": value,
            "name": key
        })
        if len(statistics_data["KeywordCloud"]) > 60:
            break

    statistics_data['updated'] = True
    return statistics_data


def add_user(username, password, intro=""):
    session = sessionmaker(bind=engine)()
    try:
        Base.metadata.create_all(engine)
        exist_user = session.query(UserItem).filter_by(username=username).first()
        if exist_user:
            return 1
        new_user = UserItem(username=username, password=password, intro=intro)
        session.add(new_user)
        session.commit()
        return 0
    except Exception as e:
        print(e)
        session.rollback()
        return 100


def delete_user(username, password):
    session = sessionmaker(bind=engine)()
    try:
        Base.metadata.create_all(engine)
        exist_user = session.query(UserItem).filter_by(username=username).first()
        if not exist_user:
            return 2
        if exist_user.password != password:
            return 1
        session.delete(exist_user)
        session.commit()
        return 0
    except Exception as e:
        session.rollback()
        return 100


def query_user(username, password):
    session = sessionmaker(bind=engine)()
    try:
        Base.metadata.create_all(engine)
        exist_user = session.query(UserItem).filter_by(username=username).first()
        if not exist_user:
            return 2, None
        if exist_user.password != password:
            return 1, None
        return 0, exist_user
    except Exception as e:
        return 100, None
