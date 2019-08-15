import helpers
import charactermenu
import basemenu
import actionmenu
import json
import asyncio

from discord.ext import commands

testServerId = "525101619612745729"

TOKEN = ''
client = commands.Bot(command_prefix='t!')

'''async def check_for_attack():
    await client.wait_until_ready()
    while not client.is_closed:
        await helpers.checkForZombies(client, testServerId)
        await asyncio.sleep(60 * 15)'''


@client.event
async def on_ready():
    print('Bot Online')

@client.command(pass_context=True)
async def start(ctx):
    await helpers.menuStart(ctx,client)

@client.command(pass_context=True)
async def startMenu(ctx):
    await helpers.menuStart(ctx,client)

# ----------------------------------
# Character Commands
# ----------------------------------
@client.command(pass_context=True)
async def begin(ctx):
    await charactermenu.begin(ctx, client)


@client.command(pass_context=True)
async def character(ctx):
   await charactermenu.character(ctx, client)

@client.command(pass_context=True)
async def set(ctx, attribute="", direction="", number=0):
    await charactermenu.set(ctx, attribute, direction, number, client)

@client.command(pass_context=True)
async def delete(ctx):
    await charactermenu.delete(ctx, client)

# ----------------------------------
# Base Commands
# ----------------------------------

@client.command(pass_context=True)
async def join(ctx):
    await basemenu.join(ctx, client)

@client.command(pass_context=True)
async def roster(ctx):
    await basemenu.roster(ctx, client)

# ----------------------------------
# Commands
# ----------------------------------
@client.command(pass_context=True)
async def ready(ctx):
    await actionmenu.ready(ctx, client)

@client.command(pass_context=True)
async def status(ctx):
    await actionmenu.status(ctx, client)

# TODO : Make Bestiary File
@client.command(pass_context=True)
async def fight(ctx):
    with open('bases.json', 'r') as f:
        bases = json.load(f)

    if bases[testServerId]['defense']:
        await actionmenu.defend(ctx, client, bases)
    else:
        await actionmenu.fight(ctx, client)


@client.command(pass_context=True)
async def zombieAttack(ctx):
    await helpers.checkForZombies(client, testServerId)

#client.loop.create_task(check_for_attack())
client.run(TOKEN)
