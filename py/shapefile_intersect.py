'''20230604 CWFIS version. Use to intersect shapefile of point locations, with tile-index file produced by 
20230530 intersect one shapefile with another. NB probably need to adjust which field is reported on.

adapted from:  bcws_select_tiles
20230520 project fire locations onto Sentinel-2 tiles
Use this to update :
.tiles_select used by safe_unzip_select.py


Note: if shapefiles are not the same CRS, use shapefile_enforce_CRS.py
'''
from misc import run, err, args, exists, sep
from osgeo import ogr
import sys
import os

rd = 'reproject'
if not exists(rd):
    os.mkdir(rd)

shapefile_1 = 'CWFIS_EPSG3347.shp'
shapefile_2 = 's2_gid/s2_gid_EPSG3347.shp'
print(args)

if len(args) < 3:
    err("shapefile_intersect.py [first shapefile] [second shapefile: S2 grid]")
else:
    shapefile_1, shapefile_2 = args[1], args[2]

# shapefile_reproject.py [input shapefile] [shapefile or raster to get CRS from] [output shapefile]

def print_feature(feature):
    num_fields = feature.GetFieldCount()
    
    # Loop through all attribute fields
    for i in range(num_fields):
        field_name = feature.GetFieldDefnRef(i).GetName()
        field_value = feature.GetField(i)
        print(f"{field_name}: {field_value}")

# intersect one shapefile with another
my_tiles, my_lat, my_lon = {}, {}, {}
def shapefile_intersect(s1_path, s2_path):
    # Open the first shapefile
    print('r', s1_path)
    s1_driver = ogr.GetDriverByName('ESRI Shapefile')
    s1_dataSource = s1_driver.Open(s1_path, 0)
    if s1_dataSource is None:
        err('opening:' + s1_path)

    s1_layer = s1_dataSource.GetLayer()
    s1_crs = s1_layer.GetSpatialRef()   
    
    # Open the second shapefile
    print('r', s2_path)
    s2_driver = ogr.GetDriverByName('ESRI Shapefile')
    s2_dataSource = s2_driver.Open(s2_path, 0)
    if s2_dataSource is None:
        err('opening:' + s2_path)
    
    s2_layer = s2_dataSource.GetLayer()
    s2_crs = s2_layer.GetSpatialRef()

    if s1_crs.ExportToWkt() == s2_crs.ExportToWkt():
        print("The CRS of the two shapefiles is the same.")
    else:
        print("The CRS of the two shapefiles is different.")
        print(s1_path, s1_crs.ExportToWkt())
        print(s2_path, s2_crs.ExportToWkt())
        sys.exit(1)

    # Loop through features in the first shapefile
    for feature1 in s1_layer:
        # print_feature(feature1) # print(feature1)
        geometry1 = feature1.GetGeometryRef()
        # Loop through features in the second shapefile 
        for feature2 in s2_layer:
            geometry2 = feature2.GetGeometryRef()
            # Check if the two geometries intersect
            # print_feature(feature2)
            if geometry1.Intersects(geometry2):
                # print("Features intersect!")
                # print("feature1", feature1)
                print_feature(feature1)
                # print(dir(feature1))
                my_fire = None
                try:
                    my_fire = feature1.GetField("firename")
                except:
                    my_fields = [feature1.GetFieldDefnRef(i).GetName() for i in range(feature1.GetFieldCount())]
                    # print("my_fields", my_fields)
                    my_fire = feature1.GetField(my_fields[0])
                    pass
                my_tile = feature2.GetField("Name")
                if my_fire not in my_tiles:
                    my_tiles[my_fire] = set()
                my_tiles[my_fire].add(my_tile)
                
                try:
                    my_lat[my_fire] = feature1.GetField("lat")
                except:
                    pass

                try:
                    my_lon[my_fire] = feature1.GetField("lon")
                except:
                    pass
                print(my_fire, my_tile)
                # print("-------------------")
                #print_feature(feature2)
                #print(geometry1)
                #print(geometry2)
    # Clean up and close the shapefile data sources
    s1_dataSource = None
    s2_dataSource = None

shapefile_intersect(shapefile_1, #'CWFIS_EPSG3347.shp', #'CWFIS.shp',
                    shapefile_2) #'s2_gid/s2_gid_EPSG3347.shp') #'s2_gid/s2_gid.shp')

for fire in my_tiles:
    lat = str(my_lat[fire] if fire in my_lat else None)
    lon = str(my_lon[fire] if fire in my_lon else None)
    s_hub = 'https://apps.sentinel-hub.com/sentinel-playground/?source=S2L2A&lat=' + \
                lat + '&lng=' + \
                lon +\
                '&zoom=12&preset=CUSTOM&layers=B12,B11,B09&maxcc=100&gain=1.0&gamma=1.0&atmFilter=&showDates=false&evalscript=cmV0dXJuIFtCMTIqMi41LEIxMSoyLjUsQjA5KjIuNV0%3D'
    print(fire, my_tiles[fire], lat, lon, s_hub)
    print(' '.join(my_tiles[fire]))



'''

s1 = 'prot_current_fire_points.shp'
shapefile_intersect(s1, s2)


if not exists('.select'):
    os.mkdir('.select')

tiles_select = set()
for fire in my_tiles:
    this_fire = []

    print(fire, my_tiles[fire])
    for tile in my_tiles[fire]:
        tiles_select.add(tile)
        this_fire += [tile]
    
    open('.select/' + fire, 'wb').write((' '.join(this_fire)).encode())
    bs = '/media/' + os.popen('whoami').read().strip() + '/disk4/active/'
    if os.path.exists(bs):
        tf = bs + fire
        if not os.path.exists(tf):
            try:
                os.mkdir(tf)
            except:
                print("Warning: mkdir failed:", tf) 
        tf +=  '/.tiles'
        print('+w', tf)
        open(bs + fire + '/.tiles', 'wb').write((' '.join(this_fire)).encode())

tiles_select = list(tiles_select)
print(tiles_select)

open('.tiles_select', 'wb').write((' '.join(['T' + t for t in tiles_select])).encode())
'''
