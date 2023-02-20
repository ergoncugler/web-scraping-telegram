# initial imports
from datetime import datetime, timezone
from datetime import datetime as dt
import time

# telegram imports
from telethon.sync import TelegramClient

# google imports
from google.colab import auth
auth.authenticate_user()
import gspread
from google.auth import default
creds, _ = default()
autoriza = gspread.authorize(creds)

# setup / change only the first time you use it
username = 'username' # here you put your username from your telegram account
phone = '+5511999999999'  # here you put your phone number from your telegram account
api_id = '12345678' # here you put your api_id from https://my.telegram.org/apps
api_hash = '12ab12ab12ab12ab12ab12ab12ab12ab' # here you put your api_hash from https://my.telegram.org/apps
data = []
url = ''
index = 1

# setup / change every time to use to define scraping
channel = '@jairbolsonarobrasil' # here you put the name of the channel or group that you want to scrap (ex: '@jairbolsonarobrasil' or 'https://t.me/jairbolsonarobrasil/' / not: 'https://web.telegram.org/z/#-1273465589' or '-1273465589')
worksheet_name = 'Telegram Teste' # here you put the name of the file you want as output, it will create a file on your google drive home screen
d_min = 1 # start day / this date will be included
m_min = 1 # start month
y_min = 2019 # start year
d_max = 1 # final day / only the day before this date will be included, that is, this date will not be included
m_max = 1 # final month
y_max = 2023 # final year
key_search = '' # only if you want to search a keyword, if not, keep as ''

# ----- #

# try to open the worksheet in your google drive
try:
    sheet = autoriza.open(worksheet_name).sheet1
    # the spreadsheet already exists, you don't need to create another one
except gspread.exceptions.SpreadsheetNotFound:
    # the spreadsheet does not exist yet, create a new one
    sh = autoriza.create(worksheet_name)
sheet = autoriza.open(worksheet_name).sheet1
# clear the worksheet completely before filling
sheet.clear()
# defines titles and workspace
titulos = ['Scraping ID','Group','Author ID', 'Content', 'Date', 'Message ID', 'Author', 'Views', 'Reactions', 'Shares', 'Media', 'Comments']
campos = sheet.range('A1:L1')
for i in range(0, len(campos)):
  campos[i].value = titulos[i]
sheet.update_cells(campos)

# scraping
async with TelegramClient(username, api_id, api_hash) as client:
  async for message in client.iter_messages(channel, search=key_search):
    if message.date < datetime(y_max, m_max, d_max, tzinfo=timezone.utc) and message.date > datetime(y_min, m_min, d_min, tzinfo=timezone.utc):

      # if there is media
      if message.media:
        url = f'https://t.me/{channel}/{message.id}'.replace('@', '')
      else:
        url = 'no media'

      # if there are reactions
      if message.reactions == None:
        pass
      else:
        emoji_string = ""
        for reaction_count in message.reactions.results:
          emoji = reaction_count.reaction.emoticon
          count = str(reaction_count.count)
          emoji_string += emoji + " " + count + " "

      # content condensation
      conteudo = [f'#ID{index:05}', channel, message.sender_id, message.text, message.date.strftime('%Y-%m-%d %H:%M:%S'), message.id, message.post_author, message.views, emoji_string, message.forwards, url]

      # if there are comments # important to come after the content list with append following it, so as not to confuse the 'message' and collect only the contents of the comments
      comments = []
      try:
        async for message in client.iter_messages(channel, reply_to=message.id):
          comments.append(message.text)
      except:
        comments = ['possible adjustment']
      comments = ', '.join(comments).replace(', ', ';\n')

      # append of the content with the comments
      conteudo.append(comments)

      # spreadsheet on google
      registros = sheet.range(f"A{index+1}:L{index+1}")
      for i in range(0,len(registros)):
        registros[i].value = conteudo[i]
      sheet.update_cells(registros)

      # updates the progress counter
      print(f'Item {index:05} completed!')
      print(f'Id: {message.id:05}.\n')

      # update loop parameters
      index = index + 1
      time.sleep(1)

# end
print(f'----------------------------------------\n#Concluded! #{index-1:05} posts were scraped!\n----------------------------------------\n\n\n\n')
