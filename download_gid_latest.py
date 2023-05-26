''' 20230317 download latest avail. data for each 6-character "UTM tiling-grid ID" https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59
* can provide a list of such 5-character codes, to this script as command args

e.g. tested this for:
T08UPC T10UGU T08VMK T08UPG T10UFU T08UNG T11UMV T07VFE T11ULP T09UUS T08UNF T11UNP T08VMJ T08VLJ T12UUA T10UEU T08UNE T08VLK T09UUB T11UQR T08VNJ T12UUV T08VNH T08VLH T08UMG T09UVR T11UMP T08VMH
over BC

NB this script pulls latest frame for the seleted gid, regardless of whether it's L1 or L2

20230525: update from 5-letter code (T prefix) to general 6-letter code
20230525: fetch multiple zip file for the same (date, gid) if there are multiple such zip files! 
'''
import os
import sys
import json
import datetime
args = sys.argv
gids = set(args[1:])

if len(gids) == 0:  # default to all footprints over BC
    gids = open('gid/BC').read().strip().split()

now = datetime.datetime.now()  # create timestamp: yyyymmddhhmmss
[year, month, day, hour, minute, second] = [str(now.year).zfill(4),
                                            str(now.month).zfill(2),
                                            str(now.day).zfill(2),
                                            str(now.hour).zfill(2),
                                            str(now.minute).zfill(2),
                                            str(now.second).zfill(2)]
ts = ''.join([year, month, day, hour, minute, second])  # time stamp: yyyymmddhhmmss

data = os.popen(' '.join(['aws',  # read data from aws
                          's3api',
                          'list-objects',
                          '--no-sign-request',
                          '--bucket sentinel-products-ca-mirror'])).read()

df = ts + '_objects.txt'  # file to write
print('+w', df)
open(df, 'wb').write(data.encode())  # record json data to file


latest = {}
d = json.loads(data)  # parse the json-format data
data = d['Contents'] # extract the data records, one per dataset
for d in data:
    key, modified = d['Key'].strip(), d['LastModified']
    w = [x.strip() for x in key.split('/')]
    if w[0] == 'Sentinel-2':
        f, gid = w[-1], f.split('_')[5]
        if gid in gids: # "2022-11-28T19:10:40.000Z"
            date, time = modified.split('T')
            date = [int(x) for x in date.split('-')]
            time = [int(float(x)) for x in time.strip('Z').split(':')]
            modified = datetime.datetime(date[0], date[1], date[2], time[0], time[1], time[2])
 
            # record latest observation(s) this gid           
            if (gid not in latest) or (latest[gid][0] > modified):
				if not gid in latest:
					latest[gid] = []
                latest[gid] += [[modified, key]]

for gid in latest:
    for a_latest in latest:
        modified, key = latest[gid]
        f = key.split('/')[-1]

        cmd = ' '.join(['aws',
                        's3',
                        'cp',
                        '--no-sign-request',
                        's3://sentinel-products-ca-mirror/' + key,
                        f])
        print(cmd)
        # a = os.system(cmd) # uncomment this to do the download.

''' # example output:
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/15/S2B_MSIL2A_20230315T185139_N0509_R113_T10UGU_20230315T230515.zip S2B_MSIL2A_20230315T185139_N0509_R113_T10UGU_20230315T230515.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/16/S2B_MSIL2A_20230316T200159_N0509_R128_T08UPC_20230316T223836.zip S2B_MSIL2A_20230316T200159_N0509_R128_T08UPC_20230316T223836.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/16/S2B_MSIL2A_20230316T200159_N0509_R128_T08UPG_20230316T223836.zip S2B_MSIL2A_20230316T200159_N0509_R128_T08UPG_20230316T223836.zip
# ... '''
