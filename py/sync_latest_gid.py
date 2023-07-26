''' 20230317 download latest avail. data for each 6-char "UTM tiling-grid ID":
        https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59

    * can provide a list of such 5-character codes, as command args
        e.g. tested this for (over BC):
            T08UPC T10UGU T08VMK T08UPG T10UFU T08UNG T11UMV T07VFE T11ULP
NB this script pulls latest frame for the seleted gid, whether L1 or L2
    20230525: update from 5-letter code (T prefix) to general 6-letter code
    20230525: include BC gid in this file
    20230525: handle fetching multiple zip file for the same (date, gid)
    20230525: need to modify this to use the L2_ etc. folder convention
'''
import os
import sys
import json
import datetime

# PARAMETER
use_L2 = True # set to False to fetch L1

# start program
args, sep, exists = sys.argv, os.path.sep, os.path.exists
my_path = sep.join(os.path.abspath(__file__).split(sep)[:-1]) + sep


def download_by_gids(gids):
    now = datetime.datetime.now()  # create timestamp yyyymmddhhmmss
    [year, month, day, hour, minute, second] = [str(now.year).zfill(4),
                                                str(now.month).zfill(2),
                                                str(now.day).zfill(2),
                                                str(now.hour).zfill(2),
                                                str(now.minute).zfill(2),
                                                str(now.second).zfill(2)]
    ts = ''.join([year, month, day, hour, minute, second])

    cmd = ' '.join(['aws',  # read data from aws
                    's3api',
                    'list-objects',
                    '--no-sign-request',
                    '--bucket sentinel-products-ca-mirror'])
    print(cmd)
    data = os.popen(cmd).read()

    if not exists(my_path + 'listing'):  # json backup for analysis
        os.mkdir(my_path + 'listing')
    df = my_path + 'listing' + sep + ts + '_objects.txt'  # file to write
    print('+w', df)
    open(df, 'wb').write(data.encode())  # record json to file

    latest = {}
    d = json.loads(data)  # parse the json
    data = d['Contents']  # extract the data records, one per dataset
    for d in data:
        key, modified = d['Key'].strip(), d['LastModified']
        w = [x.strip() for x in key.split('/')]
        if w[0] == 'Sentinel-2':
            f = w[-1]
            fw = f.split('_')
            gid = fw[5]  # e.g. T10UGU
            ts = fw[2].split('T')[0]  # e.g. 20230525
            if fw[1] != ('MSIL2A' if use_L2 else 'MSIL1C'):
                continue
            # print(w)
            print(gid, gids)
            if gid in gids:  # consider record if has selected gid
                date_str, time = modified.split('T')
                date = [int(x) for x in date_str.split('-')]
                time = [int(float(x)) for x in time.strip('Z').split(':')]

                # record latest observation(s) for this gid
                if (gid not in latest) or ts > latest[gid][0][0]:
                    if gid not in latest:
                        latest[gid] = []
                    latest[gid] = [[ts, key]] + latest[gid]  # put more recent dates first
                    print("update", gid, ts, key)

    for gid in latest:
        # print("gid", gid)
        ts_latest = latest[gid][0][0]
        for latest_i in latest[gid]:
            ts, key = latest_i
            if ts != ts_latest:
                break
            f = key.split('/')[-1]

            dest = ('L2_' if use_L2 else 'L1_') + ts + sep + f
            cmd = ' '.join(['aws',
                            's3',
                            'cp',
                            '--no-sign-request',
                            's3://sentinel-products-ca-mirror/' + key,
                            dest])
            if not exists(dest):
                print(cmd)
                a = os.system(cmd) # uncomment this to do the download.

# get gids from command line
has_error = False
gids = set(args[1:])
for g in gids:
    if len(g) != 6:
        print("Error: 6-letter code expected e.g. T10UFB")
        has_error = True
if has_error:
    err("please check gid codes and try again")

if len(gids) == 0:  # if no gids provided, default to all gids for BC
    from gid import bc
    gids = bc()

print(gids)

#  make it go
download_by_gids(gids)
print('done')
