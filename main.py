import discord
from discord.ext import commands
import requests
from keep_alive import keep_alive
import asyncio
from datetime import datetime
from replit import db

db['sent'] = False
db['msg_id'] = 0

client = commands.Bot(command_prefix = '%') # Instantiate a discord client

@client.event # Getting the bot ready
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name = "LoFi Radio in the"
                                                                                                     " LoFi Lounge"))
  print('You have logged in as {0.user}'.format(client))
  await sendprice()

# Function for our logic & embed we'll be using. Sending the embed then updating in chat every 5 mins
async def sendprice():
  dt_string = datetime.now().strftime("%m/%d/%Y %H:%M:%S") # # Store & format current GMT time

  # Requests data from the Coingecko API
  URL ='https://api.coingecko.com/api/v3/simple/price?ids=blockchain-adventurers-guild&vs_currencies=usd'
  data = requests.get(url=URL).json()
  price = data['blockchain-adventurers-guild']['usd']
  channel = client.get_channel(ID)

  # Embed starts
  embed = discord.Embed(
    title = f'**BAG Price**',
    description = 'Updated every five minutes',
    colour = discord.Color.from_rgb(255, 51, 204)
  )

  # All of the text fields & images for the embed
  embed.set_thumbnail(url='https://assets.coingecko.com/coins/images/14863/small/3iw7MAi.png?1618810870')
  embed.add_field(name='Price:', value=f'${price}', inline=False)
  embed.add_field(name="BAG on Coingecko:", 
                  value=f'[coingecko](https://www.coingecko.com/en/coins/blockchain-adventure'
                        f'rs-guild?__cf_chl_jschl_tk__=92_IPlKTDONz87G1t_oHkAR3B7rjTtWVHPkJn_'
                        f'YEBoo-1641283101-0-gaNycGzNCNE)', inline=False)
  
  embed.add_field(name='Last Updated:', value=f'{dt_string} GMT', inline=False)
  embed.set_footer(text='Blockchain Adventurers Guild',
                   icon_url='https://cdn.discordapp.com/icons/825651993816727603/'
                   'e2da84a02a7e521811136a1bf5ac8390.webp?size=96')

  # -------------------------------------------------------------------------------------------
  # First time sending embed and updating logic
  # -------------------------------------------------------------------------------------------

  if db['sent'] == False:
    msg = await channel.send(embed=embed) # Send embed to channel
    db['msg_id'] = msg.id # Store in Replit db
    db['sent'] = True
    await asyncio.sleep(300)
    await sendprice()
  else:  # When the bot is rebooted, don't spam the chat
    msg = db['msg_id']
    msg = await channel.fetch_message(msg)
    await msg.edit(embed=embed) # Edit msg in channel
    await asyncio.sleep(300)
    await sendprice()
    
keep_alive()
client.run(TOKEN)
