import os
import json
from src.mapper import map_columns, load_mapping
from src.validator import validate_data
from src.pg_inserter import get_db_connection, load_data_to_pg

def main():
    with open('config/config.json') as f:
        config = json.load(f)

    target_config = config['target_db']
    tables = config['tables']
    mapping = load_mapping()

    conn = get_db_connection(target_config)

    for table in tables:
        csv_path = os.path.join('data', f"{table}.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df = map_columns(df, table, mapping)
            issues = validate_data(df, table)
            if issues:
                print(f"Validation issues for {table}: {issues}")
            else:
                load_data_to_pg(table, csv_path, conn, mapping)
        else:
            print(f"CSV for {table} not found")

    conn.close()

if __name__ == "__main__":
    main()
