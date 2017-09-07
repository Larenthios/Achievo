#! /usr/bin/env python3
import configparser
import requests
import discord
import asyncio
import json

# colors = [0xe81717, 0xf9bd07, 0x6cf367, 0x159DC1]
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
        if game['name'].lower() == name.lower():
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
    output = ["Achievements for " + gname + " earned by " + name, str(s) + "/" + str(total)]
    return(output)

#Asynchronous tasks

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith(triggerchar + 'achievement'):
        tab = message.content.split()
        name = tab[1]
        game = ' '.join(tab[2:])
        stat = get_achievement_stat(name, game)
        em = discord.Embed(title=stat[1], color=0x159DC1)
        em.set_author(name=stat[0], icon_url=client.user.avatar_url)
        await client.send_message(message.channel, embed=em)
    elif message.content == (triggerchar + 'help'):
        await client.send_message(message.channel, "Commands: ?achievement steam_name steam_game")
    elif message.content == 'alors':
        await client.send_message(message.channel, ',')
    elif message.content.startswith(triggerchar + 'lmgtfy'):
        await client.send_message(message.channel, '<http://lmgtfy.com/?q=' + message.content.split()[1] + '>')
    elif message.content == 'mmmh' or message.content == '🤔' or message.content == 'émoticône penseur':
        await client.add_reaction(message, '🤔')
    elif message.content.startswith(triggerchar + 'kikimeter'):
        tab = message.content.split() # should be [.achievement, name1, name2, game]
        game = ' '.join(tab[3:])
        stat1 = get_achievement_stat(tab[1], game)
        stat2 = get_achievement_stat(tab[2], game)
        em = discord.Embed(title="Achievements for " + game, color=0x159DC1)
        em.add_field(name=tab[1], value=stat1[1], inline=True)
        em.add_field(name=tab[2], value=stat2[1], inline=True)
        n1 = stat1[1].split('/')[0]
        n2 = stat2[1].split('/')[0]
        if n1 == n2:
            s = "You both have the same number of achievements"
        elif n1 > n2:
            s = tab[1]
        else:
            s = tab[2]
        em.add_field(name=s, value="a winner is you", inline=False)
        await client.send_message(message.channel, embed=em)

client.run(token)
