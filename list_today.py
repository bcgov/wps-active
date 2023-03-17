'''save data by tiles'''
import os
import sys
import datetime

bc_row = os.popen("python3 ~/GitHub/wps-research/py/sentinel2_bc_tiles_shp/bc_row.py").read().strip().split()
print(bc_row)

if len(os.popen("aws 2>&1").read().split("not found")) > 1:
    print('Need to install aws cli:')
    print('  sudo apt install awscli')
    sys.exit(1)

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

start_date = now

cd = '/'.join([str(start_date.year).zfill(4),
               str(start_date.month).zfill(2),
               str(start_date.day).zfill(2)]) + '/'

c1_d = get(c1 + cd)  # Level-1 data listings
open('S2MSI1C_' + cd.replace('/', ''), 'wb').write(c1_d.encode())

c2_d = get(c2 + cd) # Level-2 data listings
open('S2MSI2A_' + cd.replace('/', ''), 'wb').write(c2_d.encode())

# aws s3 cp  --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI1C/2023/03/08/S2B_MSIL1C_20230308T190239_N0509_R013_T10UFB_20230308T223026.zip S2B_MSIL1C_20230308T190239_N0509_R013_T10UFB_20230308T223026.zip
