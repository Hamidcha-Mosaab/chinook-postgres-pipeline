import pandas as pd
import json

def map_columns(df, table_name, mapping):
    if table_name in mapping:
        rename_dict = {k: v['new_name'] for k, v in mapping[table_name].items()}
        df = df.rename(columns=rename_dict)
        for col, rules in mapping[table_name].items():
            new_col = rules['new_name']
            if rules['type'] == 'int':
                df[new_col] = df[new_col].astype('Int64', errors='ignore')
            elif rules['type'] == 'float':
                df[new_col] = df[new_col].astype(float, errors='ignore')
            elif rules['type'] == 'str':
                df[new_col] = df[new_col].astype(str)
            elif rules['type'] == 'datetime':
                df[new_col] = pd.to_datetime(df[new_col], errors='coerce')
    return df

def load_mapping():
    with open('config/mapping.json') as f:
        return json.load(f)
