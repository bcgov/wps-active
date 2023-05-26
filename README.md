# Sentinel-2 active fire mapping
Currently this repo only reflects data download 

## Functions
### For specific grid-id, pull most recent data only
```
python3 sync_latest_gid.py [gid #1] [gid #2] .. [gid #N]
```
to download only the most-recent data for a list of ["grid id"](https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59) (i.e. specific persistent footprints based on UTM coordinate system)

### For jurisdiction-specific grid-id, pull data for specific date only
```
sync_date_gid.py 20230525 # example: pull data over bc for May 25, 2023
```

## Deprecated
### The firehose: Pull all of today's captures
```
python3 sync_today_all.py # [yyyymmdd]: optional arg: sync all data from yyyymmdd
```
# Notes
Information in this repo restricted to the following teams:
* NRCan/WildFireSat
* NRCan/EGS
* NRCan/GSDI
* BC Wildfire/Predictive Services Unit 

### To be added
Features to be added:
* Filter for BC and/or other prov/territoriy since coverage expanded beyond BC (DONE 20230526)
* * CIFFC-database search and intersection operation to determine incident-specific gid (grid-ID) i.e. download incident specific data for any Canadian jurisdiction
* GDAL-based unpacking / resampling
* 2022 active fire detection rule
* 2023 hotspot detection rule
* ML-based extension based on library of operational, human-refined reference data
