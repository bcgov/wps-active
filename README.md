# Sentinel-2 NRT active fire mapping
Huge thanks to [Natural Resources Canada (NRCAN)](https://natural-resources.canada.ca/) for providing open access to their AWS mirror of ESA's Sentinel-2 satellite products. This AWS mirror contributed to ~13% of all of BC Wildfire Service's (BCWS) public-facing perimeter data in 2023! Currently, the preferred method for active fire mapping in BC is an Alberta-based airborne mission, which costs approximately $30K (CAD) per day to fly. Using NRCAN's mirror of Sentinel-2 satellite data, we were able to build critical fire maps for the unprecedented 2023 fire season, especially during critical periods when the usual airborne resources weren't available as they were already allocated. 

With the `wps-active` repo, users can download the contents of NRCAN's mirror of ESA Sentinel-2 data products stored in an Amazon Web Service (AWS) S3 bucket. That said, running the commands listed below will require the installation of the AWS command line interface (CLI), which can be found [here](https://github.com/bcgov/wps-research/blob/master/HOWTO.md) if you haven't already installed it. 

To check whether the AWS CLI has been installed, simply type in `aws` then hit "enter" in your command line and you should see the following results:

```
  aws help
  aws <command> help
  aws <command> <subcommand> help
```
## Dependencies
[Anaconda](https://www.anaconda.com/download) is recommended for managing all dependencies. Within Anaconda Prompt, [pip](https://pip.pypa.io/en/stable/installation/) will be available to install the dependencies that may be needed for this repo.

However, one library may that might cause issues is [GDAL](https://gdal.org/) as it may not come pre-installed with Anaconda Prompt and needs to be downloaded manually. If this is the case, there is a [UCLA blog tutorial](https://sandbox.oarc.ucla.edu/tutorials/installing-gdal-for-windows), along with a [video tutorial](https://youtu.be/gkdNvwmoV_E?si=twl8mSOC1yUC5ACz), that walks through how to install GDAL on Windows through the use of [wheel files (whl)](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal). Do note that it's important to download the wheel file tag that's [compatible with your system](https://stackoverflow.com/a/67970307). Run the `pip debug --verbose` command to get a list of compatible tags and match them with one of the GDAL wheel files available for download.

## Functions

Below are some examples of functions we've developed to access specific data within NRCAN's S3 bucket:

To access all the satellite data for a given date (e.g. June 3rd, 2023), run the following command:

```
python3 sync_date_gid_ramdisk.py 20230603 all 
```

To pull the most recent data for a list of [grid-IDs](https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59), which are specific persistent footprints based on UTM coordinate system, enter the command below:
```
python3 sync_latest_gid.py [gid #1] [gid #2] .. [gid #N]
```

To download the latest data for BC, use the following command:
```
python3 py/sync_latest_gid.py
```

To download data for a specific date (e.g. May 25th, 2023) and a specific jurisdiction grid-id, run the command below:
```
python3 py/sync_date_gid.py 20230525 
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
