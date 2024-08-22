let syn = {
    "v": {
        "废除规定": ["abandon", "repeal", "abrogate", "annul", "rescind", "revoke", "abate"],
        "降低（地位、职位、威望或尊严）": ["abase", "vitiate", "demoralize"],
        "削弱，损害": ["vitiate", "blemish", "flaw", "mar", "undermine"],
        "亵渎": ["profane", "defile"],
        "使尴尬，使羞愧": ["abash", "discomfit", "disconcert", "faze", "fluster"],
        "迷惑，困惑": ["nonplus", "confound"],
        "减轻（程度或者强度）": ["abate", "moderate", "subside", "diminish", "dwindle", "wane"],
        "减少（数量或者降低价值）": ["abate", "deplete", "dwindle"],
        "缩短": ["abbreviate", "abridge", "curtail", "truncate", "retrench"],
        "镇压": ["quash", "repress", "quell", "squelch", "suppress"],
        "正式放弃（权力、责任）":["abdicate","cede","relinquish",],
        "帮助，怂恿":["abet","foment",],
        "煽动":["foment","incite","instigate","provoke"],
        "深恶痛绝，极度厌恶":["abhor","abominate","despise","execrate","loathe"],
        "发誓放弃":["recant","renege","renounce","resign","abnegate","repeal"],
        "否认":["abnegate","repudiate","contradict","disavow","gainsay","refute"],
        "磨损，精神上折磨":["abrade","scuff",],
        "偷偷离开":["abscond"],
        "预防接种":["vaccinate"],
        "使无罪，解除责任":["absolve","exonerate","vindicate","exculpate"],
        "自我克制，主动戒绝":["abstain"],
        "做总结，概括":["abstract"],
        "使分心":["abstract","detract","divert"],
        "辱骂抨击":["abuse","assail","bash","belabor","blast","excoriate","castigate","berate","lambaste","reproach","upbraid","vituperate","rail"],
        "不正当不合理使用":["abuse"],
        "邻接，毗邻":["abut"],
        "极低的或极可怜的":["abysmal"],
        "（程度）很深的、极端的":["abysmal"],
        "赞成":["accede","acquiesce","assent","consent"],
        "就任，就职":["accede"],
        "加速":["accelerate","balloon","escalate","burgeon","proliferate"],
        "使提前发生":["accelerate"],
        "变大，变多":[]


        

    },
    "adj": {
        "异常的，非常规的":["aberrant","anomalous","unwonted"],
        "非凡的":["phenomenal","exceptional",],
        "专制的": ["absolute", "arbitrary", "despotic"],
        "傲慢的，专横的": ["imperious", "bumptious", "peremptory", "pompous", "presumptuous", "supercilious" ,"overbearing"],
        "永久的":["abiding","eternal","everlasting","imperishable","perpetual"],
        "无精打采的":["abject"],
        "（地位、身份）悲惨、凄凉的":["abject"],
        "卑微的，讨好的，顺从的":["abject", "humble", "menial","servile"],
        "无欺诈的，光明正大的":["aboveboard"],
        "熟知的":["abreast","conversant","versed"],
        "未出现的，缺乏的":["absent","wanting"],
        "不专心的，走神的":["absent"],
        "无限的，绝对的":["absolute","utter"],
        "完美的、纯净不掺杂的":["absolute"],
        "不容置疑的，确凿的":["absolute"],
        "（吃喝等）有节制的，节俭的":["abstemious","temperate","sober"],
        "难以理解的":["abstruse","arcane","occult","opaque","impenetrable","esoteric","hermetic","recondite"],
        "不合理的":["absurd","ludicrous","preposterous","fallacious","ludicrous"],
        "大量的":["abundant","teeming","awash","flush","fraught","replete",]

    },
    "n":{
        "中止，搁置":["abeyance","doldrums","moratorium"]
    },
    "adv":{
        "并排地":["abreast"]
    }
}

let c = (arr) => {return arr[Math.floor(Math.random()*arr.length)]}

let story = `
Please write your story here. You can use words like this: ${c(syn.v.废除规定)} 
`

//wordcound
for(let k in syn ){
    let c = 0;
    for(let k2 in syn[k]){
        c+=syn[k][k2].length;
    }
    console.log(c);
}


console.log(story);