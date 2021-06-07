import requests
import re
from time import sleep
from bs4 import BeautifulSoup


def crawl(url, OJ, rule):
    res= requests.get(url)
    if not(res.status_code==200):
        return OJ + "was broken!"
    soup= BeautifulSoup(res.text, "html.parser")
    StateElement= soup.find_all("td", class_=re.compile(rule))
    State= []
    if len(StateElement)==0:
        return "NE"

    if OJ=="TOJ":
        for StateStr in StateElement:
            if StateStr.string=="Accepted":
                return "Accepted"
            State.append(StateStr.string)
    elif OJ=="TIOJ":
        for StateStr in StateElement:
            if StateStr.string=="AC":
                return "AC"
            State.append(StateStr.string)
    return State[0]


def TIOJ(username, userID, problemID):
    if problemID=="" or userID=="":
        return "information isn't complete"
    url= "https://tioj.ck.tp.edu.tw/problems/" + problemID + "/submissions?filter_user_id=" + userID
    return crawl(url, "TIOJ", "^text-")


def TOJ(username, userID, problemID):
    if problemID=="" or userID=="":
        return "information isn't complete"
    url= "http://210.70.137.215/oj/be/chal?proid="+ problemID +"&acctid="+ userID
    return crawl(url, "TOJ", "^state-")


def ZOJ(username, userID, problemID):
    url= "https://zerojudge.tw/User/V1.0/Accepted?account="+ username
    res= requests.get(url)
    if not(res.status_code==200):
        return "ZOJ was broken"
    ACprob= eval(res.text)["accepted"]
    for prob in ACprob:
        if prob==problemID:
            return "AC"
    return "NE"


def UVa(username, userID, problemNum):
    if username=="" or problemNum=="":
        return "information isn't complete"

    reference= {'10' : "Submission error",
    '15' : "Can't be judged",
    '20' : "In queue",
    '30' : "Compile error",
    '35' : "Restricted function",
    '40' : "Runtime error",
    '45' : "Output limit",
    '50' : "Time limit",
    '60' : "Memory limit",
    '70' : "Wrong answer",
    '80' : "PresentationE",
    '90' : "Accepted"
    }
    try:
        userID_url= "https://uhunt.onlinejudge.org/api/uname2uid/" + username
        userID= requests.get(userID_url).text
    except:
        return "UidNotfound"
    try:
        problemList_url= "https://uhunt.onlinejudge.org/api/p/num/" + problemNum
        problemID= eval(requests.get(problemList_url).text)['pid']
    except:
        return "PidNotfound"

    url= "https://uhunt.onlinejudge.org/api/subs-pids/"+ userID + "/"+ str(problemID) + "/999999"
    Submit= eval(requests.get(url).text)[userID]['subs']
    State= []
    
    if len(Submit)==0:
        return "NE"
    for i in range(0, len(Submit)):
        if Submit[i][2]==90:
            return "Accepted"
        State.append([Submit[i][2], Submit[i][4]])
    State.sort(key= lambda s: s[1])
    return reference[str(State[0][0])]
 

def CodeForces(username, userID, problemID):
    url= "https://codeforces.com/api/user.status?handle=" + username
    try:
        res= requests.get(url).text
    except:
        return "UidNotfound"
    State= []
    
    for arr in eval(res.replace("false", "False"))['result']:
        if problemID==(str(arr["problem"]["contestId"]) + arr["problem"]["index"]):
            found= True
            if arr["verdict"]=="OK":
                return "Accepted"
            State.append([arr["creationTimeSeconds"], arr["verdict"]])
    State.sort(key= lambda s: s[0])
    if len(State)==0:
        return "NE"
    return State[-1][1]


def AtCoder(username, userID, problemID):
    url= "https://kenkoooo.com/atcoder/atcoder-api/results?user=" + username
    res= requests.get(url)
    if not(res.status_code==200):
        return "AtCoder was broken"
    res= eval(res.text.replace("null", "None"))
    State= []
    for sub in res:
        if sub["problem_id"]==problemID:
            found= True
            if sub["result"]=='AC':
                return "AC"
            State.append(sub["result"])
    if len(State)==0:
        return "NE"
    return State[-1][1]