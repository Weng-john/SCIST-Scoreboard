pids = [194, 60, 539]
submissions = {'975658': {'name': '林禾堃', 'uname': 'Koios1143', 'subs': [[26330364, 194, 50, 3000, 1619183579, 5, -1], [26332028, 194, 50, 3000, 1619227218, 5, -1], [26332034, 194, 50, 3000, 1619227342, 5, -1], [26320053, 539, 70, 20, 1618924849, 5, -1], [26319819, 539, 70, 30, 1618920884, 5, -1], [26320028, 539, 70, 30, 1618924530, 5, -1], [26319830, 539, 70, 40, 1618921110, 5, -1], [26327018, 60, 90, 0, 1619099672, 5, 1388], [26327162, 60, 90, 0, 1619101663, 5, 1389], [26320123, 539, 90, 20, 1618925732, 5, 56], [25141498, 539, 90, 30, 1592205341, 5, 93], [25139597, 539, 90, 50, 1592145617, 5, 159]]}}
id_to_stat = {10: 'SE', 15: 'CBJ', 20: 'IQ', 30: 'CE', 35: 'RF', 40: 'RE', 45: 'OE', 50: 'TLE', 60: 'MLE', 70: 'WA', 80: 'PE', 90: 'AC'}
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
    uname = submissions[id]['uname']
    stat = {}
    ret[uname] = {}
    res = None
    lst = {'10' : 0, '15' : 0, '20' : 0, '30' : 0, '35' : 0, '40' : 0, '45' : 0, '60' : 0, '70' : 0, '80' : 0, '90' : 0, 'tot': 0}
    lst = {'res': None, 'time': None}
    for pid in pids:
        stat[pid] = lst.copy()

    for subs in submissions[id]['subs']:
        pid = int(subs[1])
        if(stat[pid]['res'] == 90):
            continue
        elif(stat[pid]['res'] == None):
            stat[pid]['res'] = int(subs[2])
            stat[pid]['time'] = int(subs[4])
        elif(stat[pid]['time'] > int(subs[4])):
            stat[pid]['res'] = int(subs[2])
            stat[pid]['time'] = int(subs[4])
    for pid in pids:
        res = None
        if(stat[pid]['res'] is not None):
            res = id_to_stat[int(stat[pid]['res'])]
        ret[uname][pid] = res
print(ret)