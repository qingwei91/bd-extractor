from pymongo import MongoClient
import pandas
from pathlib import Path

from os import listdir
from os.path import isfile, join

client = MongoClient('localhost', 27017)

db = client['simfin_fundamentals']

def write_to_mongo(path):
    company_name = Path(path).stem

    df = pandas.read_csv(path, sep=',')
    df = df.query("Date.str.startswith('20')")

    for cl in df.columns:
        if cl != 'Date':
            df[cl] = pandas.to_numeric(df[cl])
        if '.' in cl:
            df = df.rename(columns={cl: cl.replace('.', '')})

    df['Date'] = pandas.to_datetime(df['Date'])
    data = df.to_dict(orient='records')

    collection = db[company_name]
    return collection.insert_many(data)

data_dir = 'data'
all_csv_path = [f'data/{f}' for f in listdir(data_dir) if isfile(join(data_dir, f))]

for path in all_csv_path:
    write_to_mongo(path)
