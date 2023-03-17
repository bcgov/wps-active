import os
import json
import datetime

now = datetime.datetime.now()
[year, month, day, hour, minute, second] = [str(now.year).zfill(4),
                                            str(now.month).zfill(2),
                                            str(now.day).zfill(2),
                                            str(now.hour).zfill(2),
                                            str(now.minute).zfill(2),
                                            str(now.second).zfill(2)]

ts = ''.join([year, month, day, hour, minute, second])

data = os.popen('aws s3api list-objects --no-sign-request --bucket sentinel-products-ca-mirror').read()

df = ts + '_objects.txt'  # file to write
print('+w', df)
open(df, 'wb').write(data.encode())  # write json data to file

d = json.loads(data)
print(d)
