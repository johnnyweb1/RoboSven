import discord #connect to Discord
import os # used for $ecrets (shhhh) 
import requests # allows the code to make a HTTP request
import json # handler for returned json data from the request
import random # random selector
from replit import db # uses the replit database


# we will use 3 quote API's for this bot
# https://zenquotes.io/ - a bit of rancho relaxo
# https://apizen.date/ - something that happened today
# https://www.weatherapi.com/  - current temp

client = discord.Client()
sad_words = ["sad", "unhappy", "covid", "lockdown", "miserable", "depressed", "dissapointed", "depressing", "flat"]
starter_encouragements = [
  "Cheer up!", 
  "There's light at the end of the tunnel you know!",
  "Don't forget you are awesome",
  "Hang in there",
  "Keep your chin up!",
  "Hang in there.",
  "Don’t give up.",
  "Keep pushing.",
  "Keep fighting!",
  "Stay strong.",
  "Never give up.",
  "Never say ‘die’.",
  "Come on! You can do it!",
]

def get_quote():
  response = requests.get ("https://zenquotes.io/api/random") #get the quote
  json_data  = json.loads(response.text) #retrieve json
  quote = json_data[0]['q'] + " -" + json_data[0]['a'] #concatenates a string with the quote and the author
  return (quote)

def update_encouragements (encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements]
    encouragements.apend(encouraging_message)
    db[]

def get_temp():
  response = requests.get ("http://api.weatherapi.com/v1/current.json?key=" + os.environ['weather_key'] + "&q=Melbourne&aqi=no")
  json_temp  = json.loads(response.text) #retrieve json
  # format string for current temp & convert floats to strings 
  temp = "Weather for " + json_temp['location']['name'] + " currently is " + str(json_temp['current']['temp_c']) + " degrees celcius and feels like " + str(json_temp['current']['feelslike_c']) + ". Wind is from the " + json_temp['current']['wind_dir'] + " and blowing at " + str(json_temp['current']['wind_kph']) + " Kph. We've had " +  str(json_temp['current']['precip_mm']) + " mm of rain today" 
  return (temp)



@client.event
async def on_ready():
  print('Situation normal. We have logged in as {0.user}'.format(client)) #jus confirms who teh bot is logged in as


@client.event
async def on_message(message):
  if message.author == client.user:
    return # Do nothing if the mesage is from the bot itself

  if message.content.startswith('Hey Sven'):
     await message.channel.send('Hello there young person!')

  msg=message.content # just creates shorthand for the variable for easier coding

  if msg.startswith('quote'):
    quote = get_quote()
    await message.channel.send(quote)    

  if msg.startswith('temp'):
    temp = get_temp()
    await message.channel.send(temp)

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))

#run the bot
client.run(os.environ['token'])