#!/usr/bin/env python3
from bs4 import BeautifulSoup
from datetime import datetime
from os import path, sep
import sys
from glob import glob
import re
import collections
from decimal import *
from jinja2 import Environment, PackageLoader


# REPORTS_DIR = 'C:\\NullpoMino\\report'  # windows example
REPORTS_DIR = '/home/china/report/test'  # linux example
YOUR_NAME = 'cn'  # change to your preferred nick
# note the double backslashes in windows paths.

output_dir = path.dirname(path.realpath(sys.argv[0]))
# output dir can be changed to somewhere else if wanted.
# just follow the directory format of REPORTS_DIR examples,
# and remember to place the res folder in the same dir for css.

statlist = []
processed = 0
for fname in glob(REPORTS_DIR + sep + '*.html'):
    if re.match('.*[0-9]\.html$', fname):
        soup = BeautifulSoup(open(fname))
        if processed == 1:  # lol
            print('\r' + str(processed) + ' log processed.', end='')
        else:
            print('\r' + str(processed) + ' logs processed.', end='')
        processed += 1  # just for displaying progress, so whatever

        general = soup.body.find(id="general").find_all('tr')
        lines = int(general[5].find('td').next_sibling.string)
        if 40 <= lines <= 43:  # only take completed games into consideration
            date = datetime.strptime(path.splitext(fname)[0]
                                     .split(sep)[-1], "%Y_%m_%d_%H_%M_%S")
            faults = int(soup.body.find(id="finesse").find('tr').find('td')
                         .next_sibling.string)
            time = Decimal(general[0].find('td').next_sibling.string[:-1])
            ppm = Decimal(general[1].find('td').next_sibling.string
                          .split()[0])
            pieces = int(general[4].find('td').next_sibling.string)

            linestats = soup.body.find(id="lines").find_all('tr')

            singles = int(linestats[4].find('td').next_sibling.string)
            doubles = int(linestats[5].find('td').next_sibling.string)
            triples = int(linestats[6].find('td').next_sibling.string)
            tetrises = int(linestats[7].find('td').next_sibling.string)

            manipstats = soup.body.find(id="manipulations").find_all('tr')

            rotations = int(manipstats[0].find('td').next_sibling.string)
            moves = int(manipstats[1].find('td').next_sibling.string)
            idealtime = Decimal(soup.body.find(id="stats").find('tr')
                                .find('td').next_sibling.string
                                .split()[0].replace(',', '.'))

            # i'll be using this later for graph data
            statlist.append({
                'date': date,
                'time': time,
                'ppm': ppm,
                'lines': lines,
                'faults': faults,
                'pieces': pieces,
                'singles': singles,
                'doubles': doubles,
                'triples': triples,
                'tetrises': tetrises,
                'rotations': rotations,
                'moves': moves,
                'idealtime': idealtime
            })
        else:
            continue

# reminder to rethink data struct instead of this,
# perhaps `{'a':['ordered','list','here']}` works better than statlist
res = collections.defaultdict(list)
for dick in statlist:
    for k, v in dick.items():
        res[k].append(v)

infodict = {
    'name': YOUR_NAME.upper(),
    'gendate': str(datetime.now()),
    'startdate': min(res['date']),
    'lastgame': max(res['date']),
    'rangedelta': max(res['date'])-min(res['date']),
    'totgames': len(statlist),
    'tothours': round(sum(res['time'])/60/60, 3),
    'totpieces': sum(res['pieces']),
    'totrots': sum(res['rotations']),
    'totmoves': sum(res['moves']),
    'totfaults': sum(res['faults']),
    'totlines': sum(res['lines']),
    'totsingles': sum(res['singles']),
    'totdoubles': sum(res['doubles']),
    'tottriples': sum(res['triples']),
    'tottetrises': sum(res['tetrises']),
    'avgppm': round(sum(res['ppm'])/len(res['ppm']), 3),
    'fastestppm': round(max(res['ppm']), 3),
    'avgtime': str(round(sum(res['time'])/len(res['time']), 3)) + "s",
    'fastesttime': str(round(min(res['time']), 3)) + "s"
}

env = Environment(loader=PackageLoader('moe'))
template = env.get_template('index.html')

# change filename if wanted, 'gatheredreport.html' is a pretty shit name
with open(output_dir + sep + 'gatheredreport.html', 'w') as f:
    f.write(template.render(infodict=infodict))
print('\nDone!')
