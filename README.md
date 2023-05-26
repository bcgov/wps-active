# Sentinel-2 active fire mapping
Currently this repo only reflects data download e.g. 
* download *all of Sentinel-2 data captured today that are available in the bucket*  

# Functions 

### For specific grid-id, pull most recent data only
```
python3 sync_latest_gid.py [gid #1] [gid #2] .. [gid #N]
```
to download only the most-recent data for a list of ["grid id"](https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59) (i.e. specific persistent footprints based on UTM coordinate system)

### The firehose (deprecated): Pull all of today's captures
```
python3 sync_today_all.py
```
or
```
python3 sync_today_all.py yyyymmdd # sync all data from yyyymmdd
```
# Notes
Information in this repo restricted to the following teams:
* NRCan/WildFireSat
* NRCan/EGS
* NRCan/GSDI
* BC Wildfire/Predictive Services Unit 

### To be added
Features to be added:
* Filter for BC and/or other prov/territoriy since coverage expanded beyond BC
* GDAL-based unpacking / resampling
* CIFFC-database search and intersection operation to determine incident-specific gid (grid-ID) i.e. download incident specific data for any Canadian jurisdiction
* 2022 active fire detection rule
* 2023 hotspot detection rule
* ML-based extension based on library of operational, human-refined reference data
