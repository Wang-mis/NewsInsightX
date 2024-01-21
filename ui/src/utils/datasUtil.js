// EventRootCode详细解释
let EventRootCode_ExplainDetail = {
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

// EventRootCode简称
let EventRootCode_ExplainConcise = {
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

export function getEventRootCodeExplain(id){
    if (id in EventRootCode_ExplainConcise) {
        return {
            id: id,
            concise: EventRootCode_ExplainConcise[id],
            detail: EventRootCode_ExplainDetail[id],
        }
    }
    return {
        id: id,
        concise: "CONF",
        detail: "CONF",
    }
}