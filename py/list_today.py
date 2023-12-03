'''Jurisdiction specific (to be updated to be jurisdiction-flexible):
Determine the gid (grid-ID) for which Sentinel-2 data captured today are available
TODO: put the BC-specific gid info for Sentinel-2, into this repo and add gid info for other jurisdictions 

EXAMPLE OUTPUT:
python3 list_today.py 
  bc row-id under obs: ['09UXR', '10UGB', '09VVF', '10UCG', '10UDG', '11ULB', '11ULT', '09VWG', '10UFF', '11UPQ', '08VPK', '07VFG', '09VXF', '10UCE', '08VPL', '10UFV', '09UWA', '10UCF', '08UPD', '11UQQ', '10UDV', '07VFF', '09UWV', '09UUA', '08UQC', '09UVV', '11UPS', '11UMS', '10VDK', '10VCK', '11UNR', '09UYQ', '09UWT', '10UEG', '09VXG', '10UFC', '11VLD', '09VUG', '09UWB', '09UYS', '10VCL', '09VUC', '10UGD', '09UVU', '11VLF', '10UCV', '10VEL', '10VFM', '08UQD', '09UUV', '11UMT', '10UFE', '11ULS', '11ULU', '09UVS', '08UPF', '11UMU', '10VFJ', '10UDA', '09UXA', '09UXQ', '10VCH', '09UYR', '09UYP', '09VUF', '10UFG', '10UEV', '10UGV', '11VLC', '09VVD', '10UEC', '10VCM', '10VDL', '09UWR', '10UGA', '09VUD', '10UGE', '10VEK', '10UDU', '07VEG', '10UFA', '10VDH', '08VPH', '11ULA', '09UXT', '11VLE', '08VNM', '08VLL', '11UNS', '10VFL', '10UCB', '10VDM', '09VWF', '10VEH', '10VFK', '08VMM', '10UFB', '09VXC', '10UDD', '10UEE', '09VUE', '10UDB', '09VXD', '09UWU', '11VLG', '11UNQ', '11ULR', '11ULV', '08VNK', '08VPJ', '09UUU', '09UUT', '10VCJ', '09UYT', '09VXE', '10UGC', '08VNL', '09UYU', '11UMQ', '08VLM', '09UXB', '11UNT', '09VVC', '10UEB', '10UFD', '08VML', '11UPR', '10UDE', '09UVA', '10UCC', '08VPM', '09UXS', '10VEM', '10VEJ', '10UCD', '10UED', '09VWE', '09VWC', '09VWD', '09UXU', '09UVB', '09UWS', '10UDC', '09UVT', '09UXV', '09VVG', '10UDF', '08UQE', '09VVE', '10UEA', '09UYV', '10UCA', '10VFH', '10UCU', '11ULQ', '10VDJ', '08UPE', '10UEF', '11UMR']
  ['2023', '12', '03']
  aws s3 ls --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI1C/2023/12/03/
  aws s3 ls --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/2023/12/03/
  LEVEL 1:
  row id observed today: 110
  bc row id obs. today: 0
  bc row id obs. today: []
  LEVEL 2:
  row id observed today: 1
  bc row id obs. today: 0
  bc row id obs. today: []
'''
import os
import sys
import datetime
from gid import bc
sep = os.path.sep 

bc_gid = bc()
print("bc row-id under obs:", bc_gid)

if len(os.popen("aws 2>&1").read().split("not found")) > 1:
    print('Need to install aws cli:')
    print('  sudo apt install awscli')
    sys.exit(1)

now = datetime.date.today()
year, month, day = str(now.year).zfill(4), str(now.month).zfill(2), str(now.day).zfill(2)

print([year, month, day])
ls = 'aws s3 ls --no-sign-request'
path = 's3://sentinel-products-ca-mirror/Sentinel-2/'
c1, c2 = ' '.join([ls, path + 'S2MSI1C/']), ' '.join([ls, path + 'S2MSI2A/'])
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
            pass # print(line)
        row_id = [line[-1].split('_')[5][1:] for line in lines]
        row_id = list(set(row_id))
    except:
        return
    row_id.sort()
    print("row id observed today:", len(row_id))
    # print("row id observed today:", row_id)
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
