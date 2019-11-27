DB_CONTAINER_NAME=atom

docker exec $DB_CONTAINER_NAME psql -h localhost -U postgres -c "\copy (SELECT * FROM atomicid_geocode) 
                                TO '/home/db-atomicpolygon-qaqc/output/atomicid_geocode.csv' 
                                DELIMITER ',' CSV HEADER;"

docker exec $DB_CONTAINER_NAME psql -h localhost -U postgres -c "\copy (SELECT * FROM atomicid_mismatch) 
                                TO '/home/db-atomicpolygon-qaqc/output/atomicid_mismatch.csv' 
                                DELIMITER ',' CSV HEADER;" 