WITH hasatomicidjoin AS (
	SELECT a.*, b.atomicid 
	FROM dcp_addresspoints.latest a, 
		dcp_atomicpolygons.latest b
	WHERE ST_Within(a.wkb_geometry,b.wkb_geometry)),
geocodesubset as(
SELECT DISTINCT addresspoi,
	CONCAT(house_numb,'',house_nu_1) as housenum,
	CASE 
		WHEN special_co = 'V' THEN b7sc_vanit
		ElSE  b7sc_actua
	END as b7sc,
	atomicid
FROM hasatomicidjoin
WHERE house_numb IS NOT NULL OR house_nu_1 IS NOT NULL
UNION
SELECT DISTINCT addresspoi,
	CONCAT(house_nu_2,'',house_nu_3) as housenum,
	CASE 
		WHEN special_co = 'V' THEN b7sc_vanit
		ElSE  b7sc_actua
	END as b7sc, 
	atomicid
FROM hasatomicidjoin
WHERE house_nu_2 IS NOT NULL OR house_nu_3 IS NOT NULL)

SELECT COUNT(*) FROM geocodesubset;