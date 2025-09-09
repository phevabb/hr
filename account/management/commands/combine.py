import pandas as pd

# Load the Excel file
df = pd.read_excel("HR_DataBase_Dev.xlsx")

# Combine CURRENT GRADE and NEXT GRADE
combined = pd.concat([df["CURRENT GRADE"], df["NEXT GRADE"]])

# Drop NaN and remove duplicates
unique_grades = combined.dropna().drop_duplicates().reset_index(drop=True)

# Save results to a .txt file (one grade per line)
with open("unique_grades.txt", "w", encoding="utf-8") as f:
    for grade in unique_grades:
        f.write(str(grade) + "\n")

print(f"✅ Done! Extracted {len(unique_grades)} unique grades into unique_grades.txt")
