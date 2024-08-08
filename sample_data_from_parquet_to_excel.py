import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import re
import json

def remove_urls(text):
    
    # Remove URLs from a given text string.

    # Parameters:
    # text (str): The text from which URLs should be removed.

    # Returns:
    # str: The text without URLs.
    
    url_pattern = r'http\S+|www\S+'
    cleaned_text = re.sub(url_pattern, '', text)
    return cleaned_text

def sample_data_proportionally(df, text_column, category_column, sample_size):
    
    # Sample data proportionally based on categories to reach a maximum sample size,
    # rounding up and ensuring at least one sample per category.

    # Parameters:
    # df (DataFrame): The DataFrame containing the data to sample.
    # text_column (str): The column name containing the text data.
    # category_column (str): The column name containing the category data.
    # sample_size (int): The maximum number of rows to sample.

    # Returns:
    # DataFrame: A DataFrame containing the sampled data.
    
    sample_df = pd.DataFrame()
    categories = df[category_column].unique()
    total_rows = len(df)

    for category in tqdm(categories, desc="Sampling categories"):
        category_df = df[df[category_column] == category]
        category_size = len(category_df)
        proportion = category_size / total_rows
        category_sample_size = max(1, int(np.ceil(proportion * sample_size)))

        # Prioritize rows with content in text_column
        non_empty_text_df = category_df[category_df[text_column].notna() & (category_df[text_column].str.strip() != "")]

        if len(non_empty_text_df) >= category_sample_size:
            category_sample = non_empty_text_df.sample(category_sample_size)
        elif not non_empty_text_df.empty:
            empty_text_sample_size = category_sample_size - len(non_empty_text_df)
            empty_text_df = category_df[~category_df.index.isin(non_empty_text_df.index)]
            empty_text_sample = empty_text_df.sample(empty_text_sample_size, replace=True)
            category_sample = pd.concat([non_empty_text_df, empty_text_sample])
        else:
            # If all text_column entries are empty, sample from the original category_df
            category_sample = category_df.sample(category_sample_size, replace=True)

        sample_df = pd.concat([sample_df, category_sample])

    return sample_df

def create_sampled_file(folder_path, input_filename, text_column, category_column, sample_size, output_filename, min_length):
    
    # Create a sampled file based on the input Parquet file.

    # Parameters:
    # folder_path (str): The path to the folder containing the Parquet file.
    # input_filename (str): The name of the input Parquet file.
    # text_column (str): The column name containing the text data.
    # category_column (str): The column name containing the category data.
    # sample_size (int): Maximum number of rows to sample.
    # output_filename (str): The name of the output file.
    # min_length (int): Minimum length of text content to include in analysis.

    # Returns:
    # None

    # Steps:
    # 1. Load the Parquet file into a DataFrame.
    # 2. Filter the data based on text length.
    # 3. Remove URLs from the text column.
    # 4. Decode the 'Comments List' column from JSON, if present.
    # 5. Sample data proportionally based on categories.
    # 6. Save the sampled data to a new Excel file.

    # Usage:
    # Place the Parquet file to be sampled in the specified folder path and specify the appropriate column names, sample size, output file name, and minimum text length.

    # Example:
    # create_sampled_file(
    #     folder_path=r'C:\Users\Public\PyCharmProjects\Data_Conspira',
    #     input_filename="unified_data_telegram.parquet",
    #     text_column="Content",
    #     category_column="Group",
    #     sample_size=10000,
    #     output_filename='sampled_data.xlsx',
    #     min_length=20
    # )
    
    input_file_path = os.path.join(folder_path, input_filename)

    # Load the Parquet file into a DataFrame
    print("Loading Parquet file...")
    df = pd.read_parquet(input_file_path)

    # Filter the data based on text length
    tqdm.pandas(desc="Filtering based on text length")
    df = df[df[text_column].str.len() > min_length]

    # Remove URLs from the text column
    tqdm.pandas(desc="Removing URLs from text")
    df[text_column] = df[text_column].progress_apply(remove_urls)

    # Decode the 'Comments List' column from JSON
    if 'Comments List' in df.columns:
        tqdm.pandas(desc="Decoding 'Comments List' column")
        df['Comments List'] = df['Comments List'].progress_apply(lambda x: json.loads(x) if pd.notnull(x) else x)

    # Sample data proportionally
    sample_df = sample_data_proportionally(df, text_column, category_column, sample_size)

    # Save the sampled data to a new Excel file
    output_path = os.path.join(folder_path, output_filename)
    sample_df.to_excel(output_path, index=False, engine='openpyxl')

    print(f"Sampled data saved in file: {output_path}")


# Usage
folder_path = r'C:\Users\Public\PyCharmProjects\Data_Conspira' # Example
input_filename = "unified_data_telegram.parquet" # Example
text_column = "Content"
category_column = "Group"
sample_size = 10000 # Example
output_filename = 'sampled_data.xlsx' # Example
min_length = 20 # Example

create_sampled_file(folder_path, input_filename, text_column, category_column, sample_size, output_filename, min_length)
