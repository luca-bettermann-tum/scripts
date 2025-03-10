import pandas as pd

# Define file paths
base_csv_file = 'csv_files/base.csv'
grades_csv_file = 'csv_files/grades.csv'
output_csv_file = 'csv_files/output.csv'

# Define the columns
# match_column_base = 'DB_Primary_Key_Of_Candidate'
match_column_base = 'REGISTRATION_NUMBER'
match_column_grades = 'REGISTRATION_NUMBER'
source_column = 'GRADE'
target_column = 'GRADE'

# Read the CSV files
base_df = pd.read_csv(base_csv_file, encoding='utf-8', delimiter=';')
grades_df = pd.read_csv(grades_csv_file, encoding='utf-8', delimiter=';')
# grades_df = pd.read_csv(grades_csv_file, encoding='latin_1')

# check whether columns exist in the dataframes
if match_column_base not in base_df.columns:
    raise ValueError(f'{match_column_base} not found in base CSV file')
if match_column_grades not in grades_df.columns:
    raise ValueError(f'{match_column_grades} not found in grades CSV file')
if source_column not in grades_df.columns:
    raise ValueError(f'{source_column} not found in grades CSV file')
if target_column not in base_df.columns:
    raise ValueError(f'{target_column} not found in base CSV file')

# Trim whitespace from the target column
if grades_df[source_column].dtype == 'str':
    grades_df[source_column] = grades_df[source_column].str.strip()

# Ensure that the match_column_grades is of type string and starts with a 0
# grades_df[match_column_grades] = grades_df[match_column_grades].astype(str)
# grades_df[match_column_grades] = grades_df[match_column_grades].str.zfill(8)

# Replace N and B values with Fail and Pass
grades_df[source_column] = grades_df[source_column].replace({'Fail': 'N', 'Pass': 'B'})

# Create a dictionary to map the grades
grades_dict = grades_df.set_index(match_column_grades)[source_column].to_dict()

# Update the grade column in base_df
base_df[target_column] = base_df[match_column_base].map(grades_dict)

# Fill missing values in target column with 'X - 5.0
base_df[target_column] = base_df[target_column].fillna('X-5,0')

# Save the graded CSV file with UTF-8 encoding
base_df.to_csv(output_csv_file, index=False, encoding='utf-8', sep=';')

print('Grades added to the base CSV file.')
