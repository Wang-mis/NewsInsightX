from flask import Flask, request
from flask_cors import CORS, cross_origin
from utils.helper import ReturnWarningInfo, ReturnSuccessInfo
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

    cardList = []
    for ele in range(20):
        cardList.append({
            "id": "zIISJIASnlkj",
            "title": "US Overtakes China as South Korea’s Top Export Market",
            "author": "Sam Kim and Hooyeon Kim",
            "time": "January 1, 2024 at 10:19 AM",
            "url": "https://finance.yahoo.com/news/us-overtakes-china-south-korea-021922764.html"
        })
    
    # data = {
    #     "totalRecords": 300,
    #     "newsList": cardList
    # }

    data = queryNewsByKeyword(args=args)

    return ReturnSuccessInfo(data=data)

if __name__ == '__main__':
    print('run 0.0.0.0:14449')
    app.run(host='0.0.0.0', port=14449)