import pandas as pd

input_file = "CVAP state upper house chambers 5 year 2024.csv"
output_file = "upper_converted.csv"

wanted_groups = [
    "Total",
    "American Indian or Alaska Native Alone",
    "Asian Alone",
    "Black or African American Alone",
    "Native Hawaiian or Other Pacific Islander Alone",
    "White Alone",
    "Hispanic or Latino",
]

df = pd.read_csv(input_file)

# Keep only the rows we want
df_filtered = df[df["lntitle"].isin(wanted_groups)]

# Pivot lntitle values into columns
wide = df_filtered.pivot_table(
    index="geoname",
    columns="lntitle",
    values="cvap_est",
    aggfunc="sum"
).reset_index()

# Optional: keep columns in exact desired order
wide = wide[["geoname"] + wanted_groups]

wide.to_csv(output_file, index=False)

print(f"Saved reformatted file to {output_file}")