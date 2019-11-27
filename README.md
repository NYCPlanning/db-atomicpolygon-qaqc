# db-atomicpolygon-qaqc
###### GRU Geocoding vs Atomic Polygon join QAQC project
This project aims to identify address points that match to different atomicids through spatial join and geocoding

## Instructions:
1. `sh 01_initialize.sh` to spin up a postgreSQL container
2. `sh 02_geocoding.sh` to spatially join address points with atomic polygons and geocode address points
3. `sh 03_export.sh` to output the table of mismatches
4. `sh 04_cleanup.sh` to clean up the postgreSQL container