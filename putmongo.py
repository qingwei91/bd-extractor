from pymongo import MongoClient
import pandas
from pathlib import Path

from os import listdir
from os.path import isfile, join

client = MongoClient('localhost', 27017)

db = client['simfin_data']

def transform_name(s):
    ns = s.replace('&', '_AND_')
    ns = ns.replace(' ', '_')
    ns = ns.replace('/', '_OR_')
    ns = ns.replace(',', '')
    ns = ns.replace('.', '')
    return ns.replace('__', '_').lower()


def remove_null_row(df):
    new_df = pandas.DataFrame()
    for idx, row in df.iterrows():
        is_null = True
        for v in row:
            is_null = not pandas.notnull(v)
        if not is_null:
            new_df = new_df.append(row)
    return new_df

def write_to_mongo(path):
    company_name = Path(path).stem

    df = pandas.read_csv(path, sep=',')
    df = df.query("Date.str.startswith('20')")

    for cl in df.columns:
        if cl != 'Date':
            df[cl] = pandas.to_numeric(df[cl])

        df = df.rename(columns={cl: transform_name(cl)})

    df['Date'] = pandas.to_datetime(df['Date'])
    df = remove_null_row(df)
    data = df.to_dict(orient='records')

    db[company_name].drop()

    if len(df) is 0:
        return 0
    else:
        collection = db[company_name]
        return collection.insert_many(data)

import sqlite3
conn = sqlite3.connect('/Users/limqingwei/projects/honey/sql/honey.db')

def write_to_sqlite(path):
    company_name = Path(path).stem

    df = pandas.read_csv(path, sep=',')
    df = df.query("Date.str.startswith('20')")

    for cl in df.columns:
        if cl != 'Date':
            df[cl] = pandas.to_numeric(df[cl])

        df = df.rename(columns={cl: transform_name(cl)})

    df['date'] = pandas.to_datetime(df['date'])
    df.insert(0, 'company', company_name)

    df = remove_null_row(df)

    if len(df) is 0:
        return 0

    df = df.set_index(['date', 'company'])
    return df.to_sql('company_fundamentals',conn, if_exists='append')

    # if len(df) is 0:
    #     return 0
    # else:
    #     collection = db[company_name]
    #     return collection.insert_many(data)

import itertools

data_dir = 'data'
all_csv_path = [f'{data_dir}/{f}' for f in listdir(data_dir) if isfile(join(data_dir, f))]

to_skip = [
    'data/ALTR.csv',
    'data/CC.csv',
    'data/CSC.csv',
    'data/PSEG.csv',
    'data/ES.csv',
    'data/MYL.csv',
    'data/COOL.csv',
    'data/EXC.csv',
    'data/SO.csv',
    'data/PNW.csv',
'data/ARMK.csv',
'data/SHO.csv',
'data/ISBC.csv',
'data/WFT.csv',
'data/FE.csv',
'data/CNC.csv',
'data/GOOG.csv',
'data/DUK.csv',
'data/BHGE.csv',
'data/ENDP.csv',
'data/FTI.csv',
'data/AGN.csv'
]

def pred(x):
    print(x)
    return x != to_skip[-1]

cont = itertools.dropwhile(pred, all_csv_path)
cont = list(cont)

for idx, path in enumerate(cont):
    if path in to_skip:
        print(f'Skipping for {idx}: {path}')
    else:
        print(f'Writing {idx} {path}')
        write_to_sqlite(path)

