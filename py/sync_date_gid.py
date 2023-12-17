''' 
20230526 download data for each 5-char "UTM tiling-grid ID":
        https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59
specified, 
for specified date: yyyymmdd only

python3 sync_date_gid.py [date: yyyymmdd] e.g.
python3 sync_date_gid.py 20230525

e.g. Donnie Creek (G80280) example:
python3 ~/GitHub/wps-active/py/sync_date_gid.py   20230915 10VEJ

e.g. current data over Kamloops:
python3 ~/GitHub/wps-active/py/sync_date_gid.py 20231123 10UFB

e.g. for NTFS001:
python3 ~/GitHub/wps-active/sync_date_gid.py 20230530 10VEM 10VFM 

e.g. for NTSSO08:
python3 ~/GitHub/wps-active/sync_date_gid.py 20230530 11VLG 11VLH 11VMH 11VMG
'''

import os
import sys
import json
import datetime

args, sep, exists = sys.argv, os.path.sep, os.path.exists
my_path = sep.join(os.path.abspath(__file__).split(sep)[:-1]) + sep

def download_by_gids(gids, date_string):
    # Creates a timestamp in "yyyymmddhhmmss" format
    now = datetime.datetime.now()
    [year, month, day, hour, minute, second] = [str(now.year).zfill(4),
                                                str(now.month).zfill(2),
                                                str(now.day).zfill(2),
                                                str(now.hour).zfill(2),
                                                str(now.minute).zfill(2),
                                                str(now.second).zfill(2)]
    ts = ''.join([year, month, day, hour, minute, second])

    # Reads the data from AWS
    cmd = ' '.join(['aws',
                    's3api',
                    'list-objects',
                    '--no-sign-request',
                    '--bucket', 'sentinel-products-ca-mirror'])
    data = os.popen(cmd).read()

    # Parses the JSON data
    d = json.loads(data)

    # Extracts the data records, one per dataset
    data = d['Contents']
    for d in data:
        key, modified, file_size = d['Key'].strip(), d['LastModified'], d['Size']
        w = [x.strip() for x in key.split('/')]
        if w[0] == 'Sentinel-2':
            f = w[-1]
            fw = f.split('_')
            gid = fw[5][1:]
            ts = fw[2].split('T')[0]

            # Only level-2 for selected date and gid
            if fw[1] != 'MSIL1C' or ts != date_string or gid not in gids:
                continue
            print(d)
            dest = 'L1_' + ts + sep + f
            cmd = ' '.join(['aws',
                            's3',
                            'cp',
                            '--no-sign-request',
                            's3://sentinel-products-ca-mirror/' + key,
                            dest])
            if not exists(dest) or file_size != os.path.getsize(dest):
                print(cmd)
                a = os.system(cmd)

# Gets Gaofen Image Dataset(GIDs) from command line
gids = []
if len(args) > 2:
    gids = set(args[2:])

# If no GIDs provided, default to all gids for BC
if len(gids) == 0:
    print('Error: No GIDs provided.')
    sys.exit(1)

yyyymmdd = args[1]
if len(yyyymmdd) != 8:
    print('Error: Expected date in format yyyymmdd.')
    sys.exit(1)

print("GIDs:", gids)
print("Date:", yyyymmdd)

# Running our `download_by_gids` function
download_by_gids(gids, yyyymmdd)
print('Done')