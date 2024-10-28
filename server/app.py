# -*- coding:utf-8 -*-
# http://123.57.216.53:14451

from flask import Flask, request
from flask_cors import CORS, cross_origin

from datasets.SQLiteUtil import query_news, query_statistics, query_article_counts_day, write_all_table_by_files, \
    query_news_by_id, query_news_by_ids, query_mentions_by_ids, query_keywords_by_ids, update
from datasets.users import query_user, add_user, delete_user, check_user_token
from utils.helper import return_info

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app)
app.config['CORS_HEADER'] = 'Content-Type'


@app.route("/dataset/update", methods=["GET"])
@cross_origin()
def update_api():
    # 接收到更新数据请求，更新数据
    print("接收到更新数据请求，更新数据。")
    update()
    print("更新数据完成。")
    return return_info(0, "success", "", {})


@app.route("/dataset/update_day", methods=["GET"])
@cross_origin()
def update_day():
    data = request.get_json()
    day = data.get("day")
    # 接收到更新数据请求，更新数据
    print("接收到更新数据请求，更新数据。")
    write_all_table_by_files(day)
    print("更新数据完成。")

    return return_info(0, "success", "", {})


# region Users
@app.route("/user/login", methods=["POST"])
@cross_origin()
def user_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    print(f"接受登录请求，username={username}, password={password}")

    code, user_info, token = query_user(username, password)
    if code == 0:
        print("登录成功")
        user_info['token'] = token
        return return_info(code, "success", "成功", user_info)

    if code == 1:
        msg = "密码错误"
    elif code == 2:
        msg = "用户不存在"
    else:
        msg = "未知错误"

    print(f"登录失败，msg={msg}")
    return return_info(code, "error", msg, {})


@app.route("/user/login_token", methods=["POST"])
@cross_origin()
def user_login_token():
    data = request.get_json()
    token = data.get("token")

    code, user_info = check_user_token(token)

    if code == 0:
        return return_info(code, "success", "成功", user_info)

    if code == 1:
        msg = "token错误"
    elif code == 2:
        msg = "token过期"
    else:
        msg = "未知错误"

    return return_info(code, "error", msg, {})


@app.route("/user/signup", methods=["POST"])
@cross_origin()
def user_signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    code, token = add_user(username, password)

    if code == 0:
        return return_info(code, "success", "成功", {'token': token})

    if code == 1:
        msg = "用户已存在"
    else:
        msg = "未知错误"

    return return_info(code, "error", msg, {})


@app.route("/user/delete", methods=["POST"])
@cross_origin()
def user_delete():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    code = delete_user(username, password)
    if code == 0:
        msg = "成功"
    elif code == 1:
        msg = "密码错误"
    elif code == 2:
        msg = "用户不存在"
    else:
        msg = "未知错误"

    return return_info(code, "success" if code == 0 else "error", msg, {})


# endregion


@app.route("/querynews", methods=["POST"])
@cross_origin()
def query_news_api():
    args = request.get_json()
    try:
        data = query_news(args)
        return return_info(0, "success", "成功", data)
    except Exception as e:
        print(e)
    return return_info(100, "error", "未知错误", {})


@app.route("/query_news_by_id", methods=["POST"])
@cross_origin()
def query_news_by_id_api():
    unique_id: str = request.get_json()["id"]
    try:
        data = query_news_by_id(unique_id)
        return return_info(0, "success", "成功", data)
    except Exception as e:
        print(e)
    return return_info(100, "error", "未知错误", {})


@app.route("/query_news_by_ids", methods=["POST"])
@cross_origin()
def query_news_by_ids_api():
    ids: list[str] = request.get_json()["ids"]
    try:
        data = query_news_by_ids(ids)
        return return_info(0, "success", "成功", data)
    except Exception as e:
        print(e)
    return return_info(100, "error", "未知错误", {})


@app.route("/query_mentions_by_ids", methods=["POST"])
@cross_origin()
def query_mentions_by_ids_api():
    ids: list[str] = request.get_json()["ids"]
    try:
        data = query_mentions_by_ids(ids)
        return return_info(0, "success", "成功", data)
    except Exception as e:
        print(e)
    return return_info(100, "error", "未知错误", {})


@app.route("/query_keywords_by_ids", methods=["POST"])
@cross_origin()
def query_keywords_by_ids_api():
    ids: list[str] = request.get_json()["ids"]
    try:
        data = query_keywords_by_ids(ids)
        return return_info(0, "success", "成功", data)
    except Exception as e:
        print(e)
    return return_info(100, "error", "未知错误", {})


@app.route("/homepage", methods=["POST"])
@cross_origin()
def query_home_statistics_api():
    try:
        args = request.get_json()
        data = query_statistics(args)
        return return_info(0, "success", "成功", data)

    except Exception as e:
        print("请求统计数据失败。\n", e)

    return return_info(100, "error", "未知错误", {})


@app.route("/query/counts_day", methods=["POST"])
@cross_origin()
def query_article_counts_day_api():
    args = request.get_json()
    try:
        print(args)
        data = query_article_counts_day(args=args)
        return return_info(0, "success", "成功", data)
    except Exception as e:
        print(e)

    return return_info(100, "error", "未知错误", {})


if __name__ == '__main__':
    print('run 0.0.0.0:14451')
    app.run(host='0.0.0.0', port=14451, debug=True)
