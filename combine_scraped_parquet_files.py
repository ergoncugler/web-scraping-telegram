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
    # 3. Remove rows where 'Group' is '@ohospicio' (commented out).
    # 4. Remove duplicate rows based on specified columns.
    # 5. Ensure items in 'Group' column start with '@'.
    # 6. Recalculate the 'Comments' column by counting occurrences of 'Type': 'comment' in 'Comments List'.
    # 7. Convert 'Message ID' column to string type.
    # 8. Convert 'Media' column to boolean type.
    # 9. Sort the DataFrame by 'Date' in descending order.
    # 10. Print the number of rows, number of comments, and total contents.
    # 11. Save the combined DataFrame to a Parquet file.
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

    # Function to read data from each Parquet file
    def read_parquet(file_path):
        return pd.read_parquet(file_path)

    # List of Parquet files in the folder
    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.parquet')]

    # Read and combine the data
    combined_df = pd.concat([df for df in (read_parquet(file) for file in tqdm(file_paths, desc="Reading files")) if
                             not df.empty and not df.isna().all().all()], ignore_index=True)

    # Remove duplicates based on specified columns
    combined_df.drop_duplicates(subset=duplicate_columns, inplace=True)

    # Add "@" to the beginning of items in 'Group' column if missing
    combined_df['Group'] = combined_df['Group'].apply(lambda x: x if x.startswith('@') else '@' + x)

    # Define a function to count comments in the 'Comments List' JSON
    def count_comments(comments_list):
        if pd.isna(comments_list):
            return 0
        comments_list = json.loads(comments_list)
        return sum(1 for item in comments_list if item.get('Type') == 'comment')

    if 'Comments' not in combined_df.columns:
        combined_df['Comments'] = 0

    # Recalculate 'Comments' column with the count of 'Type': 'comment' occurrences in 'Comments List' using tqdm
    combined_df['Comments'] = [count_comments(row['Comments List']) for row in
                               tqdm(combined_df.to_dict(orient="records"), desc="Calculating Comments")]

    # Convert 'Comments' column to integers
    combined_df['Comments'] = combined_df['Comments'].astype(int)

    # Ensure 'Message ID' column is of string type
    combined_df['Message ID'] = combined_df['Message ID'].astype(str)

    # Ensure 'Media' column is of boolean type or handle the conversion
    combined_df['Media'] = combined_df['Media'].astype(bool)

    # Sort 'Date' as z-a
    combined_df['Date'] = pd.to_datetime(combined_df['Date'])
    combined_df = combined_df.sort_values(by='Date', ascending=False)

    # Calculate the number of comments
    num_comments = combined_df['Comments'].sum()

    # Print the number of rows, number of comments, and total contents (rows + comments)
    print("\n")
    print(f" / Number of rows in the combined dataframe: {len(combined_df)}")
    print(f" / Number of comments: {num_comments}")
    print(f" / Total contents (rows + comments): {len(combined_df) + num_comments}")

    # Save the combined DataFrame to a Parquet file
    combined_df.to_parquet(output_file_path, index=False)

    print(f" / Combined file saved at: {output_file_path}")


# Usage
folder_path = r'C:\Users\Public\PyCharmProjects\Data_Conspira'
duplicate_columns = ['Group', 'Message ID']
output_file_path = os.path.join(folder_path, 'data_conspira_telegram.parquet')

combine_parquet_files(folder_path, duplicate_columns, output_file_path)
