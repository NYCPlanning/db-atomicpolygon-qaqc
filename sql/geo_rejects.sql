DROP TABLE IF EXISTS geo_rejects;
SELECT addresspoi AS addresspoid, housenum, b7sc, atomicid,
geo_housenum, geo_streetname, geo_borough_code, geo_b10sc,
geo_censtract, geo_atomicpolygon,
geo_grc, geo_grc2, geo_reason_code, geo_message 
INTO geo_rejects
FROM atomicid_geocode
WHERE geo_atomicpolygon = '';