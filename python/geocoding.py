from multiprocessing import Pool, cpu_count
from sqlalchemy import create_engine
from geosupport import Geosupport, GeosupportError
from pathlib import Path
import pandas as pd
import usaddress
import json
import re
import os 

g = Geosupport()

def get_sname(b7sc): 
    try:
        geo = g['D'](B7SC=b7sc)
        return geo.get('First Street Name Normalized', '')
    except: 
        return ''

def get_boro(x):
    x = ' ' if x is None else x
    return x[0]

def get_boro_code(x):
    if x != '':
        x = x[0]
    return x
    
def geocode(inputs):
    hnum = inputs.get('housenum', '')
    b7sc = inputs.get('b7sc', '')
    sname = get_sname(b7sc)
    borough = get_boro(b7sc)

    hnum = str('' if hnum is None else hnum)
    sname = str('' if sname is None else sname)
    borough = str('' if borough is None else borough)
    try:
        geo = g['1E'](house_number=hnum, street_name=sname, borough=borough)
    except GeosupportError as e:
        geo = e.result

    geo = geo_parser(geo)
    geo.update(inputs)
    return geo

def geo_parser(geo):
    return dict(
        geo_atomicpolygon = geo.get('Atomic Polygon', ''),
        geo_housenum = geo.get('House Number - Display Format', ''),
        geo_streetname = geo.get('First Street Name Normalized', ''),
        geo_b10sc = geo.get('B10SC - First Borough and Street Code', ''),
        geo_censtract = geo.get('2010 Census Tract', ''),
    )

if __name__ == '__main__':
    # connect to postgres db
    recipe_engine = create_engine(os.environ['RECIPE_ENGINE'])
    engine = create_engine(os.environ['BUILD_ENGINE'])

    import_sql = f'''
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

                    SELECT * FROM geocodesubset;
    '''

    # read in housing table
    # df = pd.read_sql("SELECT * FROM geo_inputs;", engine)
    print('dataloading begins here ...')
    df = pd.read_sql(import_sql, recipe_engine)

    records = df.to_dict('records')
    
    print('dataloading finished, start geocoding ...')
    # Multiprocess
    with Pool(processes=cpu_count()) as pool:
        it = pool.map(geocode, records, 10000)
    
    print('geocoding finished, dumping tp postgres ...')

    df = pd.DataFrame(it)
    df['geo_borough_code'] = df['geo_b10sc'].apply(lambda x: get_boro_code(x))

    df.to_sql('atomicid_geocode', engine, if_exists='replace', chunksize=10000)