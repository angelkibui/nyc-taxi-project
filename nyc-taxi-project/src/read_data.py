import pandas as pd

# Path to your parquet file
file_path = "data/raw/yellow_tripdata_2025-08.parquet"

# Read the parquet file
df = pd.read_parquet(file_path)

# Print first 5 rows
print(df.head())

# Print info about the columns
print(df.info())
