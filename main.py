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
  "Don’t give up.",
  "Keep pushing.",
  "Keep fighting!",
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

def update_encouragements (encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"] # get the values stored in the database currently to the variable encouragements 
    encouragements.append(encouraging_message) #append the new message to teh variable
    db["encouragements"] = encouragements #write teh whole thing back to the DB
  else: #if there is no database yet to write values
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index): #deletes encouraging messages
  encouragements = db["encouragements"] #get a list of messages from the DB
  if len(encouragements) > index: #check if the length is more than the index
    del encouragements[index] # delete the index
    db["encouragements"] = encouragements  #save the database


def get_temp():
  response = requests.get ("http://api.weatherapi.com/v1/current.json?key=" + os.environ['weather_key'] + "&q=Melbourne&aqi=no")
  json_temp  = json.loads(response.text) #retrieve json
  # format string for current temp & convert floats to strings 
  temp = "Weather for " + json_temp['location']['name'] + " currently is " + str(json_temp['current']['temp_c']) + " degrees celcius and feels like " + str(json_temp['current']['feelslike_c']) + ". Wind is from the " + json_temp['current']['wind_dir'] + " and blowing at " + str(json_temp['current']['wind_kph']) + " Kph. We've had " +  str(json_temp['current']['precip_mm']) + " mm of rain today" 
  return (temp)


def get_deadline():
  
  base_id = os.environ['AT_base']
  table_name = "Plan"
  url = "https://api.airtable.com/v0/" + base_id + "/" + table_name

  api_key = os.environ['AT_key']
  params = ()
    #headers = {“Authorization" : "Bearer ” + os.environ['AT_key']}
  headers = {"Authorization" : "Bearer {}".format(api_key),
              'Content-Type': 'application/json'}

  response = requests.get(url, params=params, headers=headers)
  airtable_response = response.json()
  deadline = airtable_response['records']
  

  #deadline = "Next deadline is " + json_deadline['Name'] 
  return (deadline)






@client.event
async def on_ready():
  print('Situation normal. We have logged in as {0.user}'.format(client)) #jus confirms who teh bot is logged in as


@client.event
async def on_message(message):
  if message.author == client.user:
    return # Do nothing if the mesage is from the bot itself

  if message.content.startswith('Hey Sven'):
     await message.channel.send('Hello there young person! I do not have my list of things I can do ready yet as my awsomeness is still being developed. But at least the HEX team was nice enough to put this message here')

  msg=message.content # just creates shorthand for the variable for easier coding

  if msg.startswith('quote'):
    quote = get_quote()
    await message.channel.send(quote)    

  if msg.startswith('deadline'):
    deadline = get_deadline()
    await message.channel.send(deadline)     
   

  if msg.startswith('temp'):
    temp = get_temp()
    await message.channel.send(temp)

  options = starter_encouragements
  if "encouragements" in db.keys():
    # options = options + db["encouragements"]
    # options.extend(db["encouragements"])
    # options = options + list(db["encouragements"])
    #options = options.extend(db[“encouragements”])
    options = options + db["encouragements"][:]




  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))

  if msg.startswith('$new'):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added!")

  if msg.startswith("$del"):
    encouragements = [] #creates an empty list
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1]) #split the comment from the phrase in Discord
      delete_encouragements(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
    
#run the bot
client.run(os.environ['token'])