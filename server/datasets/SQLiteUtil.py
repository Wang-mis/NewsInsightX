# -*- coding:utf-8 -*-

from collections import Counter
from datetime import datetime, timedelta
from operator import and_, or_

import pandas as pd
from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy import create_engine, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from utils.helper import get_event_root_code_explain, sort_dict_by_value, create_date_range

engine = create_engine('sqlite:////home/wsx/remote/pleasenews/helper/SQLiteTest.db?check_same_thread=False', )
Base = declarative_base()

# 缓存统计数据
statistics_data = {
    "start_date": 0,
    "end_date": 0,
    'updated': False
}

counts_day_data = {
    "start_date": 0,
    "end_date": 0,
    "counts": [],
    "updated": False,
}


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


# region 更新数据库

def gen_merge_item(row):
    return MergeItem(
        GlobalEventID=row[0],
        Day=row[1],
        MonthYear=row[2],
        Year=row[3],
        FractionDate=row[4],
        Actor1Code=row[5],
        Actor1Name=row[6],
        Actor1CountryCode=row[7],
        Actor1KnownGroupCode=row[8],
        Actor1EthnicCode=row[9],
        Actor1Religion1Code=row[10],
        Actor1Religion2Code=row[11],
        Actor1Type1Code=row[12],
        Actor1Type2Code=row[13],
        Actor1Type3Code=row[14],
        Actor2Code=row[15],
        Actor2Name=row[16],
        Actor2CountryCode=row[17],
        Actor2KnownGroupCode=row[18],
        Actor2EthnicCode=row[19],
        Actor2Religion1Code=row[20],
        Actor2Religion2Code=row[21],
        Actor2Type1Code=row[22],
        Actor2Type2Code=row[23],
        Actor2Type3Code=row[24],
        IsRootEvent=row[25],
        EventCode=row[26],
        EventBaseCode=row[27],
        EventRootCode=row[28],
        QuadClass=row[29],
        GoldsteinScale=row[30],
        NumMentions=row[31],
        NumSources=row[32],
        NumArticles=row[33],
        AvgTone=row[34],
        Actor1Geo_Type=row[35],
        Actor1Geo_Fullname=row[36],
        Actor1Geo_CountryCode=row[37],
        Actor1Geo_ADM1Code=row[38],
        Actor1Geo_Lat=row[39],
        Actor1Geo_Long=row[40],
        Actor1Geo_FeatureID=row[41],
        Actor2Geo_Type=row[42],
        Actor2Geo_Fullname=row[43],
        Actor2Geo_CountryCode=row[44],
        Actor2Geo_ADM1Code=row[45],
        Actor2Geo_Lat=row[46],
        Actor2Geo_Long=row[47],
        Actor2Geo_FeatureID=row[48],
        ActionGeo_Type=row[49],
        ActionGeo_Fullname=row[50],
        ActionGeo_CountryCode=row[51],
        ActionGeo_ADM1Code=row[52],
        ActionGeo_Lat=row[53],
        ActionGeo_Long=row[54],
        ActionGeo_FeatureID=row[55],
        DATEADDED=row[56],
        SOURCEURL=row[57],
        EventTimeDate=row[58],
        MentionTimeDate=row[59],
        MentionType=row[60],
        MentionSourceName=row[61],
        MentionIdentifier=row[62],
        SentenceID=row[63],
        Actor1CharOffset=row[64],
        Actor2CharOffset=row[65],
        ActionCharOffset=row[66],
        InRawText=row[67],
        Confidence=row[68],
        MentionDocLen=row[69],
        MentionDocTone=row[70],
        MentionDocTranslationInfo=row[71],
        Extras=row[72],
        UniqueID=row[73]
    )


def gen_new_item(row):
    return NewItem(
        UniqueID=row[0],
        Title=row[1],
        Author=row[2],
        PTime=row[3],
        DTime=row[4],
        MentionSourceName=row[5],
        MentionIdentifier=row[6],
        Content=row[7]
    )


def gen_keyword_item(row):
    return KeywordItem(
        UniqueID=row[0],
        Keyword=row[1]
    )


def write_to_table_by_csv(csv, gen_func):
    Base.metadata.create_all(engine, checkfirst=True)
    session = sessionmaker(bind=engine)()
    for index, row in csv.iterrows():
        session.merge(gen_func(row.tolist()))
    session.commit()
    session.close()


def write_to_table_by_file(file_path, gen_func, sep):
    data = pd.read_csv(file_path, sep=sep).fillna("")
    data = data.drop_duplicates(subset=['UniqueID'], keep='first')
    write_to_table_by_csv(data, gen_func)


def delete_from_table_by_id(table, unique_ids: list):
    session = sessionmaker(bind=engine)()
    items_to_delete = session.query(table).filter(table.uniqueID.in_(unique_ids)).all()
    for item in items_to_delete:
        session.delete(item)

    session.commit()
    session.close()


def write_merge_table_by_file(file_path):
    write_to_table_by_file(file_path, gen_merge_item, sep=',')


def write_new_table_by_file(file_path):
    write_to_table_by_file(file_path, gen_new_item, sep='\\')


def write_keyword_table_by_file(file_path):
    write_to_table_by_file(file_path, gen_keyword_item, sep=',')


def write_all_table_by_files(day):
    media_merge_path = "/home/wsx/remote/pleasenews/merge/" + day + ".media.merge.csv"
    mention_path = "/home/wsx/remote/pleasenews/pnews/" + day + "/MentionSourceNames.csv"
    keywords_path = "/home/wsx/remote/pleasenews/pnews/" + day + "/Keywords_check.csv"
    write_merge_table_by_file(file_path=media_merge_path)
    write_new_table_by_file(file_path=mention_path)
    write_keyword_table_by_file(file_path=keywords_path)
    statistics_data['updated'] = False
    counts_day_data['updated'] = False


# endregion

def update():
    statistics_data['updated'] = False
    counts_day_data['updated'] = False


def query_news(args):
    page = args["page"]
    limit = args["limit"]
    offset_data = (page - 1) * limit
    keywords = args["keywords"]
    case_sensitive = bool(args['caseSensitive'])
    query_by_content = bool(args['queryByContent'])
    word_match = bool(args['wordMatch'])
    only_id = bool(args['onlyId'])
    timerange = args["date"]
    word_count_range = args['wordCount']
    sources = args['sources']
    sources = list(map(lambda s: s[0], sources))
    country = args['country']
    country = '' if (country is None or len(country) == 0) else country[0]

    # 获取查询的字数范围
    if isinstance(word_count_range, list):
        min_count = int(word_count_range[0])
        max_count = int(word_count_range[1])
    else:
        min_count = 00000000
        max_count = 99999999

    # 获取查询的时间段
    if isinstance(timerange, list):
        start_date, end_date = int(timerange[0]), int(timerange[1])
    else:
        start_date, end_date = 00000000, 99999999

    print("按关键词和时间段查找文章，"
          "Keywords = " + str(keywords) +
          ", Case Sensitive = " + str(case_sensitive) +
          ", Query By Content = " + str(query_by_content) +
          ", Word Match = " + str(word_match) +
          ", Start Time = " + str(start_date) +
          ", End Time = " + str(end_date) +
          ", Min Length = " + str(min_count) +
          ", Max Length = " + str(max_count) +
          ", Page = " + str(page) +
          ", Limit = " + str(limit) +
          ", Sources = " + str(sources))

    def process_keyword(k):
        if word_match:
            k = '% ' + k + ' %'
        else:
            k = '%' + k + '%'

        if case_sensitive:
            k = '*' + k[1:-1] + '*'
        return k

    def combine_condition(conditions, fn):
        if len(conditions) == 0:
            return True
        if len(conditions) == 1:
            return conditions[0]
        if len(conditions) == 2:
            return fn(conditions[0], conditions[1])
        return fn(conditions[0], combine_condition(conditions[1:], fn))

    # 从数据库中查找相应记录

    # region 关键词筛选
    keywords_condition_list = []
    if query_by_content:
        for keyword in keywords:
            keyword = process_keyword(keyword)
            keywords_condition_list.append(or_(
                NewItem.Title.op('GLOB')(keyword) if case_sensitive else NewItem.Title.ilike(keyword),
                NewItem.Content.op('GLOB')(keyword) if case_sensitive else NewItem.Content.ilike(keyword)
            ))
    else:
        for keyword in keywords:
            keyword = process_keyword(keyword)
            keywords_condition_list.append(
                NewItem.Title.op('GLOB')(keyword) if case_sensitive else NewItem.Title.ilike(keyword))

    keywords_condition = combine_condition(keywords_condition_list, and_)
    # endregion

    # region 新闻媒体筛选
    sources_condition_list = []
    for source in sources:
        sources_condition_list.append(NewItem.MentionSourceName.ilike('%' + source + '%'))
    sources_condition = combine_condition(sources_condition_list, or_)
    # endregion

    Session = sessionmaker(bind=engine)
    with Session() as session:
        now_query = (session
                     .query(NewItem)
                     .filter(and_(NewItem.DTime >= start_date, NewItem.DTime <= end_date))  # 匹配日期
                     .filter(sources_condition)  # 匹配新闻媒体
                     .filter(keywords_condition)
                     .filter(and_(func.length(NewItem.Content) >= min_count, func.length(NewItem.Content) <= max_count))
                     .subquery()
                     )

        if country != '':
            now_query = (session
                         .query(now_query)
                         .join(MergeItem, now_query.c.UniqueID == MergeItem.UniqueID)
                         .filter(or_(MergeItem.Actor1CountryCode == country,
                                     MergeItem.Actor2CountryCode == country))
                         .subquery())

        total_records = session.query(now_query).count()  # 获取记录条数

        if only_id:
            # 如果only_id == True，则返回所有新闻的ID列表，不排序
            results = session.query(now_query.c.UniqueID).offset(offset_data).limit(limit)
            return {"ids": [t[0] for t in results], "totalRecords": total_records}
        else:
            # 按日期降序排序，获取当前页面的所有记录，results为NewItem对象的数组
            results = session.query(now_query).order_by(now_query.c.DTime.desc()).offset(offset_data).limit(limit)
            # 将NewItem对象数组转化为字典的数组，便于以json的格式传给前端
            news_list = []
            for news in results:
                news_list.append({
                    'UniqueID': news.UniqueID,
                    'Title': news.Title,
                    'Author': news.Author,
                    'PTime': news.PTime,
                    'DTime': news.DTime,
                    'MentionSourceName': news.MentionSourceName,
                    'MentionIdentifier': news.MentionIdentifier,
                    'Content': news.Content
                })

            # 将总记录数和当前页面的所有记录数据传给前端
            return {"totalRecords": total_records, "newsList": news_list}


def query_news_by_id(unique_id: str):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        news = session.query(NewItem).filter_by(UniqueID=unique_id).one()
        return {
            'UniqueID': news.UniqueID,
            'Title': news.Title,
            'Author': news.Author,
            'PTime': news.PTime,
            'DTime': news.DTime,
            'MentionSourceName': news.MentionSourceName,
            'MentionIdentifier': news.MentionIdentifier,
            'Content': news.Content
        }


def query_news_by_ids(ids: list[str]):
    """ 根据ID列表查询所有的News数据 """
    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = session.query(NewItem).filter(NewItem.UniqueID.in_(ids)).subquery()
        query = session.query(query)

        news_list: list[tuple] = []
        for news in query:
            news_list.append(tuple(news))

        return {"news_list": news_list}


def query_mentions_by_ids(ids: list[str]):
    """ 根据ID列表查询所有的Mentions数据 """
    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = session.query(MergeItem).filter(MergeItem.UniqueID.in_(ids)).subquery()
        query = session.query(query)

        mentions_list: list[tuple] = []
        for mention in query:
            mentions_list.append(tuple(mention))

        return {"mentions_list": mentions_list}


def query_keywords_by_ids(ids: list[str]):
    """ 根据ID列表查询所有的Mentions数据 """
    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = session.query(KeywordItem).filter(KeywordItem.UniqueID.in_(ids)).subquery()
        query = session.query(query)

        keywords_list: list[tuple] = []
        for keyword in query:
            keywords_list.append(tuple(keyword))

        return {"keywords_list": keywords_list}


def query_statistics(args):
    global statistics_data

    force_update = args["forceUpdate"]
    start_date = args["startDate"]
    end_date = args["endDate"]

    if force_update:
        statistics_data['updated'] = False

    print("请求统计数据。")
    if (statistics_data['updated']
            and statistics_data['start_date'] == start_date
            and statistics_data['end_date'] == end_date):
        print("已缓存统计数据。")
        return statistics_data

    print("未缓存统计数据，重新计算。")

    Session = sessionmaker(bind=engine)
    with Session() as session:
        merge_in_date_stmt = and_(MergeItem.Day >= start_date, MergeItem.Day <= end_date)
        new_in_date_stmt = and_(NewItem.DTime >= start_date, NewItem.DTime <= end_date)
        merge_query_in_date = session.query(MergeItem).filter(merge_in_date_stmt).subquery()
        new_query_in_date = session.query(NewItem).filter(new_in_date_stmt).subquery()

        # region 已有新闻文章占比
        statistics_data["NewsProportion"] = []
        merge_table_len = session.query(merge_query_in_date).count()
        new_table_len = session.query(new_query_in_date).count()
        statistics_data["NewsProportion"].append({"value": new_table_len, "name": "With Content"})
        statistics_data["NewsProportion"].append({"value": merge_table_len - new_table_len, "name": "Without Content"})
        # endregion

        # region 每个新闻媒体发表的文章数量
        statistics_data["MentionSourceName"] = []

        sources_count = (session
                         .query(merge_query_in_date.c.MentionSourceName,
                                func.count(merge_query_in_date.c.MentionSourceName))
                         .group_by(merge_query_in_date.c.MentionSourceName)
                         .all())
        sources_count = sorted(sources_count, key=lambda x: x[1], reverse=True)

        sources_count_max_len = 7
        other_sources_count = 0
        for i in range(len(sources_count)):
            value = sources_count[i][1]
            name = sources_count[i][0]
            if i < sources_count_max_len:
                statistics_data["MentionSourceName"].append({"value": value, "name": name})
            else:
                other_sources_count += value

        statistics_data["MentionSourceName"].append({"value": other_sources_count, "name": "others"})
        # endregion

        # region 事件发生的国家
        statistics_data["ActorCountryCode"] = []
        country1_query = session.query(merge_query_in_date.c.Actor1CountryCode.label('country'))
        country2_query = session.query(merge_query_in_date.c.Actor2CountryCode.label('country'))
        country_query = country1_query.union_all(country2_query).subquery()
        country_count = (session
                         .query(country_query.c.country, func.count(country_query.c.country))
                         .group_by(country_query.c.country)
                         .all())
        country_count = sorted(country_count, key=lambda x: x[1], reverse=True)
        country_count_max_len = 7
        other_country_count = 0
        for i in range(len(country_count)):
            value = country_count[i][1]
            name = country_count[i][0] if country_count[i][0] != '' else "NONE"

            if i < country_count_max_len:
                statistics_data["ActorCountryCode"].append({"value": value, "name": name})
            else:
                other_country_count += value

        statistics_data["ActorCountryCode"].append({"value": other_country_count, "name": "OTHERS"})
        # endregion

        # region 每种事件类型的数量
        statistics_data["EventRootCode"] = []
        rootcode_count = (session
                          .query(merge_query_in_date.c.EventRootCode, func.count(merge_query_in_date.c.EventRootCode))
                          .group_by(merge_query_in_date.c.EventRootCode)
                          .all())
        rootcode_count = sorted(rootcode_count, key=lambda x: x[1], reverse=True)
        rootcode_count_max_len = 7
        other_rootcode_count = 0
        for i in range(len(rootcode_count)):
            value = rootcode_count[i][1]
            name = get_event_root_code_explain(int(rootcode_count[i][0]))["concise"]

            if i < rootcode_count_max_len:
                statistics_data["EventRootCode"].append({"value": value, "name": name})
            else:
                other_rootcode_count += value

        statistics_data["EventRootCode"].append({"value": other_rootcode_count, "name": "OTHERS"})
        # endregion

        # region 积极和消极事件的数量
        statistics_data["MentionDocTone"] = []
        pos_count = session.query(func.count(merge_query_in_date.c.UniqueID)).filter(
            merge_query_in_date.c.MentionDocTone > 0).scalar()
        neg_count = session.query(func.count(merge_query_in_date.c.UniqueID)).filter(
            merge_query_in_date.c.MentionDocTone < 0).scalar()
        neu_count = merge_table_len - pos_count - neg_count
        statistics_data["MentionDocTone"].append({"value": pos_count, "name": "POS"})
        statistics_data["MentionDocTone"].append({"value": neg_count, "name": "NEG"})
        statistics_data["MentionDocTone"].append({"value": neu_count, "name": "NEU"})
        # endregion

        # region 词云
        statistics_data["KeywordCloud"] = []
        article_keywords = (session
                            .query(KeywordItem.Keyword)
                            .join(NewItem, KeywordItem.UniqueID == NewItem.UniqueID)
                            .filter(new_in_date_stmt))
        keywords = []
        for article_keyword_row in article_keywords:
            keywords.extend(article_keyword_row[0].split('|'))

        keywords_count = sort_dict_by_value(dict(Counter(keywords)))

        keywords_max_count = 60
        for key, value in keywords_count.items():
            statistics_data["KeywordCloud"].append({"value": value, "name": key})
            if len(statistics_data["KeywordCloud"]) > keywords_max_count:
                break
        # endregion

        # 新闻总数
        # total_count = session.query(NewItem).count()
        total_count = session.query(MergeItem).count()
        statistics_data["totalCount"] = total_count

        # 时间段内新闻数
        # time_range_count = session.query(new_query_in_date).count()
        time_range_count = session.query(merge_query_in_date).count()
        statistics_data["timeRangeCount"] = time_range_count

        # 昨日新闻数
        yesterday = datetime.now() - timedelta(days=2)
        yesterday = int(yesterday.strftime('%Y%m%d'))
        print(yesterday)
        # yesterday_count = session.query(NewItem).filter(NewItem.DTime == yesterday).count()
        yesterday_count = session.query(MergeItem).filter(MergeItem.Day == yesterday).count()
        statistics_data["yesterdayCount"] = yesterday_count

        print("统计数据计算完成。")

        statistics_data['start_date'] = int(start_date)
        statistics_data['end_date'] = int(end_date)
        statistics_data['updated'] = True

    return statistics_data


def query_article_counts_day(args):
    """根据传入的时间段，查询时间段之间每天的新闻数量"""
    time_range = args["timeRange"]
    force_update = args["forceUpdate"]
    start_date = int(time_range[0])
    end_date = int(time_range[1])
    print(f"查询每天新闻数量：Start Date = {start_date}，End Date = {end_date}。")

    if force_update:
        counts_day_data['updated'] = False
    if (counts_day_data['updated']
            and counts_day_data['start_date'] == start_date
            and counts_day_data['end_date'] == end_date):
        print("已缓存每天新闻数量数据，直接返回缓存数据。")
        return {"counts": counts_day_data['counts']}

    print("未缓存每天新闻数量数据，重新计算。")

    days = create_date_range([start_date, end_date])

    Session = sessionmaker(bind=engine)
    with Session() as session:
        counts = []
        for day in days:
            cnt = session.query(MergeItem).filter(MergeItem.Day == int(day)).count()
            counts.append(cnt)

    counts_day_data['start_date'] = start_date
    counts_day_data['end_date'] = end_date
    counts_day_data['counts'] = counts
    counts_day_data['updated'] = True

    return {"counts": counts}
