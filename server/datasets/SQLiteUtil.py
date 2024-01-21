from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DECIMAL, Float, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import or_
import pandas as pd
from utils.helper import getEventRootCodeExplain


engine = create_engine('sqlite:///E:\\Projects\\pleasenews\\helper\\SQLiteTest.db?check_same_thread=False', echo=True)

Base = declarative_base()

class MergeItem(Base):
    __tablename__ = 'merge_table'

    # 系统自带id 可自增
    AutoId = Column(Integer, primary_key=True)

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

def queryNewsByKeyword(args):
    print(args)

    page = args["page"]
    limit = args["limit"]
    offset_data = (page - 1) * limit

    keyword = '%' + args["keyword"] + '%'
    timerange = args["date"]

    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(NewItem).filter(NewItem.Content.ilike(keyword)).filter(or_(NewItem.DTime == timerange, timerange == ''))

    totalRecords = len(query.all())

    results = query.offset(offset_data).limit(limit).all()

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
    
    # for newItem in newsList:
    #     print(newItem)
    
    session.commit()
    session.close()

    return {
        "totalRecords": totalRecords,
        "newsList": newsList
    }

# 返回首页统计信息
def queryStatistics():
    data = {
        "MentionSourceName": [
            { "value": 1048, "name": 'bbc.com' },
            { "value": 735, "name": 'bbc.co.uk' },
            { "value": 580, "name": 'yahoo.com' },
            { "value": 484, "name": 'cnn.com' },
            { "value": 300, "name": 'nytime.com' }
        ],
        "ActorCountryCode": [
            { "value": 1048, "name": 'UKR' },
            { "value": 735, "name": 'USA' },
            { "value": 580, "name": 'GBR' },
            { "value": 484, "name": 'EUR' },
            { "value": 300, "name": 'RUS' }
        ],
        "EventRootCode": [
            { "value": 1048, "name": getEventRootCodeExplain(1)["concise"] },
            { "value": 735, "name": getEventRootCodeExplain(2)["concise"] },
            { "value": 580, "name": getEventRootCodeExplain(3)["concise"] },
            { "value": 484, "name": getEventRootCodeExplain(4)["concise"] },
            { "value": 300, "name": getEventRootCodeExplain(5)["concise"] }
        ],
        "MentionDocTone": [
            { "value": 1048, "name": 'POS' },
            { "value": 735, "name": 'NEG' },
            { "value": 580, "name": 'NEU' }
        ],
    }

    sql_merge = "SELECT * FROM merge_table"
    df_merge = pd.read_sql_query(sql_merge, engine)
    # print(df_merge)
    result_merge = df_merge.groupby("MentionSourceName").size().to_dict()
    print(result_merge)


    sql_new = "SELECT * FROM new_table"
    df_new = pd.read_sql_query(sql_new, engine)
    # print(df_new)
    result_new = df_new.groupby("MentionSourceName").size().to_dict()
    print(result_new)


    # ans = {}
    # ans["keys"] = list(result_merge.keys())
    # ans["sum"] = list(result_merge.values())
    # ans["gain"] = []
    # ans["wait"] = []
    # for index, key in enumerate(ans["keys"]):
    #     if key in result_new.keys():
    #         ans["gain"].append(result_new[key])
    #     else:
    #         ans["gain"].append(0)
        
    #     ans["wait"].append(ans["sum"][index] - ans["gain"][index])
    # print(ans)

    ans = []
    for media in list(result_merge.keys()):
        tmp = {
            "MentionSourceName": media,
            "AllNews": result_merge[media],
            "CrawlNews": result_new[media] if media in result_new.keys() else 0
        }
        tmp["WaitNews"] = tmp["AllNews"] - tmp["CrawlNews"]
        ans.append(tmp)
    
    print(ans)



    return data


def test():
    # 写一条sql
    sql = "SELECT COUNT(*) FROM new_table"
    #建立dataframe
    df = pd.read_sql_query(sql,engine)
    print(df)


if __name__ == '__main__':
    # test()

    # args = {'keyword': '', 'date': '', 'page': 1, 'limit': 20, 'total': 0}
    # queryNewsByKeyword(args=args)
    pass