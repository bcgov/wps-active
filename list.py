'''save data by tiles. NB this file includes obfuscation of Download paths which can be removed later'''
import os
import sys
import datetime

if len(os.popen("aws 2>&1").read().split("not found")) > 1:
    print('sudo apt install awscli')
    sys.exit(1)

if not os.path.exists("list"):
    os.mkdir("list")

now = datetime.date.today()
year, month, day = str(now.year).zfill(4), str(now.month).zfill(2), str(now.day).zfill(2)

print([year, month, day])
def incr(c): return chr(ord(c) + 1)
def decr(c): return chr(ord(c) - 1)
def cenc(s): return "".join([incr(si) for si in list(s)])
def cdec(s): return "".join([decr(si) for si in list(s)])
a = cdec("t4;00tfoujofm.qspevdut.db.njssps0")
ls = cdec("bxt!t4!mt!..op.tjho.sfrvftu!")
s2 = cdec("Tfoujofm.30")

c1 = ls + a + s2 + 'S2MSI1C/' # + '/'.join([year, month, day]) + '/' 
c2 = ls + a + s2 + 'S2MSI2A/' # + '/'.join([year, month, day]) + '/'

def get(c):
    print(c)
    t = [x.strip() for x in os.popen(c).read().strip().split('\n')]
    return '\n'.join(t)

start_date = datetime.date(2022, 10, 31)
while start_date != now: 
    cd = '/'.join([str(start_date.year).zfill(4),
                  str(start_date.month).zfill(2),
                  str(start_date.day).zfill(2)]) + '/'

    open('list/S2MSI1C_' + cd.replace('/', ''), 'wb').write(get(c1 + cd).encode())
    open('list/S2MSI2A_' + cd.replace('/', ''), 'wb').write(get(c2 + cd).encode())
    start_date += datetime.timedelta(days=1)

open('list/S2MSI1C_' + cd.replace('/', ''), 'wb').write(get(c1 + cd).encode())
open('list/S2MSI2A_' + cd.replace('/', ''), 'wb').write(get(c2 + cd).encode())

# aws s3 cp  --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI1C/2023/03/08/S2B_MSIL1C_20230308T190239_N0509_R013_T10UFB_20230308T223026.zip S2B_MSIL1C_20230308T190239_N0509_R013_T10UFB_20230308T223026.zip
