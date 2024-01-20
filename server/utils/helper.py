import json
from flask import jsonify


def ReturnInfo(code, type, msg, data) -> dict:
    return jsonify({
        "code": code,
        "type": type,
        "msg": msg,
        "data": data
    })

def ReturnSuccessInfo(code=0, type="success", msg="success", data=None) -> dict:
    return ReturnInfo(code, type, msg, data)

def ReturnWarningInfo(code=20010, type="warning", msg="warning", data=None) -> dict:
    return ReturnInfo(code, type, msg, data)

def Dict2Json(outfile, data):
    with open(outfile,'w') as f:
        json.dump(data, f)

def Json2Dict(file):
    with open(file, 'r') as f:
        ans = json.load(f)
    return ans

