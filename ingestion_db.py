import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename='logs/data_ingestion.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode="a"
)

engine = create_engine('sqlite:///vendor_data.db')

def ingest_db(df, table_name, engine):
    '''ingest df into db'''
    df.to_sql(table_name, con=engine, if_exists = 'replace', index = False)

def load_raw_data():
    '''load CSV as df and ingest into db'''
    start = time.time()
    for file in os.listdir('data'):
        if '.csv' in file:
            df = pd.read_csv('data/'+file)
            logging.info(f'Ingesting {file} in db')
            ingest_db(df, file[:-4], engine)
    end = time.time()        
    total_time = (end - start)/60
    logging.info('Ingestion of Data Completed')
    logging.info(f'Total time taken to ingest data is {total_time} minutes')

if __name__ == '__main__':
    load_raw_data()    
