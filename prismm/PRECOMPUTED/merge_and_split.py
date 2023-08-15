import os
import pandas as pd
import numpy as np

path_description = "p5_v5"
base_path = f"MATRICES/{path_description}"

# List of (i, j) combinations for which table files exist
combinations = [(i, j) for i in range(0, 100) for j in range(0, 100)]  # Adjust as needed

frames = []  # A list to store all dataframes we'll be concatenating

for i, j in combinations:
    table_file = os.path.join(base_path, f"table_u{i:.2f}_d{j:.2f}.csv")
    if os.path.exists(table_file):
        df = pd.read_csv(table_file)
        frames.append(df)
    else:
        print(f"Warning: {table_file} does not exist!")

# Concatenate all dataframes
concatenated_df = pd.concat(frames, ignore_index=True)

# Save the first 3 column names
names = concatenated_df.columns[:3]
names.to_csv(os.path.join(base_path, "names.csv"), index=False)

# For each CN column, save the column to its respective numpy file
for col in concatenated_df.columns:
    if "CN_" in col:
        cn_index = int(col.split("_")[1])
        output_np_file = os.path.join(base_path, f"concatenated_tables_{cn_index}.npy")
        np_array = concatenated_df[col].values
        np.save(output_np_file, np_array)

print("All CN columns saved to their respective numpy files.")

