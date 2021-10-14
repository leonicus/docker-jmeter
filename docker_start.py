import pandas as pd
import os, shutil
def fix_jtl_file(file):
    shutil.copy(file, 'backup.jtl')
    df = pd.read_csv(file)
    df['responseCode'] = pd.to_numeric(df['responseCode'], errors='coerce')
    df = df[(df['responseCode'] == 200) | (df['responseCode'] == 0)]
    result_df = pd.DataFrame(columns=df.label.value_counts().index.values)
    for c in result_df.columns:
        result_df[c] = df.loc[df['label'] == c].reset_index()['elapsed'].astype('float64')
    # result_df.columns = [f'{c}' for c in result_df.columns]
    result_df = result_df.dropna()
    return result_df
for f in os.listdir():
    if 'jtl' in f:
        df = fix_jtl_file(f)
        median_df = df.median()
        top_df = df.quantile(0.9)
        merged = pd.concat([median_df,top_df],axis=1)
        merged.columns = ['median', '90th_percentile']
        print(merged.to_json())
