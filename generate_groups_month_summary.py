import pandas as pd
from tqdm import tqdm
import os

def create_group_month_summary(folder_path, input_filename, output_filename_base, date_col, group_col, comments_col):
    
    # Creates summary tables showing the number of contents, comments, and total (contents + comments) each group had per month.

    # Parameters:
    # folder_path (str): The path to the folder containing the Parquet file.
    # input_filename (str): The name of the input Parquet file.
    # date_col (str): The column name containing the date data.
    # group_col (str): The column name containing the group data.
    # comments_col (str): The column name containing the comments data.
    # output_filename_base (str): The base name of the output Excel files.

    # Returns:
    # None

    # Steps:
    # 1. Load the Parquet file into a DataFrame.
    # 2. Convert the date column to datetime.
    # 3. Add a new column with the month and year of the date.
    # 4. Group the DataFrame by 'Group' and 'MonthYear' and count the number of items.
    # 5. Group the DataFrame by 'Group' and 'MonthYear' and sum the comments.
    # 6. Sum contents and comments.
    # 7. Reindex to include all months from the first to the last.
    # 8. Convert the PeriodIndex back to string format for Excel compatibility.
    # 9. Save the resulting DataFrames to Excel files.

    # Usage:
    # Place the Parquet file to be summarized in the specified folder path and specify the appropriate column names and output file base name.

    # Example:
    # create_group_month_summary(
    #     folder_path=r'C:\Users\Public\PyCharmProjects\Data_Conspira',
    #     input_filename='unified_data_telegram.parquet',
    #     output_filename_base='resume',
    #     date_col='Date',
    #     group_col='Group',
    #     comments_col='Comments'
    # )
    
    try:
        # Load the Parquet file into a DataFrame
        input_file_path = os.path.join(folder_path, input_filename)
        df = pd.read_parquet(input_file_path)

        # Convert the 'Date' column to datetime
        df[date_col] = pd.to_datetime(df[date_col])

        # Add a new column with the month and year of the date
        df['MonthYear'] = df[date_col].dt.to_period('M')

        # Group the DataFrame by 'Group' and 'MonthYear' and count the number of items
        df_contents = df.groupby([group_col, 'MonthYear']).size().unstack().fillna(0)

        # Group the DataFrame by 'Group' and 'MonthYear' and sum the comments
        df_comments = df.groupby([group_col, 'MonthYear'])[comments_col].sum().unstack().fillna(0)

        # Sum contents and comments
        df_total = df_contents.add(df_comments, fill_value=0)

        # Reindex to include all months from the first to the last
        all_months = pd.period_range(start=df_contents.columns.min(), end=df_contents.columns.max(), freq='M')
        df_contents = df_contents.reindex(columns=all_months, fill_value=0)
        df_comments = df_comments.reindex(columns=all_months, fill_value=0)
        df_total = df_total.reindex(columns=all_months, fill_value=0)

        # Convert the PeriodIndex back to string format for Excel compatibility
        df_contents.columns = df_contents.columns.astype(str)
        df_comments.columns = df_comments.columns.astype(str)
        df_total.columns = df_total.columns.astype(str)

        # Save the resulting DataFrames to Excel files
        output_file_path_contents = os.path.join(folder_path, f"{output_filename_base}_contents.xlsx")
        df_contents.to_excel(output_file_path_contents, index=True)

        output_file_path_comments = os.path.join(folder_path, f"{output_filename_base}_comments.xlsx")
        df_comments.to_excel(output_file_path_comments, index=True)

        output_file_path_total = os.path.join(folder_path, f"{output_filename_base}_total.xlsx")
        df_total.to_excel(output_file_path_total, index=True)

        print(f"Contents summary table saved as: {output_file_path_contents}")
        print(f"Comments summary table saved as: {output_file_path_comments}")
        print(f"Total summary table saved as: {output_file_path_total}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Usage
create_group_month_summary(
    folder_path=r'C:\Users\Public\PyCharmProjects\Data_Conspira', # Example
    input_filename='unified_data_telegram.parquet', # Example
    output_filename_base='resume', # Example
    date_col='Date',
    group_col='Group',
    comments_col='Comments'
)
