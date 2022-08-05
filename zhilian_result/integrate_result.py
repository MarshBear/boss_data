import pandas as pd
import os
import time

city = 'hangzhou'

files = os.listdir(f'{city}_result')

for file in files:
    df_new = pd.read_csv(f'{city}_result/{file}')
    if 'df' not in locals():
        df = df_new
    else:
        df = pd.concat((df, df_new), axis=0)

df = df.drop_duplicates().sort_values('origin_index')
df.to_csv(f'{int(time.time())}_{city}_all.csv', index=False, encoding='utf8')
