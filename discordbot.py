import coc

from riotwatcher import LolWatcher, ApiError

import discord
from discord.ext import commands

import json

with open(".auth") as f:
    auth = f.readlines()
auth = [x.strip() for x in auth]

clan_tag = auth[4] # Tag of the clan that you want to follow.
coc_client = coc.login(auth[0], auth[1], key_count=5, key_names="Bot key", client=coc.EventsClient)

watcher = LolWatcher(auth[5])

bot = commands.Bot(command_prefix="!")
INFO_CHANNEL_ID = int(auth[2])

@coc_client.event
async def on_clan_member_versus_trophies_change(old_trophies, new_trophies, player):
	await bot.get_channel(INFO_CHANNEL_ID).send(
        "{0.name}-nek jelenleg {1} versus trófeája van".format(player, new_trophies))

@bot.command()
async def parancsok(ctx):
    await ctx.send("!parancsok, !role \{player_tag\}, !tagok, !lol_euw \{summoner_name\}, !lol_eune \{summoner_name\}")

@bot.command()
async def role(ctx, player_tag):
    player = await coc_client.get_player(player_tag)

    to_send = "{} role-ja a klánban: {}".format(player.name, player.role)

    await ctx.send(to_send)

@bot.command()
async def tagok(ctx):
    members = await coc_client.get_members(clan_tag)

    to_send = "A tagok:\n"
    for player in members:
        to_send += "{0} ({1})\n".format(player.name, player.tag)

    await ctx.send(to_send)

lol_format = "Summoner name: {}, level: {}"

@bot.command()
async def lol_euw(ctx, summoner_name):
    summoner = json.loads(watcher.summoner.by_name('euw1', summoner_name))

    to_send = lol_format.format(summoner.name, summoner.summonerLevel)

    await ctx.send(to_send)

@bot.command()
async def lol_eune(ctx, summoner_name):
    summoner = watcher.summoner.by_name('eun1', summoner_name)
    
    to_send = lol_format.format(summoner.name, summoner.summonerLevel) 
    
    await ctx.send(to_send)


coc_client.add_clan_update(
    [clan_tag], retry_interval=60
)
coc_client.start_updates()

bot.run(auth[3])