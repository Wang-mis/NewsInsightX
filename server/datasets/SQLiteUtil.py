from collections import Counter

import pandas as pd
from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import or_

# from utils.helper import getEventRootCodeExplain, sortCustomDict
from server.utils.helper import getEventRootCodeExplain, sortCustomDict

engine = create_engine(
    'sqlite:///C:\\Programs\\github\\pleasenews\\helper\\SQLiteTest.db?check_same_thread=False',
    echo=True
)

Base = declarative_base()


# ORM模型，一个类对应数据库中的一张表，该类的一个实例对象对应表中的一条记录
class MergeItem(Base):
    __tablename__ = 'merge_table'  # 表名

    # 系统自带id 可自增
    AutoId = Column(Integer, primary_key=True)  # 一个属性对应表中的一个字段，Interger表示该属性的类型

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
    UniqueID = Column(String)


# 新闻表
class NewItem(Base):
    __tablename__ = 'new_table'

    # 系统自带id 可自增
    AutoId = Column(Integer, primary_key=True)

    # 为了唯一标记一篇新闻文章
    UniqueID = Column(String)
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

    # 系统自带id 可自增
    AutoId = Column(Integer, primary_key=True)
    # 为了唯一标记一篇新闻文章
    UniqueID = Column(String)
    Keyword = Column(Text)


def queryNewsByKeyword(args):
    print(args)

    page = args["page"]
    limit = args["limit"]
    offset_data = (page - 1) * limit

    keyword = '%' + args["keyword"] + '%'
    timerange = args["date"]

    Session = sessionmaker(bind=engine)
    session = Session()

    print(timerange)

    # 从数据库中查找相应记录
    query = (session.query(NewItem)
             .filter(NewItem.Content.ilike(keyword))  # 模糊搜索，不区分大小写
             .filter(or_(NewItem.DTime == timerange, timerange == '')))  # 匹配日期

    totalRecords = len(query.all())  # 获取记录条数

    # 按日期降序排序，获取当前页面的所有记录，results为NewItem对象的数组
    results = query.order_by(NewItem.DTime.desc()).offset(offset_data).limit(limit).all()

    # 将NewItem对象数组转化为字典的数组，便于以json的格式传给前端
    newsList = []
    for newItem in results:
        newsList.append({
            'AutoId': newItem.AutoId,
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
        "totalRecords": totalRecords,
        "newsList": newsList
    }


# 返回首页统计信息
def queryStatistics():
    data = {
        "MentionSourceName": [
            {"value": 1048, "name": 'bbc.com'},
            {"value": 735, "name": 'bbc.co.uk'},
            {"value": 580, "name": 'yahoo.com'},
            {"value": 484, "name": 'cnn.com'},
            {"value": 300, "name": 'nytime.com'}
        ],
        "ActorCountryCode": [
            {"value": 1048, "name": 'UKR'},
            {"value": 735, "name": 'USA'},
            {"value": 580, "name": 'GBR'},
            {"value": 484, "name": 'EUR'},
            {"value": 300, "name": 'RUS'}
        ],
        "EventRootCode": [
            {"value": 1048, "name": getEventRootCodeExplain(1)["concise"]},
            {"value": 735, "name": getEventRootCodeExplain(2)["concise"]},
            {"value": 580, "name": getEventRootCodeExplain(3)["concise"]},
            {"value": 484, "name": getEventRootCodeExplain(4)["concise"]},
            {"value": 300, "name": getEventRootCodeExplain(5)["concise"]}
        ],
        "MentionDocTone": [
            {"value": 1048, "name": 'POS'},
            {"value": 735, "name": 'NEG'},
            {"value": 580, "name": 'NEU'}
        ],
        "KeywordCloud": [],
    }

    # merge和new两个表的区别：new表的数据是从网络上爬取来的，merge的数据从数据集中读取，new表中包含文章内容。
    # 查询merge
    sql_merge = "SELECT * FROM merge_table"
    df_merge = pd.read_sql_query(sql_merge, engine)

    result_merge = df_merge.groupby("MentionSourceName").size().to_dict()  # 统计merge中各个媒体发布的新闻数量
    print(result_merge)

    # 查询news
    sql_new = "SELECT * FROM new_table"
    df_new = pd.read_sql_query(sql_new, engine)

    result_new = df_new.groupby("MentionSourceName").size().to_dict()  # 统计new中各个媒体发布的新闻数量
    print(result_new)

    df_inner = pd.merge(df_merge, df_new, how='inner', on='UniqueID')  # 使用内连接合并两个表，相当于扩充new表中的属性

    # NewsProportion
    data["NewsProportion"] = []
    data["NewsProportion"].append({
        "value": len(df_new),
        "name": "With Content"
    })
    data["NewsProportion"].append({
        "value": len(df_merge) - len(df_new),
        "name": "Without Content"
    })

    # MentionSourceName 每个新闻媒体发表的文章数量
    data["MentionSourceName"] = []
    sorted_dict = sortCustomDict(result_new)
    for key, value in sorted_dict.items():
        data["MentionSourceName"].append({
            "value": value,
            "name": key
        })
        if len(data["MentionSourceName"]) > 7:  # 只统计前8个新闻媒体
            break

    # ActorCountryCode 事件发生的国家，若CountryCode == ''，说明该事件与国家无关
    actorcountrycode = df_inner["Actor1CountryCode"].to_list() + df_inner["Actor2CountryCode"].to_list()
    sorted_dict = sortCustomDict(dict(Counter(actorcountrycode)))
    data["ActorCountryCode"] = []
    print("sorted_dict = " + str(sorted_dict))
    for key, value in sorted_dict.items():
        data["ActorCountryCode"].append({
            "value": value,
            "name": key
        })
        if len(data["ActorCountryCode"]) > 15:  # 只记录前16个国家（包括与国家无关）
            break

    # EventRootCode 每种事件类型的数量
    eventrootcode = df_inner["EventRootCode"].to_list()
    sorted_dict = sortCustomDict(dict(Counter(eventrootcode)))
    data["EventRootCode"] = []
    for key, value in sorted_dict.items():
        data["EventRootCode"].append({
            "value": value,
            "name": getEventRootCodeExplain(int(key))["concise"]
        })
        if len(data["EventRootCode"]) > 7:
            break

    # MentionDocTone 积极和消极事件的数量
    positive_count = len(df_inner[df_inner['MentionDocTone'] > 0])
    negative_count = len(df_inner[df_inner['MentionDocTone'] < 0])
    neutral_count = len(df_inner) - positive_count - negative_count
    mentiondoctone = {
        "POS": positive_count,
        "NEU": neutral_count,
        "NEG": negative_count,
    }
    sorted_dict = sortCustomDict(mentiondoctone)
    data["MentionDocTone"] = []
    for key, value in sorted_dict.items():
        data["MentionDocTone"].append({
            "value": value,
            "name": key
        })

    # KeywordCloud
    # 查询keyword
    sql_keyword = "SELECT * FROM keyword_table"
    df_keyword = pd.read_sql_query(sql_keyword, engine)
    Keywords = df_keyword["Keyword"].to_list()

    keywords = []
    for ele in Keywords:
        keywords += ele.split("|")  # 每个事件可能有多个关键词，关键词之间用|分隔

    sorted_dict = sortCustomDict(dict(Counter(keywords)))

    data["KeywordCloud"] = []
    for key, value in sorted_dict.items():
        data["KeywordCloud"].append({
            "value": value,
            "name": key
        })
        if len(data["KeywordCloud"]) > 60:
            break

    return data


def test():
    # 写一条sql
    sql = "SELECT COUNT(*) FROM new_table"
    # 建立dataframe
    df = pd.read_sql_query(sql, engine)
    print(df)


if __name__ == '__main__':
    # test()
    # args = {'keyword': '', 'date': '', 'page': 1, 'limit': 20, 'total': 0}
    # queryNewsByKeyword(args=args)
    pass
