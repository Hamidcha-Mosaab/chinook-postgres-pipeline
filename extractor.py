import os
import json
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_db_connection(cfg):
    return psycopg2.connect(
        host=os.getenv(cfg['host']),
        port=os.getenv(cfg['port']),
        database=os.getenv(cfg['database']),
        user=os.getenv(cfg['user']),
        password=os.getenv(cfg['password'])
    )

def extract_table_to_csv(table_name, conn, output_dir='data'):
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql_query(query, conn)
    output_path = os.path.join(output_dir, f"{table_name}.csv")
    df.to_csv(output_path, index=False)
    print(f"Extracted {table_name} to {output_path}")

def main():
    with open('config/config.json') as f:
        config = json.load(f)

    source_config = config['source_db']
    tables = config['tables']

    conn = get_db_connection(source_config)

    os.makedirs('data', exist_ok=True)

    for table in tables:
        extract_table_to_csv(table, conn)

    conn.close()

if __name__ == "__main__":
    main()
