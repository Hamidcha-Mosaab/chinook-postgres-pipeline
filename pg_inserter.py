import os
import json
import psycopg2
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

def get_db_connection(cfg):
    return psycopg2.connect(
        host=os.getenv(cfg['host']),
        port=os.getenv(cfg['port']),
        database=os.getenv(cfg['database']),
        user=os.getenv(cfg['user']),
        password=os.getenv(cfg['password'])
    )

def create_table_if_not_exists(table_name, df, conn, mapping):
    columns = []
    for col in df.columns:
        if table_name in mapping and col in [v['new_name'] for v in mapping[table_name].values()]:
            original_col = next(k for k, v in mapping[table_name].items() if v['new_name'] == col)
            col_type = mapping[table_name][original_col]['type']
            if col_type == 'int':
                sql_type = 'INTEGER'
            elif col_type == 'float':
                sql_type = 'REAL'
            elif col_type == 'str':
                sql_type = 'TEXT'
            elif col_type == 'datetime':
                sql_type = 'TIMESTAMP'
            else:
                sql_type = 'TEXT'
        else:
            sql_type = 'TEXT'
        columns.append(f'"{col}" {sql_type}')

    create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
    with conn.cursor() as cur:
        cur.execute(create_query)
    conn.commit()

def insert_data(table_name, df, conn):
    if df.empty:
        print(f"No rows to insert for {table_name}")
        return
    columns = ', '.join([f'"{col}"' for col in df.columns])
    placeholders = ', '.join(['%s'] * len(df.columns))
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    with conn.cursor() as cur:
        for _, row in df.iterrows():
            cur.execute(insert_query, tuple(row))
    conn.commit()

def load_data_to_pg(table_name, csv_path, conn, mapping):
    df = pd.read_csv(csv_path)
    create_table_if_not_exists(table_name, df, conn, mapping)
    insert_data(table_name, df, conn)
    print(f"Inserted {len(df)} rows into {table_name}")
