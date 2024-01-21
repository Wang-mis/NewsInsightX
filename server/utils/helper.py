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

# EventRootCode详细解释
EventRootCode_ExplainDetail = {
    '1' : 'MAKE PUBLIC STATEMENT',
    '2' : 'APPEAL',
    '3' : 'EXPRESS INTENT TO COOPERATE',
    '4' : 'CONSULT',
    '5' : 'ENGAGE IN DIPLOMATIC COOPERATION',
    '6' : 'ENGAGE IN MATERIAL COOPERATION',
    '7' : 'PROVIDE AID',
    '8' : 'YIELD',
    '9' : 'INVESTIGATE',
    '10' : 'DEMAND',
    '11' : 'DISAPPROVE',
    '12' : 'REJECT',
    '13' : 'THREATEN',
    '14' : 'PROTEST',
    '15' : 'EXHIBIT FORCE POSTURE',
    '16' : 'REDUCE RELATIONS',
    '17' : 'COERCE',
    '18' : 'ASSAULT',
    '19' : 'FIGHT',
    '20' : 'USE UNCONVENTIONAL MASS VIOLENCE'
}

# EventRootCode简称
EventRootCode_ExplainConcise = {
    '1' :  'STATEMENT',
    '2' :  'APPEAL',
    '3' :  'COOPERATE',
    '4' :  'CONSULT',
    '5' :  'CO-DIPLOMACY',
    '6' :  'CO-MATERIAL',
    '7' :  'AID',
    '8' :  'YIELD',
    '9' :  'INVESTIGATE',
    '10' : 'DEMAND',
    '11' : 'DISAPPROVE',
    '12' : 'REJECT',
    '13' : 'THREATEN',
    '14' : 'PROTEST',
    '15' : 'FORCE',
    '16' : 'ESTRANGED',
    '17' : 'COERCE',
    '18' : 'ASSAULT',
    '19' : 'FIGHT',
    '20' : 'VIOLENCE',
}

def getEventRootCodeExplain(id):
    id = str(id)
    if id in EventRootCode_ExplainConcise.keys():
        return {
            "id": id,
            "concise": EventRootCode_ExplainConcise[id],
            "detail": EventRootCode_ExplainDetail[id],
        }
    return {
        "id": id,
        "concise": "CONF",
        "detail": "CONF",
    }

# 按字典值value递减排序
def sortCustomDict(data: dict, reverse=True) -> dict:
    return dict(sorted(data.items(), key=lambda x: x[1], reverse=reverse))