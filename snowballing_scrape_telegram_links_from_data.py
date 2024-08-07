import pandas as pd
from tqdm import tqdm
import os
import re

def extract_telegram_links(content):
    """
    Extract Telegram links from a given content string.

    Parameters:
    content (str): The content from which to extract Telegram links.

    Returns:
    list: A list of Telegram links found in the content.
    """
    return re.findall(r'(https?://t\.me/[^\s]+)', content)

def normalize_telegram_link(link):
    """
    Normalize Telegram links to consider only the main part.

    Parameters:
    link (str): The Telegram link to normalize.

    Returns:
    str: The normalized Telegram link, or None if the link does not match the pattern.
    """
    base_link = re.match(r'(https?://t\.me/[\w\d\+]+)', link)
    return base_link.group(1) if base_link else None

def process_file_for_telegram_links(folder_path, input_filename, output_filename):
    """
    Process a Parquet file to extract, normalize, and count Telegram links.

    Parameters:
    folder_path (str): The path to the folder containing the Parquet file.
    input_filename (str): The name of the input Parquet file.
    output_filename (str): The name of the output Excel file to save the results.

    Returns:
    None

    Steps:
    1. Load the Parquet file into a DataFrame.
    2. Extract Telegram links from the 'Content' column.
    3. Flatten the list of extracted links.
    4. Normalize the Telegram links.
    5. Count the frequency of unique Telegram links.
    6. Save the results to an Excel file.

    Usage:
    Place the Parquet file to be processed in the specified folder path and specify the appropriate column names and output file name.

    Example:
    process_file_for_telegram_links(
        folder_path=r'C:\Users\Public\PyCharmProjects\Data_Conspira',
        input_filename="unified_data_telegram.parquet",
        output_filename='telegram_links.xlsx'
    )
    """
    # Combine folder path and input filename to get the full file path
    file_path = os.path.join(folder_path, input_filename)

    # Load the Parquet file with progress bar
    print(f"Loading {file_path}...")
    df = pd.read_parquet(file_path)

    # Extract Telegram links from the 'Content' column with progress bar
    print("Extracting Telegram links...")
    tqdm.pandas(desc="Extracting Telegram links")
    df['Telegram Links'] = df['Content'].progress_apply(lambda x: extract_telegram_links(str(x)))

    # Flatten the list of lists and filter out empty entries with progress bar
    print("Flattening list of Telegram links...")
    all_links = [link for sublist in tqdm(df['Telegram Links'].tolist(), desc="Flattening links") for link in sublist]

    # Normalize the links
    print("Normalizing Telegram links...")
    normalized_links = [normalize_telegram_link(link) for link in tqdm(all_links, desc="Normalizing links")]

    # Filter out None values
    normalized_links = [link for link in normalized_links if link]

    # Create a DataFrame with the unique links and their frequency
    print("Counting unique links...")
    link_counts = pd.Series(tqdm(normalized_links, desc="Counting links")).value_counts().reset_index()
    link_counts.columns = ['Telegram Link', 'Frequency']

    # Save the result to a new Excel file
    output_path = os.path.join(folder_path, output_filename)
    print(f"Saving the Telegram links to '{output_path}'...")
    link_counts.to_excel(output_path, index=False)

    print(f"Analysis completed and saved to '{output_path}'")

# Usage
folder_path = r'C:\Users\Public\PyCharmProjects\Data_Conspira' # Example
input_filename = "unified_data_telegram.parquet" # Example
output_filename = 'telegram_links.xlsx' # Example
process_file_for_telegram_links(folder_path, input_filename, output_filename)
