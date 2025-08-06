import pandas as pd

# File name (make sure it's in the same directory as this script)
file_name = "HR_DataBase_Dev.xlsx"

# Read Excel file
df = pd.read_excel(file_name)

# Normalize column names for easier matching
df.columns = df.columns.str.strip()

# Extract the 'MANAGEMENT UNIT/COST CENTRE' column (case-insensitive)
search_column = "management unit/cost centre"
district_column = None
for col in df.columns:
    if search_column in col.lower():
        district_column = col
        break

if district_column:
    # Drop empty values and duplicates
    districts = df[district_column].dropna().drop_duplicates()

    # Save to .txt file
    output_file = "districts.txt"
    districts.to_csv(output_file, index=False, header=False)
    print(f"✅ Data extracted from '{district_column}' and saved to {output_file}")
else:
    print("❌ No column named 'MANAGEMENT UNIT/COST CENTRE' found in the Excel file.")
