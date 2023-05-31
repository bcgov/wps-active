### By Dan Thompson
### Simple GeoServer call to the WFS active fire layer
library(sf)
library(httr2)
library(geojsonsf)

### See https://cwfis.cfs.nrcan.gc.ca/interactive-map for browser version of same layer

### WFS active fires request for  all of Canada as json
urlActiveFires=paste0("http://cwfis.cfs.nrcan.gc.ca/geoserver/public/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=public:activefires_current&outputFormat=json")

#convert json to sf
fires_current_json = request(urlActiveFires) |> req_perform() |> resp_body_string()
  fires_current_sf = geojson_sf(fires_current_json)
    
    ## custom filters of sf dataframe using dplyr
  fires_current <- fires_current_sf %>% ### preserve as sf
  filter(hectares>1000) %>% ##filter only fires >1,000 hectares
  filter(stage_of_control == "OC")
  
  ### see glossary at https://ciffc.ca/ for definition of stage_of_control levels
  
  
  ## can use st_drop_geometry() to strip locations (EPSG:3978) if you want
  ##lat/long is embedded in the data table in EPSG:4326  otherwise
