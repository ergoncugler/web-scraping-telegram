# initial imports
from datetime import datetime, timezone
import time
import asyncio
import pandas as pd
from telethon.sync import TelegramClient

# setup / change only the first time you use it
username = 'Felipe Antunes'  # here you put your username from your telegram account
phone = '+5521981022053'  # here you put your phone number from your telegram account
api_id = '20916318'  # here you put your api_id from https://my.telegram.org/apps
api_hash = '9bb1551e4a5f08b2f836e7332fcf9994'  # here you put your api_hash from https://my.telegram.org/apps
data = []
url = ''
index = 1

# setup / change every time to use to define scraping
channel = '@jairbolsonarobrasil'  # here you put the name of the channel or group that you want to scrap (ex: '@jairbolsonarobrasil' or 'https://t.me/jairbolsonarobrasil/' / not: 'https://web.telegram.org/z/#-1273465589' or '-1273465589')
d_min = 1  # start day / this date will be included
m_min = 1  # start month
y_min = 2023  # start year
d_max = 2  # final day / only the day before this date will be included, that is, this date will not be included
m_max = 1  # final month
y_max = 2023  # final year
key_search = ''  # only if you want to search a keyword, if not, keep as ''

# scraping
async def main():
    async with TelegramClient(username, api_id, api_hash) as client:
        index = 1
        data = []
        async for message in client.iter_messages(channel, search=key_search):
            if message.date < datetime(y_max, m_max, d_max, tzinfo=timezone.utc) and message.date > datetime(y_min, m_min, d_min, tzinfo=timezone.utc):
                
                # if there is media
                if message.media:
                    url = f'https://t.me/{channel}/{message.id}'.replace('@', '')
                else:
                    url = 'no media'

                if message.reactions is None:
                    emoji_string = ""
                else:
                    emoji_string = ""
                    for reaction_count in message.reactions.results:
                        emoji = reaction_count.reaction.emoticon
                        count = str(reaction_count.count)
                        emoji_string += emoji + " " + count + " "

                conteudo = [f'#ID{index:05}', channel, message.sender_id, message.text, message.date.strftime('%Y-%m-%d %H:%M:%S'), message.id, message.post_author, message.views, emoji_string, message.forwards, url]

                comments = []
                try:
                    async for comment in client.iter_messages(channel, reply_to=message.id):
                        comments.append(comment.text)
                except:
                    comments = ['possible adjustment']
                comments = ', '.join(comments).replace(', ', ';\n')

                conteudo.append(comments)
                
                data.append(conteudo)

                print(f'Item {index:05} completed!')
                print(f'Id: {message.id:05}.\n')
                print(conteudo)

                index = index + 1
                time.sleep(1)
        
       
        columns = ['Scraping ID', 'Group', 'Author ID', 'Content', 'Date', 'Message ID', 'Author', 'Views', 'Reactions', 'Shares', 'Media', 'Comments']
        df = pd.DataFrame(data, columns=columns)
        
        # Saving DataFrame to JSON
        df.to_json('telegram_scraping_results.json', orient='records', lines=True)
        print('Data saved to telegram_scraping_results.json')


asyncio.run(main())
