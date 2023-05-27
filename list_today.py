'''Jurisdiction specific (to be updated to be jurisdiction-flexible):

Determine the gid (grid-ID) for which Sentinel-2 data captured today are available

TODO: put the BC-specific gid info for Sentinel-2, into this repo and add gid info for other jurisdictions 
'''
import os
import sys
import datetime
from gid import bc

bc_gid = bc()
print("bc row-id under obs:", bc_gid)

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

def my_list(c2_d):
    lines, row_id = None, None
    try:
        lines = [x.split() for x in c2_d.strip().split('\n')]
        for line in lines:
            print(line)
        row_id = [line[-1].split('_')[5][1:] for line in lines]
        row_id = list(set(row_id))
    except:
        return
    row_id.sort()
    print("row id observed today:", len(row_id))
    print("row id observed today:", row_id)
    # print(bc_gid)
    bc_row_id = []
    for r in row_id:
        if r in bc_gid:
            bc_row_id += [r]
    print("bc row id obs. today:", len(bc_row_id))
    print("bc row id obs. today:", bc_row_id)
    if len(bc_row_id) != len(list(set(bc_row_id))):
        print("Multiple obs. for some bc gid")
    

print("LEVEL 1:")
my_list(c1_d)
print("LEVEL 2:")
my_list(c2_d)
# aws s3 cp  --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI1C/2023/03/08/S2B_MSIL1C_20230308T190239_N0509_R013_T10UFB_20230308T223026.zip S2B_MSIL1C_20230308T190239_N0509_R013_T10UFB_20230308T223026.zip
