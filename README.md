# Web Scraping Telegram Posts and Content

This code aims to **scrape data** from selected Telegram Channels, Groups or Chats through the Telethon Library, also integrating Google's Gspread Library **and printing the results in a Google Spreadsheet in real time**.

In summary, it is possible to set **'Periods' (date), 'Keywords' (search) and 'ID' (Channels, Groups or Chats)** to scrape all the desired content, returning: **'Scraping ID', 'Group', 'Author ID', 'Content', 'Date ', 'Message ID', 'Author', 'Views', 'Reactions', 'Shares', 'Media', 'Comments'**.

To avoid impacts from code breaks during the scraping process, it was decided **to insert each scraped content into the spreadsheet, one by one**, instead of scraping them all and, only at the end, resulting in output to a spreadsheet.

### Output Example:
It was asked to scrape Jair Bolsonaro's Channel from Telegram between january 1st 2019 and january 1st 2023, then it returned 5241 posts:
![image](https://user-images.githubusercontent.com/81989837/219953529-959d6f15-8f9b-4b4c-b010-91def95b73f6.png)

___

## !Pip Before Coding

```python
pip install telethon
```
```python
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

___

## Setup the Code

### Just First Time:

***Attention: If you don't have the necessary credentials, you can create it for free on the official Telegram for Developers website: https://my.telegram.org/apps. There you can get your 'api_id' and 'api-hash'.***

```python
# setup / change only the first time you use it
username = 'username' # here you put your username from your telegram account
phone = '+5511999999999'  # here you put your phone number from your telegram account
api_id = '12345678' # here you put your api_id from https://my.telegram.org/apps
api_hash = '12ab12ab12ab12ab12ab12ab12ab12ab' # here you put your api_hash from https://my.telegram.org/apps
```

### To Scrape:

```python
# setup / change every time to use to define scraping
channel = '@jairbolsonarobrasil' # here you put the name of the channel or group that you want to scrap (ex: '@jairbolsonarobrasil' or 'https://t.me/jairbolsonarobrasil/' / not: 'https://web.telegram.org/z/#-1273465589' or '-1273465589')
worksheet_name = 'Telegram Teste' # here you put the name of the file you want as output, it will create a file on your google drive home screen
d_min = 1 # start day / this date will be included
m_min = 1 # start month
y_min = 2022 # start year
d_max = 2 # final day / only the day before this date will be included, that is, this date will not be included
m_max = 1 # final month
y_max = 2022 # final year
key_search = '' # only if you want to search a keyword, if not, keep as ''
```

### Done? You can run it!

___

## Run the Code (10 easy steps! Just your first run!)

### Just First Time:

**01.)** It should ask you 'allow this laptop to access your Google credentials?' This will allow code running on this notebook to access your Google Drive and Google Cloud data. Review the code before allowing access. Put ir 'Allow':

![image](https://user-images.githubusercontent.com/81989837/219951620-9f939108-2660-4965-8744-e8429cd867fb.png)

**02.)** Choose an account to proceed to Collaboratory Runtimes. To continue, Google will share your name, email address, preferred language, and profile picture with the Collaboratory Runtimes app. Please review the Collaboratory Runtimes app's Privacy Policy and Terms of Service before using it:

![image](https://user-images.githubusercontent.com/81989837/219951831-c2ff8a85-7076-414f-8a5a-aadd8f59ad99.jpg)

**03.)** Then it'll call you to config your Telegram, put your phone number:

![image](https://user-images.githubusercontent.com/81989837/219951933-633bbb68-3c84-4176-8af3-db9124b82c00.png)

**04.)** You will recieve a code:

![image](https://user-images.githubusercontent.com/81989837/219951979-22735a77-ed8f-4b71-a45a-52ccb851cc01.png)

**05.)** Came back with your new code:

![image](https://user-images.githubusercontent.com/81989837/219952026-dcf4e1c6-8cc8-42cc-8c11-00632c5a3623.png)

**06.)** Put your password for your Telegram account:

![image](https://user-images.githubusercontent.com/81989837/219952063-180d2fef-4ae8-4a6a-9933-653814082e76.png)

**07.)** You will be notified that the Login was successful:

![image](https://user-images.githubusercontent.com/81989837/219952102-d7724867-236b-44d0-95b0-d7db3bf6e6d1.png)

![image](https://user-images.githubusercontent.com/81989837/219952296-3f1ea6b1-8534-4422-a40c-ebf8f9aab0cb.png)

### The next time it runs, it will start here!

**08.)** The scraping will start from the parameters you entered earlier, note that it will also be updated in the panel:

![image](https://user-images.githubusercontent.com/81989837/219954277-918f0d60-6447-4fba-a39c-e6d1c8430ad3.png)

**09.)** Your file will be automatically generated on the homepage of your logged in Google Drive:

![image](https://user-images.githubusercontent.com/81989837/219953050-1733a9fd-8228-4873-92bc-168f2199f9d8.png)

**10.)** At the end, you will receive a message of how many messages were scraped, based on the loop performed:

![image](https://user-images.githubusercontent.com/81989837/219954193-90c754ad-7a18-4c91-a94f-e7dcc33b5cb9.png)

### It's done!

The output can be found in this format:

![image](https://user-images.githubusercontent.com/81989837/219954132-a164007c-b18f-4ad9-a37b-ebbdc511ad60.png)

___

## Author Info:

Ergon Cugler de Moraes Silva, from Brazil, mailto: <a href="contato@ergoncugler.com">contato@ergoncugler.com</a>
</br>Master's Program in Public Administration and Government, Getulio Vargas Foundation (FGV)
</br>Funded Researcher by the National Council for Scientific and Technological Development (CNPq)
