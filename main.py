import discord #connect to Discord
import os # used for $ecrets (shhhh) 
import requests # allows the code to make a HTTP request
import json # handler for returned json data from the request
import random # random selector
import datetime # 
import pandas as pd
from replit import db # uses the replit database


# we will use 3 quote API's for this bot
# https://zenquotes.io/ - a bit of rancho relaxo
# https://apizen.date/ - something that happened today
# https://www.weatherapi.com/  - current temp

client = discord.Client()
sad_words = ["sad", "unhappy", "covid", "lockdown", "miserable", "depressed", "dissapointed", "depressing", "flat"]
starter_encouragements = [
  "I might be a robot, but you are awesome!", 
  "There's light at the end of the tunnel you know!",
  "Don't forget you are awesome",
  "Hang in there",
  "Keep your chin up!",
  "Don’t give up.",
  "Good things take time, keep at it and you'll succeed",
  "Cheer up! Rome wasn't built in a day",
  "You can do it, I have faith in you.",
  "Never give up.",
  "You are a gigantic bottle of awesomesauce!",
  "Come on! You can do it!",
]

def get_quote():
  response = requests.get ("https://zenquotes.io/api/random") #get the quote
  json_data  = json.loads(response.text) #retrieve json
  quote = json_data[0]['q'] + " -" + json_data[0]['a'] #concatenates a string with the quote and the author
  return (quote)

def get_on_this_day():
  now = datetime.datetime.now()
  response = requests.get ("https://byabbe.se/on-this-day" + str(now.month) + "/" + str(now.day) + "/births.json") #get the data from on this day
  json_otd  = json.loads(response.text) #retrieve json
  #on_this_day = json_otd['Events']['text'] #returns the event
  return (json_otd)




def get_temp(temp_city):
  response = requests.get ("http://api.weatherapi.com/v1/current.json?key=" + os.environ['weather_key'] + "&q=" + temp_city + "&aqi=no")
  json_temp  = json.loads(response.text) #retrieve json
  # format string for current temp & convert floats to strings 
  temp = "Weather for " + json_temp['location']['name'] + " currently is " + str(json_temp['current']['temp_c']) + " degrees celcius and feels like " + str(json_temp['current']['feelslike_c']) + ". Wind is from the " + json_temp['current']['wind_dir'] + " and blowing at " + str(json_temp['current']['wind_kph']) + " Kph. We've had " +  str(json_temp['current']['precip_mm']) + " mm of rain today" 
  return (temp)


def get_airtable():
  
  base_id = os.environ['AT_base']
  table_name = "Plan"
  url = "https://api.airtable.com/v0/" + base_id + "/" + table_name

  api_key = os.environ['AT_key']
  params = ()
  headers = {"Authorization" : "Bearer {}".format(api_key),
              'Content-Type': 'application/json'}
  response = requests.get(url, params=params, headers=headers)
  airtable_response = response.json()
  airtable_records = airtable_response['records']
  

  #deadline = "Next deadline is " + json_deadline['Name'] 
  return (airtable_records)

def convert_to_dataframe(airtable_records):
    """Converts dictionary output from airtable_download() into a Pandas dataframe."""
    airtable_rows = []
    airtable_index = []
    for record in airtable_records:
        airtable_rows.append(record['fields'])
       # airtable_index.append(record['id'])
    airtable_dataframe = pd.DataFrame(airtable_rows) #, index=airtable_index)
    return airtable_dataframe




@client.event
async def on_ready():
  print('Situation normal. We have logged in as {0.user}'.format(client)) #jus confirms who teh bot is logged in as


@client.event
async def on_message(message):
  if message.author == client.user:
    return # Do nothing if the mesage is from the bot itself

  if message.content.startswith('Hey Sven') or message.content.startswith('hey sven'):
     await message.channel.send('Sup young person? \n Here''s a list of things I can do for you. If you type -  \n quote - I''ll give you a quote of the day \n schedule - will grab the latest schedule for an activity like a hackathon \n temp - then a city name like ''temp melbourne'' where i''m from give you the current temperature \n I also jump in and offer encouragement if I think you are feeling a little down')

  msg=message.content # just creates shorthand for the variable for easier coding

  if msg.startswith('quote'):
    quote = get_quote()
    await message.channel.send(quote)    

  if msg.startswith('otd'):
    otd = get_on_this_day()
    await message.channel.send(otd)      

  if msg.startswith('schedule'):
    airtable_records = get_airtable() #get the data from airtable
    airtable_dataframe = convert_to_dataframe(airtable_records) #make it purdy
    await message.channel.send(airtable_dataframe)     
    
  

  if msg.startswith('temp'):
    temp_city = msg.split("temp ",1)[1] #split out the command from the name of the city
    temp = get_temp(temp_city)
    await message.channel.send(temp)

  options = starter_encouragements
  if "encouragements" in db.keys():
       options = options + db["encouragements"][:]

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))

      
#run the bot
client.run(os.environ['token'])