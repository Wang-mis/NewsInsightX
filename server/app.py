from flask import Flask, request
from flask_cors import CORS, cross_origin

from datasets.users import query_user, add_user, delete_user, check_user_token
from utils.helper import return_info
from datasets.SQLiteUtil import query_news_by_keyword, query_statistics

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app)
app.config['CORS_HEADER'] = 'Content-Type'


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


@app.route("/querynews", methods=["POST"])
@cross_origin()
def query_news_api():
    args = request.get_json()
    try:
        print(args)
        data = query_news_by_keyword(args=args)
        return return_info(0, "success", "成功", data)
    except Exception as e:
        print(e)
    return return_info(100, "error", "未知错误", {})


@app.route("/homepage", methods=["GET"])
@cross_origin()
def query_home_statistics_api():
    try:
        force_update = bool(int(request.args.get('update', default='0')))
        data = query_statistics(force_update)
        return return_info(0, "success", "成功", data)

    except Exception as e:
        print("请求统计数据失败。\n", e)


    return return_info(100, "error", "未知错误", {})


if __name__ == '__main__':
    print('run 0.0.0.0:14451')
    app.run(host='0.0.0.0', port=14451, debug=True)
