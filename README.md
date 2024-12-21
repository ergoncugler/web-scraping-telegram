# TelegramScrap: A comprehensive tool for scraping Telegram posts and contents [new version updated in August 2024]

This code ([**available here on Github**](https://github.com/ergoncugler/web-scraping-telegram/blob/main/TelegramScrap_A_comprehensive_tool_for_scraping_Telegram_data.ipynb) */or/* [**directly on Google Colab, just play it**](https://colab.research.google.com/drive/1lzn_XomUI9uCMLkGjQf6-2JnkKazgevh?usp=sharing)) aims to scrape data from selected `Telegram Channels, Groups, or Chats` using the `Telethon Library`. It is designed to facilitate the extraction of various data fields including `message content, author information, reactions, views, and comments`. The primary functions of this code include setting up scraping parameters, processing messages and their associated comments, and handling unsupported characters to ensure data integrity. Data is stored in `Apache Parquet files (.parquet)`, which are highly efficient for both storage and processing, making them superior to traditional spreadsheets in terms of speed and scalability. This tool is particularly **useful for researchers and analysts** looking to collect and analyze Telegram data efficiently.

Data is stored as `Apache Parquet (.parquet)`, which are highly efficient for both storage and processing, making them superior to traditional spreadsheets in terms of speed and scalability. Unlike spreadsheets, which have limitations on the number of characters per cell and the total number of rows, Apache Parquet files can handle large datasets with ease. The `.parquet` format also offers faster read and write operations, ensuring that data can be accessed and processed more quickly, making it an ideal choice for handling extensive Telegram data efficiently.

This tool requires initial setup where you need to input your Telegram credentials such as `username, phone, api_id, and api_hash`. These credentials can be generated from the [Telegram API](https://my.telegram.org/apps). Once the initial setup is complete, you can define the scraping parameters like `Channels, Date Range, Output File Name, Keywords, Maximum Messages to Scrape,` and `Timeout` to scrape all the desired content, returning: `'Group', 'Author ID', 'Content', 'Date ', 'Message ID', 'Author', 'Views', 'Reactions', 'Shares', 'Media', 'Comments List'`. The tool then processes messages and their associated comments, ensuring unsupported characters are handled to maintain data integrity. The output is stored in `.parquet` files for efficient storage and processing.

Once the data is extracted into `.parquet` files, various authoring tools are available for analyzing this data. Examples include: [**combine_scraped_parquet_files.py**](https://github.com/ergoncugler/web-scraping-telegram/blob/main/combine_scraped_parquet_files.py), which combines multiple Parquet files into a single DataFrame, removing duplicates and adjusting columns; [**generate_groups_month_summary.py**](https://github.com/ergoncugler/web-scraping-telegram/blob/main/generate_groups_month_summary.py), which creates monthly summary tables for each group, showing the number of contents and comments; [**sample_data_from_parquet_to_excel.py**](https://github.com/ergoncugler/web-scraping-telegram/blob/main/sample_data_from_parquet_to_excel.py), which samples data proportionally based on categories and saves it to an Excel file; [**scrape_and_filter_by_keywords_from_parquet_to_excel.py**](https://github.com/ergoncugler/web-scraping-telegram/blob/main/scrape_and_filter_by_keywords_from_parquet_to_excel.py), which filters rows based on keywords, adds indicator columns for each keyword, and saves the results to Excel files; and [**snowballing_scrape_telegram_links_from_data.py**](https://github.com/ergoncugler/web-scraping-telegram/blob/main/snowballing_scrape_telegram_links_from_data.py), which extracts, normalizes, and counts Telegram links, saving the analysis to an Excel file.

| Tips |
|------|
| **1. Google Colab runtime limit:** Google Colab typically crashes after running this code for around 6 hours and 20 minutes. Therefore, set a limit within this timeframe to avoid interruptions. |
| **2. Telegram API soft ban:** The Telegram API usually imposes a 24-hour soft ban after scraping more than 200 channels or groups. However, there seems to be no limit on the number of messages scraped from fewer communities. To avoid the ban, scrape large amounts of content from blocks of up to 150-200 communities at a time, even if you extract entire months of data from each one or just days. |
| **3. Using Google Colab for async operations:** One advantage of using Google Colab is the ability to run `async` functions without needing to define them within an `async def`. If you plan to use PyCharm or another IDE, consider adapting the code with an `async def`. |
| **4. Handling JSON in 'Comments List' column:** The `'Comments List'` column stores comments in a JSON list format. Remember to decode this JSON when converting to a spreadsheet or presenting the data. |

### Output example:
✅ It was asked to scrape Donald Trump's contents from several Brazilian channels on Telegram, which returned approximately 17,000 posts:
![image](https://github.com/user-attachments/assets/b18c3c0e-8efc-49ab-bfac-4c525d4452b9)

✅ In the realm of scientific articles, this code was instrumental in the study **Informational Co-option against Democracy: Comparing Bolsonaro's Discourses about Voting Machines with the Public Debate** ([**link**](https://dl.acm.org/doi/abs/10.1145/3614321.3614373)). It was also used in **Institutional Denialism From the President's Speeches to the Formation of the Early Treatment Agenda (Off Label) in the COVID-19 Pandemic in Brazil** ([**link**](https://anepecp.org/ojs/index.php/br/article/view/561)). Moreover, the code facilitated research in **Catalytic Conspiracism: Exploring Persistent Homologies Time Series in the Dissemination of Disinformation in Conspiracy Theory Communities on Telegram** ([**link**](https://www.abcp2024.sinteseeventos.com.br/trabalho/view?ID_TRABALHO=687)) and **Conspiratorial Convergence: Comparing Thematic Agendas Among Conspiracy Theory Communities on Telegram Using Topic Modeling** ([**link**](https://www.abcp2024.sinteseeventos.com.br/trabalho/view?ID_TRABALHO=903)). Lastly, it was pivotal in the study **Informational Disorder and Institutions Under Attack: How Did Former President Bolsonaro's Narratives Against the Brazilian Judiciary Between 2019 and 2022 Manifest?** ([**link**](https://www.encontro2023.anpocs.org.br/trabalho/view?ID_TRABALHO=8990)).

✅ Furthermore, the code was utilized in several technical notes, as we can see in **Technical Note #16 – Disinformation about Electronic Voting Machines Persists Outside Election Periods** ([**link**](https://www.monitordigital.org/2023/05/18/nota-tecnica-16-desinformacao-sobre-urnas-eletronicas-persiste-fora-dos-periodos-eleitorais/)). It was also employed in **Technical Note #18 – Electoral Fraud Discourse in Argentina on Telegram and Twitter** ([**link**](https://www.monitordigital.org/2023/10/24/nota-tecnica-18-discurso-de-fraude-eleitoral-na-argentina-no-telegram-e-no-twitter/)). The code contributed to the analysis in the technical note **Bashing and Praising Public Servants and Bureaucrats During the Bolsonaro Government (2019 - 2022)** ([**link**](https://neburocracia.wordpress.com/wp-content/uploads/2024/04/nota-tecnica-neb-fgv-eaesp-como-bolsonaro-equilibrou-ataques-e-acenos-aos-servidores-publicos-e-burocratas-entre-2019-e-2022.pdf)). Additionally, it was used in **Technical Note 2: The Digital Territory of Milei's Followers: From Commerce to Politics** ([**link**](https://pacunla.com/nota-tecnica-2-el-territorio-digital-de-los-seguidores-de-milei-del-comercio-a-la-politica/)).

## Recommendation

### [Data] [Academic Research] [Scientific Research] [Public Policy] [Political Science] [Data Science]

Its use is highly encouraged and recommended for academic and scientific research, content analysis, sentiment analysis, and speech analysis. While it is free to use and modify, the responsibility for its use and any modifications lies with the user. Feel free to explore, utilize, and adapt the code to suit your needs, but please ensure you comply with Telegram's terms of service and data privacy regulations. This tool is released under a free and open-source license. When using or modifying the tool, please ensure to provide appropriate credit and citation. Referencing the tool in your research is appreciated and contributes to its continued development and improvement.
___

## Setup

### Just the first time:

Here you need to input your credentials like `username, phone, api_id and api_hash`. Your api_id and your api_hash, **it can be only generated from ([https://my.telegram.org/apps](https://my.telegram.org/apps))**. Once you set your details for the first time, you no longer need to update, just click play.

```python
# @title **1. [ Required ] Set up your credentials once** { display-mode: "form" }

# @markdown Here, you need to input your credentials: `username`, `phone`, `api_id`, and `api_hash`. Your `api_id` and `api_hash` can only be generated from [Telegram's app creation page](https://my.telegram.org/apps). Once your credentials are set up, you won’t need to update them again. Just click “Run” to proceed.

# Install the Telethon library for Telegram API interactions
!pip install -q telethon

# Initial imports
from datetime import datetime, timezone
import pandas as pd
import time
import json
import re

# Telegram imports
from telethon.sync import TelegramClient

# Google Colab imports
from google.colab import files

# Setup / change only the first time you use it
# @markdown **1.1.** Your Telegram account username (just 'abc123', not '@'):
username = 'your_username' # @param {type:"string"}
# @markdown **1.2.** Your Telegram account phone number (ex: '+5511999999999'):
phone = '+5511999999999' # @param {type:"string"}
# @markdown **1.3.** Your API ID, it can be only generated from https://my.telegram.org/apps:
api_id = '11111111' # @param {type:"string"}
# @markdown **1.4.** Your API hash, also from https://my.telegram.org/apps:
api_hash = '1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a' # @param {type:"string"}

```

### Scraping:

In this section, you will define the parameters for scraping data from Telegram channels or groups. Specify the channels you want to scrape using the format `@ChannelName` or the full URL `https://t.me/ChannelName`. Do not use URLs starting with `https://web.telegram.org/`. Set the date range by defining the start and end day, month, and year. Choose an output file name for the scraped data. Optionally, set a search keyword if you need to filter messages by specific terms. Define the maximum number of messages to scrape and set a timeout in seconds.

```python
# @title **2. [ Required ] Adjust every time you want to use it** { display-mode: "form" }

# @markdown In this section, you will define the parameters for scraping data from Telegram channels or groups. Specify the channels you want to scrape using the format `@ChannelName` or the full URL `https://t.me/ChannelName`. Do not use URLs starting with `https://web.telegram.org/`. Set the date range by defining the start and end day, month, and year. Choose an output file name for the scraped data. Optionally, set a search keyword if you need to filter messages by specific terms. Define the maximum number of messages to scrape and set a timeout in seconds.

# Setup / change every time to define scraping parameters

# @markdown **2.1.** Here you put the name of the channel or group that you want to scrape, as an example, play: '@LulanoTelegram' or 'https://t.me/LulanoTelegram'. Do not use: 'https://web.telegram.org/a/#-1001249230829' or '-1001249230829'. **Just write the `channel names` always separated by commas (,):**
channels = "@LulanoTelegram, @jairbolsonarobrasil, @Other_Channel_Name" # @param {type:"string"}
channels = [channel.strip() for channel in channels.split(",")]

# @markdown **2.2.** Here you can select the `time window` you would like to extract data from the listed communities:
date_min = '2024-10-15' # @param {type:"date"}
date_max = '2025-01-15' # @param {type:"date"}

date_min = datetime.fromisoformat(date_min).replace(tzinfo=timezone.utc)
date_max = datetime.fromisoformat(date_max).replace(tzinfo=timezone.utc)

# @markdown **2.3.** Choose a `name` for the final file you want to download as output:
file_name = 'Test' # @param {type:"string"}

# @markdown **2.4.** `Keyword` to search, **leave empty if you want to extract all messages from the channel(s):**
key_search = '' # @param {type:"string"}

# @markdown **2.5.** **Maximum** `number of messages` to scrape (only use if you want a specific limit, otherwise leave a high number to scrape everything):
max_t_index = 1000000   # @param {type:"integer"}

# @markdown **2.6.** `Timeout in seconds` (never leave it longer than 6 hours, that is 21600 seconds, as Google Colab deactivates itself after that time):
time_limit = 21600 # @param {type:"integer"}

# @markdown **2.7.** Choose the format of the final file you want to download. If you are a first-time user, choose `Excel`. If you have advanced skills, you can use `Parquet`:
File = 'excel' # @param ["excel", "parquet"]

```

### Done? You can run it!

___

## Run the code (5 easy steps! Just your first run!)

### Just the first time:

Once you press play on the code, it will ask you to enter your phone number:

#### **01.)** Call you to config your Telegram, put your phone number:

![image](https://user-images.githubusercontent.com/81989837/219951933-633bbb68-3c84-4176-8af3-db9124b82c00.png)

#### **02.)** You will recieve a code:

![image](https://user-images.githubusercontent.com/81989837/219951979-22735a77-ed8f-4b71-a45a-52ccb851cc01.png)

#### **03.)** Came back with your new code:

![image](https://user-images.githubusercontent.com/81989837/219952026-dcf4e1c6-8cc8-42cc-8c11-00632c5a3623.png)

#### **04.)** Put your password for your Telegram account:

![image](https://user-images.githubusercontent.com/81989837/219952063-180d2fef-4ae8-4a6a-9933-653814082e76.png)

#### **05.)** You will be notified that the Login was successful:

![image](https://user-images.githubusercontent.com/81989837/219952102-d7724867-236b-44d0-95b0-d7db3bf6e6d1.png)

![image](https://user-images.githubusercontent.com/81989837/219952296-3f1ea6b1-8534-4422-a40c-ebf8f9aab0cb.png)

___

### If you still logged in, the next time it runs, it will start here!

#### **01.)** The scraping will start from the parameters you entered earlier, note that it will also be updated in the panel:

![image](https://github.com/user-attachments/assets/d4894f30-7b2a-49c9-8b09-2be1bb963adc)

#### **02.)** For every 1,000 scraped contents, a backup file will be created, in case you want to download it:

![image](https://github.com/user-attachments/assets/a2f22108-c8a5-4622-930c-f3d0f803edcb)

### It's done!

#### **03.)** The output can be found as '.parquet' and transformed into Excel, for example:

![image](https://github.com/user-attachments/assets/b18c3c0e-8efc-49ab-bfac-4c525d4452b9)

___

## Author info:

Ergon Cugler de Moraes Silva, from Brazil, mailto: [contato@ergoncugler.com](contato@ergoncugler.com) / Founded Researcher at the Brazilian Institute of Information in Science and Technology (IBICT). Graduated in Public Policy Management (USP) and Postgraduate in Data Science & Analytics (USP) and Master in Public Administration and Government (FGV). More info at: [http://ergoncugler.com/](http://ergoncugler.com/).

___

## How to cite it:

**SILVA, Ergon Cugler de Moraes. *Web Scraping Telegram Posts and Content*. (feb) 2023. Avaliable at: [https://github.com/ergoncugler/web-scraping-telegram/](https://github.com/ergoncugler/web-scraping-telegram/).**
