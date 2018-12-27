import pandas

file_name = 'output-semicolon-wide.csv'
# file_name = 'sample-data.csv'
file_name = '1comp.csv'

df = pandas.read_csv(file_name, sep=';', header=[2, 5])
all_levels = df.columns.levels
all_companies = all_levels[0].drop('ticker')

level_0 = all_levels[0]
level_1 = all_levels[1]

renamed_0 = ['Date' if x == 'ticker' else x for x in level_0]
renamed_1 = ['Date' if x == 'indicator' else x for x in level_1]

new_col = df.columns.set_levels([renamed_0, renamed_1])
df.columns = new_col

date = df['Date']

for company_name in all_companies:
    print(f'Processing {company_name}')
    cm_data = df[company_name]
    date.join(cm_data).to_csv(f'data/{company_name}.csv', index=False)

