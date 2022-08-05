import os
import pandas as pd

city_name = 'shenzhen'

files = os.listdir(f'./{city_name}_urls/')

for file in files:
    category = file.strip('.csv').split('_')
    df_new = pd.read_csv(f'./{city_name}_urls/{file}')
    for i in range(3):
        df_new[f'category{i+1}'] = category[i]
    if 'df' not in locals():
        df = df_new
    else:
        df = pd.concat((df, df_new), axis=0)
df = df.drop_duplicates()
df.to_csv(f'{city_name}_urls.csv', index=False, encoding='utf8')
