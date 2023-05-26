''' 20230317 download latest avail. data for each 6-char "UTM tiling-grid ID":
        https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59

    * can provide a list of such 5-character codes, as command args
        e.g. tested this for (over BC):
            T08UPC T10UGU T08VMK T08UPG T10UFU T08UNG T11UMV T07VFE T11ULP
NB this script pulls latest frame for the seleted gid, whether L1 or L2
    20230525: update from 5-letter code (T prefix) to general 6-letter code
    20230525: include BC gid in this file
    20230525: handle fetching multiple zip file for the same (date, gid)
'''
import os
import sys
import json
import datetime
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
            gid = f.split('_')[5]  # e.g. T10UGU

            if gid in gids:  # look at selected gid
                date, time = modified.split('T')
                date = [int(x) for x in date.split('-')]
                time = [int(float(x)) for x in time.strip('Z').split(':')]
                modified = datetime.datetime(date[0], date[1], date[2],
                                             time[0], time[1], time[2])

                # record latest observation(s) for this gid
                if (gid not in latest) or (latest[gid][0][0] > modified):
                    if gid not in latest:
                        latest[gid] = []
                    latest[gid] += [[modified, key]]

    for gid in latest:
        for latest_i in latest[gid]:
            modified, key = latest_i
            f = key.split('/')[-1]

            cmd = ' '.join(['aws',
                            's3',
                            'cp',
                            '--no-sign-request',
                            's3://sentinel-products-ca-mirror/' + key,
                            f])
            print(cmd)
            # a = os.system(cmd) # uncomment this to do the download.


# get gids from command line
gids = set(args[1:])

if gids == []:  # if no gids provided, default to all gids for BCa
    gids = ['T09UXR', 'T10UGB', 'T09VVF', 'T10UCG', 'T10UDG', 'T11ULB',
            'T11ULT', 'T09VWG', 'T10UFF', 'T11UPQ', 'T08VPK', 'T07VFG',
            'T09VXF', 'T10UCE', 'T08VPL', 'T10UFV', 'T09UWA', 'T10UCF',
            'T08UPD', 'T11UQQ', 'T10UDV', 'T07VFF', 'T09UWV', 'T09UUA',
            'T08UQC', 'T09UVV', 'T11UPS', 'T11UMS', 'T10VDK', 'T10VCK',
            'T11UNR', 'T09UYQ', 'T09UWT', 'T10UEG', 'T09VXG', 'T10UFC',
            'T11VLD', 'T09VUG', 'T09UWB', 'T09UYS', 'T10VCL', 'T09VUC',
            'T10UGD', 'T09UVU', 'T11VLF', 'T10UCV', 'T10VEL', 'T10VFM',
            'T08UQD', 'T09UUV', 'T11UMT', 'T10UFE', 'T11ULS', 'T11ULU',
            'T09UVS', 'T08UPF', 'T11UMU', 'T10VFJ', 'T10UDA', 'T09UXA',
            'T09UXQ', 'T10VCH', 'T09UYR', 'T09UYP', 'T09VUF', 'T10UFG',
            'T10UEV', 'T10UGV', 'T11VLC', 'T09VVD', 'T10UEC', 'T10VCM',
            'T10VDL', 'T09UWR', 'T10UGA', 'T09VUD', 'T10UGE', 'T10VEK',
            'T10UDU', 'T07VEG', 'T10UFA', 'T10VDH', 'T08VPH', 'T11ULA',
            'T09UXT', 'T11VLE', 'T08VNM', 'T08VLL', 'T11UNS', 'T10VFL',
            'T10UCB', 'T10VDM', 'T09VWF', 'T10VEH', 'T10VFK', 'T08VMM',
            'T10UFB', 'T09VXC', 'T10UDD', 'T10UEE', 'T09VUE', 'T10UDB',
            'T09VXD', 'T09UWU', 'T11VLG', 'T11UNQ', 'T11ULR', 'T11ULV',
            'T08VNK', 'T08VPJ', 'T09UUU', 'T09UUT', 'T10VCJ', 'T09UYT',
            'T09VXE', 'T10UGC', 'T08VNL', 'T09UYU', 'T11UMQ', 'T08VLM',
            'T09UXB', 'T11UNT', 'T09VVC', 'T10UEB', 'T10UFD', 'T08VML',
            'T11UPR', 'T10UDE', 'T09UVA', 'T10UCC', 'T08VPM', 'T09UXS',
            'T10VEM', 'T10VEJ', 'T10UCD', 'T10UED', 'T09VWE', 'T09VWC',
            'T09VWD', 'T09UXU', 'T09UVB', 'T09UWS', 'T10UDC', 'T09UVT',
            'T09UXV', 'T09VVG', 'T10UDF', 'T08UQE', 'T09VVE', 'T10UEA',
            'T09UYV', 'T10UCA', 'T10VFH', 'T10UCU', 'T11ULQ', 'T10VDJ',
            'T08UPE', 'T10UEF', 'T11UMR']

#  make it go
download_by_gids(gids)
