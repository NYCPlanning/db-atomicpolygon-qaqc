DROP TABLE IF EXISTS atomicid_mismatch;
SELECT addresspoi AS addresspoid, housenum, geo_housenum, geo_streetname,
atomicid, geo_atomicid
INTO atomicid_mismatch
FROM atomicid_geocode
WHERE atomicid != geo_atomicid; 