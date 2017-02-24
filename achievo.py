#! /usr/bin/env python3
import configparser
import requests
import discord
import asyncio
import json
import logging

logging.basicConfig(level=logging.DEBUG)

client = discord.Client()
triggerchar = '?'
config = configparser.ConfigParser()
config.read('config.ini')
steam_apikey = config['keys']['steam']
token = config['keys']['discord']

def get_player_id(name):
    steam_steamid = requests.get("http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=" + steam_apikey + "&vanityurl=" + name)
    parsed_json = json.loads(steam_steamid.text)
    return (parsed_json['response']['steamid'])

def get_game_id(name):
    all_app_list = requests.get("http://api.steampowered.com/ISteamApps/GetAppList/v2/")
    parsed_aal = json.loads(all_app_list.text)
    game_tab = parsed_aal['applist']['apps']
    for game in game_tab:
        if game['name'].lower() == game_name.lower():
            return (game['appid'])

def get_achievement_stat(name, game):
    s = 0
    total = 0
    r = requests.get("http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=" + str(get_game_id(game)) + "&key=" + steam_apikey + "&steamid=" + str(get_player_id(name)))
    r = json.loads(r.text)
    gname = r['playerstats']['gameName']
    r = r['playerstats']['achievements']
    for d in r:
        s += d['achieved']
        total += 1
    output = "Achievements for " + gname + " earned by " + name + ": \n " + str(s) + "/" + str(total)
    return(output)

#Asynchronous tasks

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event # should be [.achievement, name, game]
async def on_message(message):
    if message.content.startswith(triggerchar + 'achievement'):
        osef, name, game = message.content.split()
        output = get_achievement_stat(name, game)
        logging.debug(output)
        await client.send_message(message.channel, output)

# @client.event
# async def on_message(message):
#     if message.content.startswith(triggerchar + 'kikimeter'):
#         osef, name1, name2, game = message.content.split() # should be [.achievement, name1, name2, game]
#         name = get_player_id(name)
#         game = "374320"#get_game_id(game)
#         r = requests.get("http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=" + game + "&key=" + steam_apikey + "&steamid=" + name)
#         await client.send_message(message.channel, r.body)

@client.event
async def on_message(message):
    if message.content.startswith(triggerchar + 'help'):
        await client.send_message(message.channel, 'Je dispose de 20.000 Dataris.')

client.run(token)
