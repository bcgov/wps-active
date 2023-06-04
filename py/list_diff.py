'''20230317 relative to Sentinel-2 tiles selected by us, determine at a point in time:
    which records have been added since the last run.

TODO: copy the script to retrieve the jurisdiction-specific (e.g. BC) grid-id, to this repo. 
'''
import os
import sys
import json
import datetime


lines = [x.strip() for x in os.popen('ls -1 *_objects.txt').readlines()]
lines.sort()
latest = lines[-1]
old_ts = latest.split('_')[0]
if len(old_ts) != len('20230316233654'):
    print("Error: ", latest)
    sys.exit(1)

# row ID over BC from our records (thanks adyk)
bc_rows = set(os.popen("python3 ~/GitHub/wps-research/py/sentinel2_bc_tiles_shp/bc_row.py").read().strip().split())

now = datetime.datetime.now()  # create timestamp
[year, month, day, hour, minute, second] = [str(now.year).zfill(4),
                                            str(now.month).zfill(2),
                                            str(now.day).zfill(2),
                                            str(now.hour).zfill(2),
                                            str(now.minute).zfill(2),
                                            str(now.second).zfill(2)]
ts = ''.join([year, month, day, hour, minute, second])  # time stamp

if old_ts > ts:
    print("Error: past timestamp in future"); sys.exit(1)

data = os.popen(' '.join(['aws',  # read data from aws
                          's3api',
                          'list-objects',
                          '--no-sign-request',
                          '--bucket sentinel-products-ca-mirror'])).read()


d1 = json.loads(data)
d0 = json.loads(open(latest).read())

df = ts + '_objects.txt'  # file to write
print('+w', df)
open(df, 'wb').write(data.encode())  # write json data to file

def list_products(d):
    data = d['Contents']  # extract the data records, one per dataset
    my_list = {}

    for d in data:
        key = d['Key'].strip()
        w = [x.strip() for x in key.split('/')]
        if w[0] == 'Sentinel-2':
            f = w[-1]
            row = f.split('_')[5][1:]
            if row in bc_rows:
                modified = d['LastModified']
                my_list[f] = modified
    return my_list

l0, l1 = list_products(d0), list_products(d1)


added = []
modif = []
remov = []
for k in l1:
    if k not in l0:
        print(ts, "ADDED:", k, l1[k])
        added += [[k, l1[k]]]
    else:
        if l1[k] != l0[k]:
            print(ts, "MODIF:", l1[k])
            modif += [[k, l1[k]]]

for k in l0:
    if k not in l1:
        print(ts, "REMOV:", k, l0[k])
        remov += [[k, l0[k]]]

if len(added) > 0:
    open(ts + '_added.txt', 'wb').write(('\n'.join([' '.join(x) for x in added])).encode())

if len(remov) > 0:
    open(ts + '_remov.txt', 'wb').write(('\n'.join([' '.join(x) for x in remov])).encode())

if len(modif) > 0:
    open(ts + '_modif.txt', 'wb').write(('\n'.join([' '.join(x) for x in modif])).encode())


