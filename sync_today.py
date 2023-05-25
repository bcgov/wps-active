'''save all available aws data (Level-2 from today) NB data are saved to subfolder of "present working directory"

***e.g. Run this from active/ folder where active detection stuff lives***
'''
import os
import sys
import datetime
args = sys.argv

if len(os.popen("aws 2>&1").read().split("not found")) > 1:  # check for aws cli
    print('Error: aws cli not found. To install on debian/ubuntu:\n  sudo apt install awscli')
    sys.exit(1)

now = datetime.date.today()
year, month, day = str(now.year).zfill(4), str(now.month).zfill(2), str(now.day).zfill(2)

if len(args) > 1:
	t = args[1]
	if len(t) == 8:
		year = t[0:4]
		month = t[4:6]
		day = t[6:8]
today = year + month + day
print([year, month, day])

def get(c):
    print(c)
    t = [x.strip() for x in os.popen(c).read().strip().split('\n')]
    return '\n'.join(t)

cd = '/'.join([year, 
			   month,
			   day]) + '/'

L2_F = 'L2_' + today + '/'
L1_F = 'L1_' + today + '/'
for d in [L1_F, L2_F]:
	if not os.path.exists(d):
		os.mkdir(d)

cmd = 'aws s3 sync --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI1C/' + cd + ' ' + L1_F
a = os.system(cmd)

cmd = 'aws s3 sync --no-sign-request s3://sentinel-products-ca-mirror/Sentinel-2/S2MSI2A/' + cd + ' ' + L2_F
a = os.system(cmd)



