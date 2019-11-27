from cook import Importer
import os
from sqlalchemy import create_engine

def ETL():
    RECIPE_ENGINE = os.environ.get('RECIPE_ENGINE', '')
    BUILD_ENGINE=os.environ.get('BUILD_ENGINE', '')

    importer = Importer(RECIPE_ENGINE, BUILD_ENGINE)

    importer.import_table(schema_name='dcp_addresspoints')
    importer.import_table(schema_name='dcp_atomicpolygons')

if __name__ == "__main__":
    ETL()