''' 20230317 download the latest available data for each 5-character row-index/ID (tile/footprint ID) or whatever.
List of 5-character symbols are listed as command-line arguments

e.g. for:
08UPC 10UGU 08VMK 08UPG 10UFU 08UNG 11UMV 07VFE 11ULP 09UUS 08UNF 11UNP 08VMJ 08VLJ 12UUA 10UEU 08UNE 08VLK 09UUB 11UQR 08VNJ 12UUV 08VNH 08VLH 08UMG 09UVR 11UMP 08VMH
'''
import os
import sys
import json
import datetime
args = sys.argv
rows = set(args[1:])

now = datetime.datetime.now()  # create timestamp
[year, month, day, hour, minute, second] = [str(now.year).zfill(4),
                                            str(now.month).zfill(2),
                                            str(now.day).zfill(2),
                                            str(now.hour).zfill(2),
                                            str(now.minute).zfill(2),
                                            str(now.second).zfill(2)]
ts = ''.join([year, month, day, hour, minute, second])  # time stamp

data = os.popen(' '.join(['aws',  # read data from aws
                          's3api',
                          'list-objects',
                          '--no-sign-request',
                          '--bucket sentinel-products-ca-mirror'])).read()

df = ts + '_objects.txt'  # file to write
print('+w', df)
open(df, 'wb').write(data.encode())  # write json data to file

d = json.loads(data)  # load the json-format data
data = d['Contents'] # extract the data records, one per dataset

latest = {}
for d in data:
    key = d['Key'].strip()
    modified = d['LastModified']
    w = [x.strip() for x in key.split('/')]
    if w[0] == 'Sentinel-2':
        f = w[-1]
        row = f.split('_')[5][1:]
        if row in rows:
            # "2022-11-28T19:10:40.000Z"
            date, time = modified.split('T')
            date = [int(x) for x in date.split('-')]
            time = [int(float(x)) for x in time.strip('Z').split(':')]
            modified = datetime.datetime(date[0], date[1], date[2], time[0], time[1], time[2])
            if (row not in latest) or (latest[row][0] > modified):
                latest[row] = [modified, key]

for row in latest:
    modified, key = latest[row]
    f = key.split('/')[-1]

    cmd = ' '.join(['aws',
                    's3',
                    'cp',
                    '--no-sign-request',
                    's3://sentinel-products-ca-mirror/' + key,
                    f])
    print(cmd)


'''
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/15/S2B_MSIL2A_20230315T185139_N0509_R113_T10UGU_20230315T230515.zip S2B_MSIL2A_20230315T185139_N0509_R113_T10UGU_20230315T230515.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/16/S2B_MSIL2A_20230316T200159_N0509_R128_T08UPC_20230316T223836.zip S2B_MSIL2A_20230316T200159_N0509_R128_T08UPC_20230316T223836.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/16/S2B_MSIL2A_20230316T200159_N0509_R128_T08UPG_20230316T223836.zip S2B_MSIL2A_20230316T200159_N0509_R128_T08UPG_20230316T223836.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/16/S2B_MSIL2A_20230316T200159_N0509_R128_T09UUB_20230316T223836.zip S2B_MSIL2A_20230316T200159_N0509_R128_T09UUB_20230316T223836.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/15/S2A_MSIL2A_20230315T194151_N0509_R042_T09UUS_20230315T231958.zip S2A_MSIL2A_20230315T194151_N0509_R042_T09UUS_20230315T231958.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/16/S2A_MSIL2A_20230316T191131_N0509_R056_T10UEU_20230317T005400.zip S2A_MSIL2A_20230316T191131_N0509_R056_T10UEU_20230317T005400.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/16/S2A_MSIL2A_20230316T191131_N0509_R056_T10UFU_20230317T005400.zip S2A_MSIL2A_20230316T191131_N0509_R056_T10UFU_20230317T005400.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/15/S2B_MSIL2A_20230315T185139_N0509_R113_T11ULP_20230315T230515.zip S2B_MSIL2A_20230315T185139_N0509_R113_T11ULP_20230315T230515.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/15/S2B_MSIL2A_20230315T185139_N0509_R113_T11UMP_20230315T230515.zip S2B_MSIL2A_20230315T185139_N0509_R113_T11UMP_20230315T230515.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/16/S2A_MSIL2A_20230316T191131_N0509_R056_T11UMV_20230317T005400.zip S2A_MSIL2A_20230316T191131_N0509_R056_T11UMV_20230317T005400.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/15/S2B_MSIL2A_20230315T203219_N0509_R114_T07VFE_20230315T225437.zip S2B_MSIL2A_20230315T203219_N0509_R114_T07VFE_20230315T225437.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/15/S2B_MSIL2A_20230315T203219_N0509_R114_T08VLK_20230315T225437.zip S2B_MSIL2A_20230315T203219_N0509_R114_T08VLK_20230315T225437.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/14/S2A_MSIL2A_20230314T183131_N0509_R027_T11UQR_20230315T002301.zip S2A_MSIL2A_20230314T183131_N0509_R027_T11UQR_20230315T002301.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/14/S2A_MSIL2A_20230314T183131_N0509_R027_T12UUA_20230315T002301.zip S2A_MSIL2A_20230314T183131_N0509_R027_T12UUA_20230315T002301.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/14/S2A_MSIL2A_20230314T183131_N0509_R027_T12UUV_20230315T002301.zip S2A_MSIL2A_20230314T183131_N0509_R027_T12UUV_20230315T002301.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/14/S2A_MSIL2A_20230314T201211_N0509_R028_T08UMG_20230315T000207.zip S2A_MSIL2A_20230314T201211_N0509_R028_T08UMG_20230315T000207.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/16/S2B_MSIL2A_20230316T200159_N0509_R128_T08UNE_20230316T223836.zip S2B_MSIL2A_20230316T200159_N0509_R128_T08UNE_20230316T223836.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/16/S2B_MSIL2A_20230316T200159_N0509_R128_T08UNF_20230316T223836.zip S2B_MSIL2A_20230316T200159_N0509_R128_T08UNF_20230316T223836.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/16/S2B_MSIL2A_20230316T200159_N0509_R128_T08UNG_20230316T223836.zip S2B_MSIL2A_20230316T200159_N0509_R128_T08UNG_20230316T223836.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/14/S2A_MSIL2A_20230314T201211_N0509_R028_T08VLH_20230315T000207.zip S2A_MSIL2A_20230314T201211_N0509_R028_T08VLH_20230315T000207.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/14/S2A_MSIL2A_20230314T201211_N0509_R028_T08VMH_20230315T000207.zip S2A_MSIL2A_20230314T201211_N0509_R028_T08VMH_20230315T000207.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/15/S2B_MSIL2A_20230315T203219_N0509_R114_T08VMJ_20230315T225437.zip S2B_MSIL2A_20230315T203219_N0509_R114_T08VMJ_20230315T225437.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/15/S2B_MSIL2A_20230315T203219_N0509_R114_T08VMK_20230315T225437.zip S2B_MSIL2A_20230315T203219_N0509_R114_T08VMK_20230315T225437.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/16/S2B_MSIL2A_20230316T200159_N0509_R128_T08VNH_20230316T223836.zip S2B_MSIL2A_20230316T200159_N0509_R128_T08VNH_20230316T223836.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/16/S2B_MSIL2A_20230316T200159_N0509_R128_T08VNJ_20230316T223836.zip S2B_MSIL2A_20230316T200159_N0509_R128_T08VNJ_20230316T223836.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/15/S2B_MSIL2A_20230315T185139_N0509_R113_T11UNP_20230315T230515.zip S2B_MSIL2A_20230315T185139_N0509_R113_T11UNP_20230315T230515.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/15/S2B_MSIL2A_20230315T203219_N0509_R114_T08VLJ_20230315T225437.zip S2B_MSIL2A_20230315T203219_N0509_R114_T08VLJ_20230315T225437.zip
aws s3 cp --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/03/15/S2A_MSIL2A_20230315T194151_N0509_R042_T09UVR_20230315T231958.zip S2A_MSIL2A_20230315T194151_N0509_R042_T09UVR_20230315T231958.zip
'''
