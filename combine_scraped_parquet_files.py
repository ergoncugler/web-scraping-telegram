import os
import pandas as pd
from tqdm import tqdm
import json

def combine_parquet_files(folder_path, duplicate_columns, output_file_path):

    # Combines multiple Parquet files from a specified folder into a single DataFrame,
    # removes duplicates, adjusts the 'Group' and 'Comments' columns, and saves the result as a Parquet file.
    #
    # Parameters:
    # folder_path (str): Path to the folder containing the Parquet files to be combined.
    # duplicate_columns (list of str): List of column names to check for duplicates.
    # output_file_path (str): Path to save the combined Parquet file.
    #
    # Returns:
    # None
    #
    # Steps:
    # 1. Read each Parquet file in the specified folder.
    # 2. Concatenate the data from all Parquet files into a single DataFrame.
    # 3. Convert 'Message ID' column to string type.
    # 4. Ensure items in 'Group' column start with '@'.
    # 5. Remove duplicate rows based on specified columns.
    # 6. Recalculate the 'Comments' column by counting occurrences of 'Type': 'comment' in 'Comments List'.
    # 7. Convert 'Media' column to boolean type.
    # 8. Sort the DataFrame by 'Date' in descending order.
    # 9. Print the number of rows, number of comments, and total contents.
    # 10. Save the combined DataFrame to a Parquet file.
    #
    # Usage:
    # Place all .parquet files to be unified in the specified folder path.
    #
    # Example:
    # folder_path = r'C:\Users\Public\PyCharmProjects\Data_Conspira'
    # duplicate_columns = ['Group', 'Message ID']
    # output_file_path = os.path.join(folder_path, 'data_conspira_telegram.parquet')
    #
    # combine_parquet_files(folder_path, duplicate_columns, output_file_path)

    def read_parquet(file_path):
        return pd.read_parquet(file_path)

    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.parquet')]

    combined_df = pd.concat([df for df in (read_parquet(file) for file in tqdm(file_paths, desc="Reading files")) if
                             not df.empty and not df.isna().all().all()], ignore_index=True)

    # Convert 'Message ID' to string type before checking duplicates
    combined_df['Message ID'] = combined_df['Message ID'].astype(str)

    # Add "@" to the beginning of items in 'Group' column if missing before checking duplicates
    combined_df['Group'] = combined_df['Group'].apply(lambda x: x if x.startswith('@') else '@' + x)

    print(f"Number of rows before removing duplicates: {len(combined_df)}")
    print(f"Checking duplicates based on columns {duplicate_columns}...")
    print(combined_df.duplicated(subset=duplicate_columns).sum(), "duplicated rows found.")

    combined_df.drop_duplicates(subset=duplicate_columns, inplace=True)

    print(f"Number of rows after removing duplicates: {len(combined_df)}")

    def count_comments(comments_list):
        if pd.isna(comments_list):
            return 0
        comments_list = json.loads(comments_list)
        return sum(1 for item in comments_list if item.get('Type') == 'comment')

    if 'Comments' not in combined_df.columns:
        combined_df['Comments'] = 0

    combined_df['Comments'] = [count_comments(row['Comments List']) for row in
                               tqdm(combined_df.to_dict(orient="records"), desc="Calculating Comments")]

    combined_df['Comments'] = combined_df['Comments'].astype(int)
    combined_df['Media'] = combined_df['Media'].astype(bool)

    combined_df['Date'] = pd.to_datetime(combined_df['Date'])
    combined_df = combined_df.sort_values(by='Date', ascending=False)

    num_comments = combined_df['Comments'].sum()

    print("\n")
    print(f" / Number of rows in the combined dataframe: {len(combined_df)}")
    print(f" / Number of comments: {num_comments}")
    print(f" / Total contents (rows + comments): {len(combined_df) + num_comments}")

    combined_df.to_parquet(output_file_path, index=False)

    print(f" / Combined file saved at: {output_file_path}")


# Usage
folder_path = r'C:\Users\Public\PyCharmProjects\Data_Conspira' # Example
duplicate_columns = ['Group', 'Message ID']
output_file_path = os.path.join(folder_path, 'unified_data_telegram.parquet') # Example

combine_parquet_files(folder_path, duplicate_columns, output_file_path)
