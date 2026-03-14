import pandas as pd
import glob
import os

# Path where your monthly CSVs are stored
data_path = "data"

# Get all CSV files that match the monthly pattern
csv_files = sorted(glob.glob(os.path.join(data_path, "imdb_2024_*.csv")))

# Read and concatenate
dfs = []
for file in csv_files:
    df = pd.read_csv(file)
    dfs.append(df)

# Merge into one DataFrame
merged_df = pd.concat(dfs, ignore_index=True)

# Save consolidated file
merged_df.to_csv(os.path.join(data_path, "imdb_2024_all.csv"), index=False)

print(f"Merged {len(csv_files)} files into imdb_2024_all.csv")
print("Total movies:", len(merged_df))
