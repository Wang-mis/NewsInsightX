from flask import jsonify


def return_info(code, info_type, msg, data):
    return jsonify({
        "code": code,
        "type": info_type,
        "msg": msg,
        "data": data
    })


def return_success_info(msg="success", data=None):
    return return_info(0, "success", msg, data)


def return_warning_info(msg="warning", data=None):
    return return_info(20010, "warning", msg, data)


# EventRootCode详细解释
EventRootCode_ExplainDetail = {
    '1': 'MAKE PUBLIC STATEMENT',
    '2': 'APPEAL',
    '3': 'EXPRESS INTENT TO COOPERATE',
    '4': 'CONSULT',
    '5': 'ENGAGE IN DIPLOMATIC COOPERATION',
    '6': 'ENGAGE IN MATERIAL COOPERATION',
    '7': 'PROVIDE AID',
    '8': 'YIELD',
    '9': 'INVESTIGATE',
    '10': 'DEMAND',
    '11': 'DISAPPROVE',
    '12': 'REJECT',
    '13': 'THREATEN',
    '14': 'PROTEST',
    '15': 'EXHIBIT FORCE POSTURE',
    '16': 'REDUCE RELATIONS',
    '17': 'COERCE',
    '18': 'ASSAULT',
    '19': 'FIGHT',
    '20': 'USE UNCONVENTIONAL MASS VIOLENCE'
}

# EventRootCode简称
EventRootCode_ExplainConcise = {
    '1': 'STATEMENT',
    '2': 'APPEAL',
    '3': 'COOPERATE',
    '4': 'CONSULT',
    '5': 'CO-DIPLOMACY',
    '6': 'CO-MATERIAL',
    '7': 'AID',
    '8': 'YIELD',
    '9': 'INVESTIGATE',
    '10': 'DEMAND',
    '11': 'DISAPPROVE',
    '12': 'REJECT',
    '13': 'THREATEN',
    '14': 'PROTEST',
    '15': 'FORCE',
    '16': 'ESTRANGED',
    '17': 'COERCE',
    '18': 'ASSAULT',
    '19': 'FIGHT',
    '20': 'VIOLENCE',
}


def get_event_root_code_explain(code):
    code = str(code)
    if code in EventRootCode_ExplainConcise.keys():
        return {
            "id": code,
            "concise": EventRootCode_ExplainConcise[code],
            "detail": EventRootCode_ExplainDetail[code],
        }
    return {
        "id": code,
        "concise": "CONF",
        "detail": "CONF",
    }


# 按字典值value递减排序
def sort_dict_by_value(data: dict, reverse=True) -> dict:
    return dict(sorted(data.items(), key=lambda x: x[1], reverse=reverse))
