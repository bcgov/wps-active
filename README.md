# Sentinel-2 NRT active fire mapping
Huge thanks to NRCAN for access to their AWS mirror of Sentinel-2 products! According to a colleage, this source contributed to 13% of all public facing BCWS perimeter data in 2023. The dominant/preferred method for active fire mapping in BC is Alberta-based airborne mission costing approx 30K CAD / day to fly. The NRCAN AWS mirror was used heavily for Sentinel-2 (satellite) based fire mapping in the unprecedented 2023 season, especially during a critical period when the airborne source was not available. 

Currently this repo only reflects data download 
```
# sync and process all mirrored images for one date e.g. Jun 3rd, 2023
python3 sync_date_gid_ramdisk.py 20230603 all 
```
## Functions
### For specific grid-id, pull most recent data only
```
python3 sync_latest_gid.py [gid #1] [gid #2] .. [gid #N]
```
to download only the most-recent data for a list of ["grid id"](https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59) (i.e. specific persistent footprints based on UTM coordinate system)

Currently this downloads the latest data for BC:
```
python3 py/sync_latest_gid.py
```

### For jurisdiction-specific grid-id, pull data for specific date only
```
python3 py/sync_date_gid.py 20230525 # example: pull data over bc for May 25, 2023
```

## Deprecated
### The firehose: Pull all of today's captures
```
python3 py/sync_today_all.py # [yyyymmdd]: optional arg: sync all data from yyyymmdd
```
# Notes
Information in this repo reflects collaboration with the following teams:
* NRCan/WildFireSat
* NRCan/EGS
* NRCan/GSDI
* BC Public Service
* BC Wildfire/Predictive Services Unit 

### To be added
Features to be added:
* Filter for BC and/or other prov/territory since coverage expanded beyond BC (DONE 20230526)
* CIFFC-database search and intersection operation to determine incident-specific gid (grid-ID) i.e. download incident specific data for any Canadian jurisdiction
* GDAL-based unpacking / resampling
* 2022 active fire detection rule
* 2023 hotspot detection rule
* ML-based extension based on library of operational, human-refined reference data
