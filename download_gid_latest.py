''' 20230317 download latest avail. data for each 6-character "UTM tiling-grid ID" https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59
* can provide a list of such 5-character codes, to this script as command args
e.g. tested this for:
T08UPC T10UGU T08VMK T08UPG T10UFU T08UNG T11UMV T07VFE T11ULP T09UUS T08UNF T11UNP T08VMJ T08VLJ T12UUA T10UEU T08UNE T08VLK T09UUB T11UQR T08VNJ T12UUV T08VNH T08VLH T08UMG T09UVR T11UMP T08VMH
over BC
NB this script pulls latest frame for the seleted gid, regardless of whether it's L1 or L2

20230525: update from 5-letter code (T prefix) to general 6-letter code
20230525: include BC gid in this file
20230525: fetch multiple zip file for the same (date, gid) if there are multiple such zip files! 
'''
import os
import sys
import json
import datetime
args = sys.argv
gids = set(args[1:])

if len(gids) == 0:  # default to all footprints over BC
    gids = ['T09UXR', 'T10UGB', 'T09VVF', 'T10UCG', 'T10UDG', 'T11ULB', 'T11ULT', 'T09VWG', 'T10UFF', 'T11UPQ', 'T08VPK', 'T07VFG', 'T09VXF', 'T10UCE', 'T08VPL', 'T10UFV', 'T09UWA', 'T10UCF', 'T08UPD', 'T11UQQ', 'T10UDV', 'T07VFF', 'T09UWV', 'T09UUA', 'T08UQC', 'T09UVV', 'T11UPS', 'T11UMS', 'T10VDK', 'T10VCK', 'T11UNR', 'T09UYQ', 'T09UWT', 'T10UEG', 'T09VXG', 'T10UFC', 'T11VLD', 'T09VUG', 'T09UWB', 'T09UYS', 'T10VCL', 'T09VUC', 'T10UGD', 'T09UVU', 'T11VLF', 'T10UCV', 'T10VEL', 'T10VFM', 'T08UQD', 'T09UUV', 'T11UMT', 'T10UFE', 'T11ULS', 'T11ULU', 'T09UVS', 'T08UPF', 'T11UMU', 'T10VFJ', 'T10UDA', 'T09UXA', 'T09UXQ', 'T10VCH', 'T09UYR', 'T09UYP', 'T09VUF', 'T10UFG', 'T10UEV', 'T10UGV', 'T11VLC', 'T09VVD', 'T10UEC', 'T10VCM', 'T10VDL', 'T09UWR', 'T10UGA', 'T09VUD', 'T10UGE', 'T10VEK', 'T10UDU', 'T07VEG', 'T10UFA', 'T10VDH', 'T08VPH', 'T11ULA', 'T09UXT', 'T11VLE', 'T08VNM', 'T08VLL', 'T11UNS', 'T10VFL', 'T10UCB', 'T10VDM', 'T09VWF', 'T10VEH', 'T10VFK', 'T08VMM', 'T10UFB', 'T09VXC', 'T10UDD', 'T10UEE', 'T09VUE', 'T10UDB', 'T09VXD', 'T09UWU', 'T11VLG', 'T11UNQ', 'T11ULR', 'T11ULV', 'T08VNK', 'T08VPJ', 'T09UUU', 'T09UUT', 'T10VCJ', 'T09UYT', 'T09VXE', 'T10UGC', 'T08VNL', 'T09UYU', 'T11UMQ', 'T08VLM', 'T09UXB', 'T11UNT', 'T09VVC', 'T10UEB', 'T10UFD', 'T08VML', 'T11UPR', 'T10UDE', 'T09UVA', 'T10UCC', 'T08VPM', 'T09UXS', 'T10VEM', 'T10VEJ', 'T10UCD', 'T10UED', 'T09VWE', 'T09VWC', 'T09VWD', 'T09UXU', 'T09UVB', 'T09UWS', 'T10UDC', 'T09UVT', 'T09UXV', 'T09VVG', 'T10UDF', 'T08UQE', 'T09VVE', 'T10UEA', 'T09UYV', 'T10UCA', 'T10VFH', 'T10UCU', 'T11ULQ', 'T10VDJ', 'T08UPE', 'T10UEF', 'T11UMR']

now = datetime.datetime.now()  # create timestamp
[year, month, day, hour, minute, second] = [str(now.year).zfill(4),
                                            str(now.month).zfill(2),
                                            str(now.day).zfill(2),
                                            str(now.hour).zfill(2),
                                            str(now.minute).zfill(2),
                                            str(now.second).zfill(2)]
ts = ''.join([year, month, day, hour, minute, second])  # time stamp: yyyymmddhhmmss

cmd = ' '.join(['aws',  # read data from aws
                's3api',
                'list-objects',
                '--no-sign-request',
                '--bucket sentinel-products-ca-mirror'])
print(cmd)
data = os.popen(cmd).read()

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
        f = w[-1]  # e.g. f == 'S2A_MSIL1C_20221031T185531_N0400_R113_T10UGU_20221031T204816.zip'
        gid = f.split('_')[5]  # e.g. T10UGU

        # consider only selected gid
        if gid in gids:
            date, time = modified.split('T')  # e.g. modified == "2022-11-28T19:10:40.000Z"
            date = [int(x) for x in date.split('-')]
            time = [int(float(x)) for x in time.strip('Z').split(':')]
            modified = datetime.datetime(date[0], date[1], date[2], time[0], time[1], time[2])
 
            # record latest observation(s) this gid      
            # print("latest", latest)     
            if (gid not in latest) or (latest[gid][0][0] > modified):
                if not gid in latest:
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

''' # example output:
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/15/S2B_MSIL2A_20230315T185139_N0509_R113_T10UGU_20230315T230515.zip S2B_MSIL2A_20230315T185139_N0509_R113_T10UGU_20230315T230515.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/16/S2B_MSIL2A_20230316T200159_N0509_R128_T08UPC_20230316T223836.zip S2B_MSIL2A_20230316T200159_N0509_R128_T08UPC_20230316T223836.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/16/S2B_MSIL2A_20230316T200159_N0509_R128_T08UPG_20230316T223836.zip S2B_MSIL2A_20230316T200159_N0509_R128_T08UPG_20230316T223836.zip
# ... '''
