import os
import discord
import requests
import json
from replit import db
from random import randint
from discord.ext import commands
from webserver import keep_alive
import pyshorteners




my_secret = os.environ['token2']
api_key = os.environ['api']

#setting the prefix to #
client = commands.Bot(command_prefix='#')


#fetching gifs from giphy
def fetch(query):
    try:
        url = 'https://api.giphy.com/v1/gifs/search?q=' + query + '&api_key=' + api_key
        response = requests.get(url)
        r = response.json()
        index = randint(0, 30)
        gif_url = r['data'][index]['url']
        return gif_url, True
    except Exception as e:
        url = 'https://api.giphy.com/v1/gifs/search?q=notfound' + '&api_key=' + api_key
        response = requests.get(url)
        r = response.json()
        index = randint(0, 2)
        gif_url = r['data'][index]['url']
        return gif_url, False


#fetching definition from dictionnary api
def fetch_definition(word):
    try:
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
        data = requests.get(url)
        r = data.json()
        definition = r[0]['meanings'][0]['definitions'][0]['definition']
        return definition, True
    except Exception as e:
        return 'no meaning', False


#fetching pronouciation from dictionnary api
def fetch_pronouciation(word):
    try:
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
        data = requests.get(url)
        r = data.json()
        audio = r[0]['phonetics'][0]['audio']
        return audio, True
    except Exception as e:
        return 'no audio', False

#url shortner 

def shorten(url):
    try:
      s = pyshorteners.Shortener()
      short_url = s.tinyurl.short(url)
      return short_url
    except Exception :
       return 'Ooooops! could not shorten this URL'
    

#building our main programm


@client.event
async def on_ready():
   
    print('we logged in as {0.user}'.format(client))


#get a gif
@client.command()
async def gif(ctx, args):
    gif, found = fetch(args)
    if found:
        await ctx.send(gif)
    else:
        await ctx.send("Oooops! found no gifs")
        await ctx.send(gif)


#define a word
@client.command()
async def define(ctx, args):
    definition, found = fetch_definition(args)
    if found:
        await ctx.send(args + " : " + definition)
    else:
        await ctx.send("Oooops! found no definition")


#return link to a correct pronouciation
@client.command()
async def audio(ctx, args):
    pronouciation, found = fetch_pronouciation(args)
    if found:
        await ctx.send("find pronounciation here : http:" + pronouciation)
    else:
        await ctx.send("Oooops! found no pronouciation")


#count members
@client.command()
async def count(ctx):
    bots = [m for m in ctx.guild.members if m.bot]
    #number of bot members
    number_of_bots = len(bots)

    await ctx.send(ctx.guild.member_count - number_of_bots)

#shorten url
@client.command()
async def short(ctx,args):
     url = shorten(args)
     await ctx.send(url)
#adding commands

#match score alerts

keep_alive()
client.run(my_secret)
