from pathlib import Path
from os import listdir
from os.path import isfile, join

import pandas

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

import sqlite3
conn = sqlite3.connect('/Users/limqingwei/projects/honey/sql/honey.db')

def fix_col(df):
    # faulty_col = [c for c in df.columns if '.1' in c]
    ok_col = [c for c in df.columns if '.1' not in c]

    new_df = pandas.DataFrame()

    new_df.loc[:, 'Date'] = df['Date']

    for c in ok_col:
        if c != 'Date':
            corresponding = f'{c}.1'
            combined = df[c].combine_first(df[corresponding])
            new_df.loc[:, c] = combined

    return new_df

def write_to_sqlite(df, company_name):
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

def read_file(path):
    df = pandas.read_csv(path, sep=',')
    return df

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

for p in to_skip:
    df = read_file(p)
    company_name = Path(p).stem
    fixed = fix_col(df)
    write_to_sqlite(fixed, company_name)