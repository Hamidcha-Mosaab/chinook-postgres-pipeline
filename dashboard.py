import dash
from dash import html, dcc
import plotly.express as px
import psycopg2
import os
from dotenv import load_dotenv
import json
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

def get_table_stats(conn, tables):
    stats = []
    for table in tables:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {table};")
            row_count = cur.fetchone()[0]
            cur.execute(f"SELECT COUNT(*) FROM information_schema.columns WHERE table_name = '{table.lower()}';")
            col_count = cur.fetchone()[0]
            stats.append({'Table': table, 'Rows': row_count, 'Columns': col_count})
    return stats

app = dash.Dash(__name__)

with open('config/config.json') as f:
    config = json.load(f)

target_config = config['target_db']
tables = config['tables']
conn = get_db_connection(target_config)
stats = get_table_stats(conn, tables)
conn.close()

df_stats = pd.DataFrame(stats)

app.layout = html.Div([
    html.H1('Data Ingestion Dashboard'),
    dcc.Graph(
        id='table-stats',
        figure=px.bar(df_stats, x='Table', y='Rows', title='Row Count per Table')
    ),
    dcc.Graph(
        id='column-stats',
        figure=px.bar(df_stats, x='Table', y='Columns', title='Column Count per Table')
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
