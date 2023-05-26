'''The firehose: 
Save all available aws data (Level-2 from today). NB data are saved to
subfolder of "present working directory"
***e.g. cd to a folder on a large storage device'''
import os
import sys
import shutil
import datetime
args, sep = sys.argv, os.path.sep

if shutil.which('aws') is None:
    print('Error: aws cli not found. please check path variable and/or install')
    print('  sudo apt install awscli  # e.g. install for ubuntu/debian')
    sys.exit(1)

now = datetime.date.today()
[year, month, day] = [str(now.year).zfill(4),
                      str(now.month).zfill(2),
                      str(now.day).zfill(2)]

if len(args) > 1:
    t = args[1]
    if len(t) == 8:
        year, month, day = t[0:4], t[4:6], t[6:8]
today = year + month + day
print([year, month, day])


def get(c):  # get STDOUT output of command 'c'; remove extra whitespace
    print(c)
    t = [x.strip() for x in os.popen(c).read().strip().split('\n')]
    return '\n'.join(t)


cd = sep.join([year,  month,  day]) + sep
L2_F, L1_F = 'L2_' + today + sep, 'L1_' + today + sep
for d in [L1_F, L2_F]:
    if not os.path.exists(d):
        os.mkdir(d)


def run(c):
    print(c)
    return os.system(c)


run(' ' .join(['aws s3 sync',
               '--no-sign-request',
               's3://sentinel-products-ca-mirror/Sentinel-2/S2MSI1C/' + cd,
               L1_F]))

run(' '.join(['aws s3 sync',
              '--no-sign-request',
              's3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/' + cd,
              L2_F]))
