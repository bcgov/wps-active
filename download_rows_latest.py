import os
import sys
import json
import datetime

# row ID over BC from our records (thanks adyk)
bc_row = os.popen("python3 ~/GitHub/wps-research/py/sentinel2_bc_tiles_shp/bc_row.py").read().strip().split()
bc_row = set(bc_row)

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
data, rows = d['Contents'], []  # extract the data records, one per dataset

for d in data:
    key = d['Key'].strip()
    modified = d['LastModified']
    w = [x.strip() for x in key.split('/')]
    if w[0] == 'Sentinel-2':
        f = w[-1]
        row = f.split('_')[5][1:]

rows = set(rows)

bc_row = os.popen("python3 ~/GitHub/wps-research/py/sentinel2_bc_tiles_shp/bc_row.py").read().strip().split()
# print(bc_row)
print(len(bc_row))

bc_row = set(bc_row)

rows_outside = []
for row in rows:  # check for rows that are not over bc (according to our records of the necessary rows)
    if row not in bc_row:
        rows_outside += [row]

print('rows outside bc:')
print(' '.join(rows_outside))

for row in bc_row:  # check for rows (according to our records) that are not being captured in AWS
    if row not in rows:
        print('Error: not found:', row)  # when we ran it, all rows were represented


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
