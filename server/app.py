from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

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
        return jsonify({
            "code": 0,
            "type": "success",
            "data": {
                "token": "666666"
            }
        })
    else:
        return jsonify({
            "code": 20010,
            "type": "warning",
            "msg": "用户名或密码错误"
        })


@app.route("/user/info", methods=["GET", "POST"])
@cross_origin()
def user_info():
    """
    获取当前用户信息
    :return:
    """
    token = request.headers.get("token")
    if token == "hdjhs__token":
        return jsonify({
            "code": 0,
            "type": "success",
            "msg": "success",
            "data": {
                "id": "1",
                "userName": "admin",
                "realName": "张三",
                "userType": 1
            }
        })
    return jsonify({
        "code": 20010,
        "type": "warning",
        "msg": "token不存在或已过期"
    })


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
        return jsonify({
            "code": 0,
            "type": "success",
            "msg": "success",
            "data": {
                "id": "1",
                "arr": [1,2,3]
            }
        })
    
    return jsonify({
        "code": 20010,
        "type": "warning",
        "msg": "搞错了。。。"
    })


if __name__ == '__main__':
    print('run 0.0.0.0:14449')
    app.run(host='0.0.0.0', port=14449)