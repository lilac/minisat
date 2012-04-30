#!/usr/bin/env python
import re

exps = [
        ('nVar', 'Number of variables:\\s*(\\d+)'),
        ('nCls', r'Number of clauses:\s*(\d+)'),
        ('time', r'CPU time\s*:\s*(?P<time>[\d|\.]+)')
        ]

REs = [(n, re.compile(e)) for (n, e) in exps]

def parse(fn):
    res = {}
    with open(fn, 'r') as log:
        for line in log:
            for (n, re) in REs:
                m = re.search(line)
                if m:
                    res[n] = m.group(1)
        res['ans'] = line.strip()
    return res

def sort_dict(a):
    return sorted(a.items(), key = lambda x: x[0])

def print_stat(info, stat):
    print('*** ' + info + ' ***')
    import pprint
    #pp = pprint.PrettyPrinter(indent=4)
    
    pprint.pprint(stat)
    print('\n')

dirs = ['jarvisalo', 'UUF250']
grows = ['0', '100', '1000']

import sys
import os, glob

stats = {}
cmp = {}
for d in dirs:
    cmp[d] = {}
    stats[d] = {}
    for g in grows:
        ext = '' if g == '0' else '.' + g
        dir = 'log/minisat.' + d + ext
        
        stats[d][g] = {}
       
        for file in glob.glob(dir + "/*.log"):
            basename = os.path.basename(file)
            stats[d][g][basename] = parse(file)

            if basename not in cmp[d].keys():
                cmp[d][basename] = {}
            cmp[d][basename][g] = stats[d][g][basename]['time']

        #stat = sort_dict(stats[d][g])
        #print_stat(dir, stat)

    print_stat(d, cmp[d])

#print (stats)
#print (parse(sys.argv[1]))
