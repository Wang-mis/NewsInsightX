from flask import Flask, request
from flask_cors import CORS, cross_origin

from datasets.SQLiteUtil import query_user, add_user, delete_user
from utils.helper import return_info
from utils.helper import return_warning_info, return_success_info
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

    code, user = query_user(username, password)
    if code == 0:
        msg = "成功"
        return return_info(code, "success", msg, {
            'username': user.username,
            'password': user.password,
            'intro': user.intro,
        })
    elif code == 1:
        msg = "密码错误"
    elif code == 2:
        msg = "用户不存在"
    else:
        msg = "未知错误"

    return return_info(code, "error", msg, {})


@app.route("/user/signup", methods=["POST"])
@cross_origin()
def user_signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    code = add_user(username, password)

    if code == 0:
        msg = "成功"
    elif code == 1:
        msg = "用户已存在"
    else:
        msg = "未知错误"

    return return_info(code, "success" if code == 0 else "error", msg, {})


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
        return return_success_info(data=data)
    except Exception as e:
        print(e)
    return return_warning_info()


@app.route("/homepage", methods=["GET"])
@cross_origin()
def query_home_statistics_api():
    try:
        force_update = bool(int(request.args.get('update', default='0')))
        data = query_statistics(force_update)
        return return_success_info(data=data)
    except Exception as e:
        print("请求统计数据失败。\n", e)
        return return_warning_info()


if __name__ == '__main__':
    print('run 0.0.0.0:14451')
    app.run(host='0.0.0.0', port=14451, debug=True)
