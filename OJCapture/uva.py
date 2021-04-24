import requests, json
from flask import current_app

api_link = 'https://uhunt.onlinejudge.org/api'
id_to_stat = {10: 'SE', 15: 'CBJ', 20: 'IQ', 30: 'CE', 35: 'RF', 40: 'RE', 45: 'OE', 50: 'TLE', 60: 'MLE', 70: 'WA', 80: 'PE', 90: 'AC'}

# transform username into uid
def get_uid(username):
    res = requests.get(api_link + '/uname2uid/{}'.format(username))
    if(res.status_code == 200):
        if(res.text == '0'):
            # username not found
            return 0
        else:
            # some weired behavior
            return res.text
    else:
        return 0

# transform problem number into pid
def get_pid(prob_num):
    res = requests.get(api_link + '/p/num/{}'.format(prob_num))
    if(res.status_code == 200):
        data = json.loads(res.text)
        try:
            return data['pid']
        except:
            # problem number not found
            return 0
    else:
        # some weired behavior
        return -1

# get specify users' stats in specify problems
def get_all_subs(uids, problems):
    current_app.logger.info(f'uids: {uids}\nproblems: {problems}')
    ids = ','.join(str(s) for s in uids)
    probs = ','.join(str(s) for s in problems)
    current_app.logger.info(f'requests link: {api_link}/subs-pids/{ids}/{probs}/0')
    res = requests.get(api_link + '/subs-pids/{}/{}/0'.format(ids, probs))
    if(res.status_code == 200):
        return res.text
    else:
        return 'Error'

def get_all_stat(uname_to_username, pids, pid_to_pnum, submissions):
    '''
        --------status code---------
        10 : Submission error
        15 : Can't be judged
        20 : In queue
        30 : Compile error
        35 : Restricted function
        40 : Runtime error
        45 : Output limit
        50 : Time limit
        60 : Memory limit
        70 : Wrong answer
        80 : PresentationE
        90 : Accepted
    '''
    
    ret = {}
    for id in submissions:
        '''
            --------- return values --------
            0: Submission ID
            1: Problem ID
            2: Verdict ID
            3: Runtime
            4: Submission Time (unix timestamp)
            5: Language ID (1=ANSI C, 2=Java, 3=C++, 4=Pascal, 5=C++11)
            6: Submission Rank
        '''

        # init
        uname = submissions[id]['uname']
        stat = {}
        ret[uname_to_username[uname]] = {}
        res = None
        lst = {'res': None, 'time': None}
        for pid in pids:
            stat[pid] = lst.copy()

        # Get stat
        # If there's any AC, then select AC
        # Otherwise, select the nearest ones
        for subs in submissions[id]['subs']:
            pid = int(subs[1])
            if(stat[pid]['res'] == 90):
                continue
            elif(int(subs[2]) == 90):
                stat[pid]['res'] = int(subs[2])
            elif(stat[pid]['res'] == None):
                stat[pid]['res'] = int(subs[2])
                stat[pid]['time'] = int(subs[4])
            elif(stat[pid]['time'] > int(subs[4])):
                stat[pid]['res'] = int(subs[2])
                stat[pid]['time'] = int(subs[4])
        
        # Collect results
        for pid in pids:
            res = None
            if(stat[pid]['res'] is not None):
                res = id_to_stat[int(stat[pid]['res'])]
            pnum = pid_to_pnum[pid]
            ret[uname_to_username[uname]][pnum] = res
    return ret

def get_uva_data(users, unames, pnums):
    '''
        receive usernames ans pnums (list type)
        return a dictionary in format: {'username': [stat, stat, stat, ...], 'username2': [stat, stat, ...]}
    '''
    uids = []
    uname_to_username = {}
    for i in range(len(unames)):
        uids.append(get_uid(unames[i]))
        try:
            uname_to_username[unames[i]] = users[i]
        except:
            pass

    pids = []
    pid_to_pnum = {}
    for pnum in pnums:
        current_app.logger.info(f'checking pnum: {int(pnum)}')
        pid = get_pid(int(pnum))
        pids.append(pid)
        pid_to_pnum[pid] = int(pnum)
    
    #current_app.logger.info(f'get subs: {get_all_subs(uids, pids)}')
    subs = json.loads(get_all_subs(uids, pids))
    return get_all_stat(uname_to_username, pids, pid_to_pnum, subs)
