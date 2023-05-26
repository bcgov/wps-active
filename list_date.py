'''Retrieve data listing by date, e.g. to count frames on day X'''
import os
import sys
import datetime

if len(os.popen("aws 2>&1").read().split("not found")) > 1:
    print('sudo apt install awscli')
    sys.exit(1)

if not os.path.exists("list_date"):
    os.mkdir("list_date")

now = datetime.date.today()
year, month, day = str(now.year).zfill(4), str(now.month).zfill(2), str(now.day).zfill(2)

print([year, month, day])
ls = 'aws s3 ls --no-sign-request'
path = 's3://sentinel-products-ca-mirror/Sentinel-2/'
c1, c2 = ' '.join([ls, path + 'S2MSI1C/']), ' '.join([ls, path + 'S2MSI2A/'])

def get(c):
    print(c)
    t = [x.strip() for x in os.popen(c).read().strip().split('\n')]
    return '\n'.join(t)

start_date = datetime.date(2022, 10, 31)
while start_date != now: 
    cd = '/'.join([str(start_date.year).zfill(4),
                   str(start_date.month).zfill(2),
                   str(start_date.day).zfill(2)]) + '/'
    open('list_date/S2MSI1C_' + cd.replace('/', ''), 'wb').write(get(c1 + cd).encode())
    open('list_date/S2MSI2A_' + cd.replace('/', ''), 'wb').write(get(c2 + cd).encode())
    start_date += datetime.timedelta(days=1)

open('list_date/S2MSI1C_' + cd.replace('/', ''), 'wb').write(get(c1 + cd).encode())
open('list_date/S2MSI2A_' + cd.replace('/', ''), 'wb').write(get(c2 + cd).encode())
