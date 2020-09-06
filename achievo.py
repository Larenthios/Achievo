#! /usr/bin/env python3
import configparser
import requests
import discord
from discord.ext import commands
import asyncio
import json

# colors = [0xe81717, 0xf9bd07, 0x6cf367, 0x159DC1]
config = configparser.ConfigParser()
config.read('config.ini')
steam_apikey = config['keys']['steam']
token = config['keys']['discord']
triggerchar='?'

bot = commands.Bot(command_prefix='?', description='Jean Plancher dans les pieds')

def get_player_id(name):
    steam_steamid = requests.get("http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=" + steam_apikey + "&vanityurl=" + name)
    parsed_json = json.loads(steam_steamid.text)
    return (parsed_json['response']['steamid'])

def get_game_id(name):
    all_app_list = requests.get("http://api.steampowered.com/ISteamApps/GetAppList/v2/")
    parsed_aal = json.loads(all_app_list.text)
    game_tab = parsed_aal['applist']['apps']
    for game in game_tab:
        if game['name'].lower().encode("ascii", "ignore").decode() == name.lower():
            return (game['appid'])

def get_achievement_stat(name, game):
    s = 0
    total = 0
    r = requests.get("http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=" + str(get_game_id(game)) + "&key=" + steam_apikey + "&steamid=" + str(get_player_id(name)))
    r = json.loads(r.text)
    print(r)
    print(r['playerstats'])
    gname = r['playerstats']['gameName']
    r = r['playerstats']['achievements']
    for d in r:
        s += d['achieved']
        total += 1
    output = ["Achievements for " + gname + " earned by " + name, str(s) + "/" + str(total)]
    return(output)

#Asynchronous tasks

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(name='newcmd', pass_context='true')
async def testcmd(ctx):
    await ctx.channel.send("c bn")

@bot.command(name='achievement', pass_context='true')
async def achievement(ctx, name, game):
    stat = get_achievement_stat(name, game)
    em = discord.Embed(title=stat[1], color=0x159DC1)
    em.set_author(name=stat[0], icon_url=bot.user.avatar_url)
    await ctx.channel.send(embed=em)

@bot.command(name='lmgtfy', pass_context='true')
async def lmgtfy(ctx, link):
    await ctx.channel.send('<http://lmgtfy.com/?q=' + link + '>')

@bot.command(name='ac_compare', pass_context='true')
async def ac_compare(ctx, name1, name2, game):
    await ctx.channel.send("processing...")
    stat1 = get_achievement_stat(name1, game)
    await ctx.channel.send("Done fetching first gamer's stats")
    stat2 = get_achievement_stat(name2, game)
    await ctx.channel.send("Done fetching second gamer's stats")
    em = discord.Embed(title="Achievements for " + game, color=0x159DC1)
    em.add_field(name=name1, value=stat1[1], inline=True)
    em.add_field(name=name2, value=stat2[1], inline=True)
    n1 = stat1[1].split('/')[0]
    n2 = stat2[1].split('/')[0]
    if n1 == n2:
        s = "You both have the same number of achievements"
    elif n1 > n2:
        s = tab[1]
    else:
        s = tab[2]
    em.add_field(name=s, value="a winner is you", inline=False)
    await ctx.channel.send(embed=em)

bot.run(token)