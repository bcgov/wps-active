'''20230603 query CIFFC active fire locations
NB need to clip Sentinel-2 footprint for Canada'''
from urllib.request import urlopen
from misc import time_stamp, run
import argparse
import shutil
import json
import sys
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--skip_download", action="store_true",
                    help="skip downloading CWFIS data and use existing local copy")
parser.add_argument("agency", nargs='?', type=str, default=None,
                    help="CIFFC agency code in lower case e.g. on, qc, ab, etc")
args = parser.parse_args()
select_agency = args.agency
try_download = not args.skip_download

data_json = None  # read json data
if try_download:
    try:  
        url = 'https://cwfis.cfs.nrcan.gc.ca/geoserver/public/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=public:activefires_current&outputFormat=json'
        response = urlopen(url)
        data_json = response.read()

        ts = time_stamp()  # local data archive
        jfn = ts + '_CWFIS_fires.json'
        open(jfn, 'wb').write(data_json)
        print('+w', jfn)

        shutil.copyfile(jfn, 'CWFIS_fires.json')  # copy and convert to shapefile
        run('ogr2ogr -skipfailures -f "ESRI Shapefile" CWFIS.shp CWFIS_fires.json')
    except:
        print("download time out, defaulting to local copy")
        data_json = open('CWFIS_fires.json').read()
else:
    data_json = open('CWFIS_fires.json').read()

data_json = json.loads(data_json)  # parse json data
agency = {}
for f in data_json['features']:
    print(f.keys()) # dict_keys(['type', 'id', 'geometry', 'geometry_name', 'properties'])
    properties = f['properties']
    ag = properties['agency']
    if ag not in agency:
        agency[ag] = 0
    agency[ag] += 1
    if ag == select_agency or select_agency is None:
        s_hub = 'https://apps.sentinel-hub.com/sentinel-playground/?source=S2L2A&lat=' + str(properties['lat']) + '&lng=' + str(properties['lon']) + \
                    '&zoom=12&preset=CUSTOM&layers=B12,B11,B09&maxcc=20&gain=1.0&gamma=1.0&atmFilter=&showDates=false&evalscript=cmV0dXJuIFtCMTIqMi41LEIxMSoyLjUsQjA5KjIuNV0%3D'
        print(properties, s_hub)
print(agency)
