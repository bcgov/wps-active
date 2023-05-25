# Sentinel-2 active fire mapping
Currently this repo only reflects data download e.g. 
* download *all of Sentinel-2 data captured today that are available in the bucket*  

# Functions 
### Pull all data captured today
Currently using:
```
python3 sync_today.py
```
Will update this to:
* ignore L1, since Will will be turning that off.
* filter for BC and other prov/territory since the coverage is expanded beyond BC

### Pull only most-recent data for specific grid-id
```
python3 download_gid_latest.py [gid #1] [gid #2] .. [gid #N]
```
to download only the most-recent data for a list of ["grid id"](https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59) (i.e. specific persistent footprints based on UTM coordinate system)

# Notes
Information in this repo restricted to the following teams:
* NRCan/WildFireSat
* NRcan/EGS
* NRCan/GSDI
* BC Wildfire/Predictive Services Unit 

Tech notes:
* NB tested in posix environment. May contain '/' that need be replaced with os.path.sep to be Windows compatible.
### To be added
Features to be added:
* GDAL-based unpacking / resampling
* CIFFC-database search and intersection operation to determine incident-specific gid (grid-ID) i.e. download incident specific data for any Canadian jurisdiction
* 2022 active fire detection rule
* 2023 hotspot detection rule
* ML-based extension based on library of operational, human-refined reference data
