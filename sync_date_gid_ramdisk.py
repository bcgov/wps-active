''' 20230526 download data for each 5-char "UTM tiling-grid ID":
        https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59
specified, 
for specified date: yyyymmdd only

python3 sync_date_gid.py [date: yyyymmdd] e.g.
python3 sync_date_gid.py 20230525

e.g. for NTFS001:
python3 ~/GitHub/s2-fire-mapping/sync_date_gid.py 20230530 10VEM 10VFM 

e.g. for NTSSO08:
python3 ~/GitHub/s2-fire-mapping/sync_date_gid.py 20230530 11VLG 11VLH 11VMH 11VMG

Re-run this script to regenerate the batch file that downloads and processes any frames that aren't already unpacked, spectrally subsetted and resampled in the target folder.
'''
import os
import sys
import json
import datetime
from misc import args, sep, exists, parfor
my_path = sep.join(os.path.abspath(__file__).split(sep)[:-1]) + sep

product_target = os.getcwd() + sep # run from the folder you want the products to arrive into

def download_by_gids(gids, date_string):
    now = datetime.datetime.now()  # create timestamp yyyymmddhhmmss
    [year, month, day, hour, minute, second] = [str(now.year).zfill(4),
                                                str(now.month).zfill(2),
                                                str(now.day).zfill(2),
                                                str(now.hour).zfill(2),
                                                str(now.minute).zfill(2),
                                                str(now.second).zfill(2)]
    ts = ''.join([year, month, day, hour, minute, second])

    cmd = ' '.join(['aws',  # read data from aws
                    's3api',
                    'list-objects',
                    '--no-sign-request',
                    '--bucket sentinel-products-ca-mirror'])
    # print(cmd)
    data = os.popen(cmd).read()

    if not exists(my_path + 'listing'):  # json backup for analysis
        os.mkdir(my_path + 'listing')
    df = my_path + 'listing' + sep + ts + '_objects.txt'  # file to write
    print('+w', df)
    open(df, 'wb').write(data.encode())  # record json to file

    jobs, d = [], None
    try:
        d = json.loads(data)  # parse json data
    except:
        err('please confirm aws cli is installed: e.g. sudo apt install awscli')
    data = d['Contents']  # extract the data records, one per dataset
    for d in data:
        key, modified, file_size = d['Key'].strip(), d['LastModified'], d['Size']
        w = [x.strip() for x in key.split('/')]
        if w[0] == 'Sentinel-2':
            f = w[-1]
            fw = f.split('_')
            gid = fw[5][1:]  # e.g. T10UGU
            ts = fw[2].split('T')[0]  # e.g. 20230525
            if fw[1] != 'MSIL2A' or ts != date_string:
                continue
            if gids is not None and gid not in gids:  # only level-2 for selected date and gid
                continue
            # print(d)
            # f = key.split('/')[-1]
            dest = 'L2_' + ts + sep + f
            cmd = ' '.join(['aws',
                            's3',
                            'cp',
                            '--no-sign-request',
                            's3://sentinel-products-ca-mirror/' + key,
                            f]) # dest])

            product_target_file =  product_target + f[:-3] + 'bin'
            prod_target_hdr = product_target + f[:-3] + 'hdr'
            prod_file = f[:-3] + 'bin'
            prod_hdr = f[:-3] + 'hdr'
            if not exists(product_target_file):
                jobs += [{'zip_filename': f,
                          'gid': gid,
                          'date_string': ts,
                          'download_command': cmd,
                          'prod_target': product_target_file,
                          'prod_target_hdr': prod_target_hdr,
                          'prod_file': prod_file,
                          'prod_hdr': prod_hdr}]
           
    # partition into batches
    batches = {}
    jobs_per_iter = 8
    ci, batch_i = 0, -1 
    for j in jobs:
        if ci % jobs_per_iter == 0:
            batch_i += 1        

        if batch_i not in batches:
            batches[batch_i] = []

        batches[batch_i] += [j]
        ci += 1
    
    bf = open('batch_job.sh', 'wb')
    for b in batches:
        bf.write(('# batch ' + str(b) + '\n').encode())
        bf.write('cd /ram\n'.encode())
        for j in batches[b]:
            bf.write((j['download_command'] + ' &\n').encode())
        bf.write('wait\n'.encode())
        bf.write('s2u2s\n'.encode())        
        bf.write('rm *swir*\n'.encode())
        for j in batches[b]:
            bf.write(('mv -v ' + j['prod_file'] + ' ' + j['prod_target'] + ' &\n').encode())
        for j in batches[b]:
            bf.write(('mv -v ' + j['prod_hdr'] + ' ' + j['prod_target_hdr'] + ' &\n').encode())
        bf.write('wait\n'.encode())
        bf.write('rm -rf /ram/*\n'.encode()) # clear ramdisk
        # next batch

    bf.close()
    print("+w batch_job.sh")

# get gids from command line
gids = []
if len(args) > 2:
    gids = set(args[2:])

if len(gids) == 0:  # if no gids provided, default to all gids for BC
    from gid import bc
    gids = bc()
else:
    if 'all' in gids:
        gids = None

yyyymmdd = args[1]
if len(yyyymmdd) != 8:
    print('Error: expected date in format yyyymmdd')
    sys.exit(1)
#  make it go
download_by_gids(gids, yyyymmdd)
print('done')
