from pymongo import MongoClient
import pandas

client = MongoClient('localhost', 27017)
db = client['simfin_data']

def get_from_mongo(db, ticker):
    collection = db[ticker]
    all_docs = collection.find()
    return pandas.DataFrame(list(all_docs))

aapl_df = get_from_mongo(db, 'AAPL')
roe_col = 'Return_on_Equity'
date_col = 'Date'

# filter rows with non null roe values
non_empty = aapl_df.loc[aapl_df[roe_col].notnull()]

# need to set date as index for plotting
date_indexed_data = non_empty.set_index(date_col)

date_indexed_data[roe_col].plot()

