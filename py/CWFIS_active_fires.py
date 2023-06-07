'''20230603 query CIFFC active fire locations

NB need to clip Sentinel-2 footprint for Canada'''
from urllib.request import urlopen
from misc import time_stamp, run
import shutil
import json
import sys

data_json = None  # read json data
try:  
    url = 'https://cwfis.cfs.nrcan.gc.ca/geoserver/public/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=public:activefires_current&outputFormat=json'
    response = urlopen(url)
    data_json = response.read()

    # save to file
    ts = time_stamp()
    jfn = ts + '_CWFIS_fires.json'
    open(jfn, 'wb').write(data_json)
    print('+w', jfn)

    # convert to shapefile
    shutil.copyfile(jfn, 'CWFIS_fires.json')
    run('ogr2ogr -skipfailures -f "ESRI Shapefile" CWFIS.shp CWFIS_fires.json')
except:
    data_json = open('CWFIS_fires.json').read()

# parse json data
data_json = json.loads(data_json)
# print(data_json)

select_agency = None
if len(sys.argv) > 1:
    select_agency = sys.argv[1]

agency = {}
for f in data_json['features']:
    print(f.keys()) # dict_keys(['type', 'id', 'geometry', 'geometry_name', 'properties'])
    properties = f['properties']
    ag = properties['agency']
    if ag not in agency:
        agency[ag] = 0
    agency[ag] += 1
    if ag == select_agency or select_agency is None:
        print(properties)

print(agency)
