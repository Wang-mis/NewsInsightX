from flask import Flask, request
from flask_cors import CORS, cross_origin
from utils.helper import ReturnWarningInfo, ReturnSuccessInfo, getEventRootCodeExplain
from datasets.SQLiteUtil import queryNewsByKeyword

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app)
app.config['CORS_HEADER'] = 'Content-Type'


@app.route("/user/login", methods=["POST"])
@cross_origin()
def user_login():
    """
    用户登录
    :return:
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username == "admin" and password == "123456":
        return ReturnSuccessInfo(data={ "token": "666666" })
    
    return ReturnWarningInfo()


@app.route("/user/info", methods=["GET", "POST"])
@cross_origin()
def user_info():
    """
    获取当前用户信息
    :return:
    """
    token = request.headers.get("token")
    if token == "hdjhs__token":
        return ReturnSuccessInfo(data={ "id": "1", "userName": "admin", "realName": "张三", "userType": 1 })
    
    return ReturnWarningInfo()


@app.route("/user/test", methods=["POST"])
@cross_origin()
def user_test():
    """
    测试POST方法
    """
    data = request.get_json()
    print(data)
    test_arg = data.get("test_arg")
    if test_arg == "test_arg":
        return ReturnSuccessInfo(data={ "id": "1", "arr": [1,2,3] })
    
    return ReturnWarningInfo()


@app.route("/querynews", methods=["POST"])
@cross_origin()
def queryNewsAPI():
    args = request.get_json()
    try:
        data = queryNewsByKeyword(args=args)
        return ReturnSuccessInfo(data=data)
    except Exception as e:
        print(e)
    return ReturnWarningInfo()


@app.route("/homepage", methods=["GET"])
@cross_origin()
def queryHomeStatisticsAPI():
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
    return ReturnSuccessInfo(data=data)



if __name__ == '__main__':
    print('run 0.0.0.0:14449')
    app.run(host='0.0.0.0', port=14449)