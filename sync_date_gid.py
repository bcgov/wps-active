''' 20230526 download data for each 6-char "UTM tiling-grid ID":
        https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59
specified, 
for specified date: yyyymmdd only

python3 sync_date_gid.py [date: yyyymmdd] e.g.
python3 sync_date_gid.py 20230525
'''
import os
import sys
import json
import datetime
args, sep, exists = sys.argv, os.path.sep, os.path.exists
my_path = sep.join(os.path.abspath(__file__).split(sep)[:-1]) + sep


def download_by_gids(gids, date_string):
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
    # print(cmd)
    data = os.popen(cmd).read()

    if not exists(my_path + 'listing'):  # json backup for analysis
        os.mkdir(my_path + 'listing')
    df = my_path + 'listing' + sep + ts + '_objects.txt'  # file to write
    # print('+w', df)
    open(df, 'wb').write(data.encode())  # record json to file

    latest = {}
    d = json.loads(data)  # parse the json
    data = d['Contents']  # extract the data records, one per dataset
    for d in data:
        key, modified, file_size = d['Key'].strip(), d['LastModified'], d['Size']
        w = [x.strip() for x in key.split('/')]
        if w[0] == 'Sentinel-2':
            f = w[-1]
            fw = f.split('_')
            gid = fw[5]  # e.g. T10UGU
            ts = fw[2].split('T')[0]  # e.g. 20230525
            if fw[1] != 'MSIL2A' or ts != date_string or gid not in gids:  # only level-2 for selected date and gid
                continue
            # print(d)

            f = key.split('/')[-1]
            dest = 'L2_' + ts + sep + f
            cmd = ' '.join(['aws',
                            's3',
                            'cp',
                            '--no-sign-request',
                            's3://sentinel-products-ca-mirror/' + key,
                            dest])
            if not exists(dest):
                pass
                print(cmd)
                a = os.system(cmd) # uncomment this to do the download.
            else:
                if file_size != os.path.getsize(dest):
                    print("WARNING: wrong size")

    

# get gids from command line
gids = [] # set(args[1:])

if len(gids) == 0:  # if no gids provided, default to all gids for BC
    from gid import bc
    gids = bc()
# print(agids)

yyyymmdd = args[1]
if len(yyyymmdd) != 8:
    print('Error: expected date in format yyyymmdd')
    sys.exit(1)
#  make it go
download_by_gids(gids, yyyymmdd)
print('done')
