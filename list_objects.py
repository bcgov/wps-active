import os
import json
import datetime

# row ID over BC from our records (thanks adyk)
bc_row = os.popen("python3 ~/GitHub/wps-research/py/sentinel2_bc_tiles_shp/bc_row.py").read().strip().split()

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
    w = [x.strip() for x in key.split('/')]
    if w[0] == 'Sentinel-2':
        f = w[-1]
        row = f.split('_')[5][1:]
        rows += [row]

rows = list(set(rows))
print(rows)
print(len(rows))

bc_row = os.popen("python3 ~/GitHub/wps-research/py/sentinel2_bc_tiles_shp/bc_row.py").read().strip().split()
# print(bc_row)
print(len(bc_row))
