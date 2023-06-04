'''Make a list of objects in the AWS bucket that are captured. E.g.:
*** Confirm that all grid-ID (gid) in our jurisdiction, are captured in the mirror.
'''
import os
import json
import datetime
from misc import time_stamp
from gid import bc

# grid-ID over BC from our records (thanks adyk at PFC)
bc_row = bc() # os.popen("python3 ~/GitHub/wps-research/py/sentinel2_bc_tiles_shp/bc_row.py").read().strip().split()

data = os.popen(' '.join(['aws',  # read data from aws
                          's3api',
                          'list-objects',
                          '--no-sign-request',
                          '--bucket sentinel-products-ca-mirror'])).read()
ts = time_stamp()
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

rows = set(rows)
print("Number of gid:", len(rows))
print("Number of BC gid:", len(bc_row))
bc_row = set(bc_row)

rows_outside = []
for row in rows:  # check for rows that are not over bc (according to our records of the necessary rows)
    if row not in bc_row:
        rows_outside += [row]

print('Number of gid outside bc:', len(rows_outside))
print(' '.join(rows_outside))

for row in bc_row:  # check for rows (according to our records) that are not being captured in AWS
    if row not in rows:
        print('Error: bc gid not found:', row)  # when we ran it, all rows were represented
