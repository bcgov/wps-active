'''
20241210 sync_daterange_aoi_zip.py: download sentinel-2 data zipfiles, from NRCAN AWS mirror, within daterange ( yyyymmdd ) over specified aoi ( within Canada )

NOTE: linux or linux via WSL ( windows subsystem / Linux ) assumed 

20241210: sync sentinel-2 data in a date range, all tiles which intersect the given AOI provided in shapefile format.
20230627: sync a date range for selected GID, in Level-2 to zip file format.
20230627: sync a date range for selected GID'''

use_L2 = True
data_type = 'MSIL2A'
if not use_L2:
    data_type = 'MSIL1C'

from misc import args, sep, exists, parfor, run, timestamp, err
import multiprocessing as mp
import geopandas as gpd
import datetime
import time
import json
import sys
import os

import warnings
import urllib3
warnings.filterwarnings("ignore", message="Unable to import Axes3D")  # suppress axes3d warning
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)  # suppress insecure request warning

my_path = sep.join(os.path.abspath(__file__).split(sep)[:-1]) + sep
product_target = os.getcwd() + sep # put ARD products into present folder

'''check that s2_gid is extracted for Canada'''
s2_tar = os.path.normpath(os.path.abspath(my_path)) + sep + 's2_gid.tar.gz'
s2_shp = os.path.normpath(os.path.abspath(my_path)) + sep # + 's2_gid' + sep 

print(s2_tar)
print(s2_shp)
if not exists(s2_shp + sep + 's2_gid'):
    import tarfile
    print("tar xvf s2_gid.tar.gz")
    with tarfile.open(s2_tar, "r:gz") as tar:
        tar.extractall(path = s2_shp)
else:
    print("+r s2_gid.tar.gz")


def download_by_gids(gids, date_range):
    global data_type
    global use_L2

    ts = timestamp()
    cmd = ' '.join(['aws',  # read data from aws
                    's3api',
                    'list-objects',
                    '--no-verify-ssl',
                    '--no-sign-request',
                    '--bucket sentinel-products-ca-mirror'])
    print(cmd)
    data = os.popen(cmd).read()

    if not exists(my_path + 'listing'):  # json backup for analysis
        os.mkdir(my_path + 'listing')
    df = my_path + 'listing' + sep + ts + '_objects.txt'  # file to write
    open(df, 'wb').write(data.encode())  # record json to file

    jobs, d = [], None
    try:
        d = json.loads(data)  # parse json data
    except:
        err('please confirm aws cli: e.g. sudo apt install awscli')
    data = d['Contents']  # extract the data records, one per dataset
    
    cmds = []
    for d in data:
        key, modified, file_size = d['Key'].strip(), d['LastModified'], d['Size']
        w = [x.strip() for x in key.split('/')]
        if w[0] == 'Sentinel-2':
            f = w[-1]
            fw = f.split('_')
            gid = fw[5][1:]  # e.g. T10UGU
            ts = fw[2].split('T')[0]  # e.g. 20230525
            if fw[1] != data_type or ts not in date_range:  # wrong product or outside date range
                continue
            if gids is not None and gid not in gids:  # only level-2 for selected date and gid
                continue

            cmd = ' '.join(['aws',
                            's3',
                            'cp',
                            '--no-verify-ssl',
                            '--no-sign-request',
                            's3://sentinel-products-ca-mirror/' + key,
                            f])
            if exists(f):
                print(f, "SKIPPING")
            else:
                print(f)
                cmds += [cmd]
    
    print(cmds)
    def runc(c):
        print([c])
        return os.system(c)
    parfor(runc, cmds, int(mp.cpu_count()))  

gids = []

if len(args) < 4:
    err("sync_daterange_aoi_zip.tar.gz [yyyymmdd] [yyyymmdd] [aoi shapefile] [--use_L1 or --use_L2]")

if not (('--use_L1' in args) or ('--use_L2' in args)):
    err('please specify whether to retrieve L1 or L2 data using the --use_L1 or --use_L2 flag')

if '--use_L1' in args:
    use_L2 = False

if '--use_L2' in args:
    use_L2 = True

if '--use_L1' in args and '--use_L2' in args:
    err('please select L1 or L2 only')

if not use_L2:
    data_type = 'MSIL1C'

aoi_shp = args[3]

if not exists(aoi_shp):
    err('input AOI shapefile not found: ' + str(aoi_shp))

# intersect the aoi with the Sentinel-2 grid shapefile ( to determine applicable tiles )
gdf_aoi = gpd.read_file(aoi_shp)
gdf_s2 = gpd.read_file(s2_shp + 's2_gid' + sep + 's2_gid.shp')
gdf_aoi = gdf_aoi.to_crs(gdf_s2.crs)  # interpret the two shapefiles on the same coordinate system
intersect = gpd.sjoin(gdf_s2, gdf_aoi, how='inner', predicate="intersects")
# print(intersect)
# print(type(intersect))

gids = intersect['Name'].to_list()
print('Selected Sentinel-2 tile/grid ID: ' + str(gids))

yyyymmdd, yyyymmdd2 = args[1], args[2]
if len(yyyymmdd) != 8 or len(yyyymmdd2) != 8:
    err('expected date in format yyyymmdd')

start_d = datetime.datetime(int(yyyymmdd[0:4]),
                            int(yyyymmdd[4:6]),
                            int(yyyymmdd[6:8]))

end_d = datetime.datetime(int(yyyymmdd2[0:4]),
                            int(yyyymmdd2[4:6]),
                            int(yyyymmdd2[6:8]))

print("start", start_d, "end", end_d)

date_range = []
while start_d <= end_d:
    print(start_d)
    start_d += datetime.timedelta(days=1)
    date_range += [str(start_d.year).zfill(4) + str(start_d.month).zfill(2) + str(start_d.day).zfill(2)]
print(date_range)
   
download_by_gids(gids, date_range)
print('done')
