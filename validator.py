import pandas as pd

def validate_data(df, table_name):
    issues = []
    if df.empty:
        issues.append(f"{table_name}: DataFrame is empty")
    if df.isnull().sum().sum() > 0:
        issues.append(f"{table_name}: Contains null values")
    # Add more validations as needed
    return issues
