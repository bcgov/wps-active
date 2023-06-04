'''20230603 query CIFFC active fire locations
'''
from urllib.request import urlopen
from misc import time_stamp
import sys
import json

url = 'https://cwfis.cfs.nrcan.gc.ca/geoserver/public/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=public:activefires_current&outputFormat=json'
response = urlopen(url)
data_json = json.loads(response.read())

jfn = ts + '_CWIFS_fires.json'
open(jfn, 'wb').write(data_json.encode())
print('+w', jfn)

# print(data_json)

select_agency = None
if len(sys.argv) > 1:
    select_agency = sys.argv[1]

agency = {}
for f in data_json['features']:
    # print(f.keys()) # dict_keys(['type', 'id', 'geometry', 'geometry_name', 'properties'])
    properties = f['properties']
    ag = properties['agency']
    if ag not in agency:
        agency[ag] = 0
    agency[ag] += 1
    if ag == select_agency or select_agency is None:
        print(properties)

print(agency)
