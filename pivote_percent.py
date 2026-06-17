import pandas as pd

input_file = "CVAP 119th Congress 5 year 2024.csv"
output_file = "congress_percent.csv"

wanted_groups = [
    "American Indian or Alaska Native Alone",
    "Asian Alone",
    "Black or African American Alone",
    "Native Hawaiian or Other Pacific Islander Alone",
    "White Alone",
    "Hispanic or Latino",
]

df = pd.read_csv(input_file)

# Get Total CVAP for each geoname
totals = (
    df[df["lntitle"] == "Total"]
    [["geoname", "cvap_est"]]
    .rename(columns={"cvap_est": "Total"})
)

# Keep only desired race/ethnicity rows
df_filtered = df[df["lntitle"].isin(wanted_groups)]

# Pivot to wide format
wide = (
    df_filtered
    .pivot_table(
        index="geoname",
        columns="lntitle",
        values="cvap_est",
        aggfunc="sum"
    )
    .reset_index()
)

# Merge totals
wide = wide.merge(totals, on="geoname", how="left")

# Ensure desired column order
wide = wide[["geoname"] + wanted_groups + ["Total"]]

# Add percentage columns
for group in wanted_groups:
    pct_col = f"{group} %"
    wide[pct_col] = (wide[group] / wide["Total"] * 100).round(2)

# Optional column ordering
wide = wide[
    ["geoname", "Total"] +
    wanted_groups +
    [f"{g} %" for g in wanted_groups]
]

wide.to_csv(output_file, index=False)

print(f"Saved reformatted file to {output_file}")