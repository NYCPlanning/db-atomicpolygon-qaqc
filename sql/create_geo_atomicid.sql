ALTER TABLE atomicid_geocode
ADD geo_atomicid TEXT;
UPDATE atomicid_geocode
SET geo_atomicid = geo_borough_code||geo_censtract||geo_atomicpolygon
;