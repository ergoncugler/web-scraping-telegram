import pandas as pd
from tqdm import tqdm
import os
import json

def filter_and_save_by_keywords(folder_path, input_filename, output_filename, content_col, keywords, max_rows_per_file):
    """
    Filters the rows based on keywords in the specified column, adds a column for each keyword indicating its presence,
    and saves the result to new Excel files if the maximum number of rows is exceeded.

    Parameters:
    folder_path (str): The path to the folder containing the Parquet file.
    input_filename (str): The name of the input Parquet filename.
    content_col (str): The column name containing the content data.
    keywords (list): The list of keywords to filter the content.
    output_filename (str): The base name of the output Excel file.
    max_rows_per_file (int): The maximum number of rows per output file.

    Returns:
    None

    Steps:
    1. Load the Parquet file into a DataFrame.
    2. Decode the 'Comments List' column from JSON, if present.
    3. Create a new column for each keyword indicating its presence in the content.
    4. Add a column that counts the number of keywords found in each row.
    5. Filter the DataFrame to include only rows where at least one keyword was found.
    6. Split and save the filtered DataFrame into multiple Excel files if necessary.

    Usage:
    Place the Parquet file to be filtered in the specified folder path and specify the appropriate column names, keywords, output file name, and maximum number of rows per file.

    Example:
    filter_and_save_by_keywords(
        folder_path=r'C:\Users\Public\PyCharmProjects\Data_Conspira',
        input_filename="unified_data_telegram.parquet",
        content_col='Content',
        keywords=['Trump', 'Biden', 'Kamala'],
        output_filename='filtered_keywords',
        max_rows_per_file=1000000
    )
    """
    try:
        # Combine folder path and input filename to get the full file path
        input_file_path = os.path.join(folder_path, input_filename)

        # Load the Parquet file
        print(f"Loading {input_file_path}...")
        df = pd.read_parquet(input_file_path)

        # Decode the 'Comments List' column from JSON
        if 'Comments List' in df.columns:
            tqdm.pandas(desc="Decoding 'Comments List' column")
            df['Comments List'] = df['Comments List'].progress_apply(lambda x: json.loads(x) if pd.notnull(x) else x)

        # Create a new column for each keyword
        print("Creating keyword columns...")
        for keyword in tqdm(keywords, desc="Creating keyword columns"):
            df[keyword] = df[content_col].astype(str).apply(lambda x: 1 if keyword in x else 0)

        # Add a column that counts the number of keywords found in each row
        print("Adding count of keywords found...")
        df['Keyword_Count'] = df[keywords].sum(axis=1)

        # Filter the DataFrame to only include rows where at least one keyword was found
        print("Filtering by keywords...")
        filtered_df = df[df['Keyword_Count'] > 0]

        # Print the number of rows in the filtered dataframe
        print(f"Number of rows in the filtered dataframe: {len(filtered_df)}")

        # Split and save the final files
        num_files = (len(filtered_df) // max_rows_per_file) + 1

        for i in tqdm(range(num_files), desc="Saving files"):
            start_row = i * max_rows_per_file
            end_row = (i + 1) * max_rows_per_file
            output_df = filtered_df.iloc[start_row:end_row]

            part_suffix = 'unique' if num_files == 1 else f'part_{i + 1}'
            output_path = os.path.join(folder_path, f'{output_filename}_{part_suffix}.xlsx')
            output_df.to_excel(output_path, index=False, engine='openpyxl')

            print(f"Filtered file saved at: {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
folder_path = r'C:\Users\Public\PyCharmProjects\Data_Conspira' # Example
input_filename = "unified_data_telegram.parquet" # Example
content_col = 'Content'
keywords = ['Trump', 'Biden', 'Kamala']  # Add your keywords here
output_filename = 'filtered_keywords' # Example
max_rows_per_file = 1000000  # Adjust the maximum number of rows per file as needed (max for .xlsx is 1,048,576)

filter_and_save_by_keywords(folder_path, input_filename, output_filename, content_col, keywords, max_rows_per_file)
