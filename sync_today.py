'''save data by tiles'''
import os
import sys
import datetime
if len(os.popen("aws 2>&1").read().split("not found")) > 1:
    print('sudo apt install awscli')
    sys.exit(1)

now = datetime.date.today()
year, month, day = str(now.year).zfill(4), str(now.month).zfill(2), str(now.day).zfill(2)
print([year, month, day])

def get(c):
    print(c)
    t = [x.strip() for x in os.popen(c).read().strip().split('\n')]
    return '\n'.join(t)

start_date = now

cd = '/'.join([str(start_date.year).zfill(4),
               str(start_date.month).zfill(2),
               str(start_date.day).zfill(2)]) + '/'
cmd = 'aws s3 sync --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/' + cd + ' ./L2_' + year + month + day + '/'
print(cmd)
