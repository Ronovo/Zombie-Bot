import json
import helpers
import discord

async def begin(ctx, client):
    with open('users.json', 'r') as f:
        users = json.load(f)
    author = ctx.message.author

    player = await helpers.check_if_player(users, author)
    if player:
        await client.say("You have already created a character!")
    else:
        await client.say("Welcome! We will create your new character!")
        await client.say("What do you want to name your character?")
        userInput = await client.wait_for_message()
        name = userInput.content
        await create_player(users, author, name)
        await client.say("Welcome, %s" % name)
    await client.say("type z!character to see your character")
    await client.say("type z!join after you have assigned your attributes!")

    with open('users.json', 'w') as f:
        json.dump(users, f)


async def character(ctx, client):
    with open('users.json', 'r') as f:
        users = json.load(f)
    author = ctx.message.author
    embed = discord.Embed(
        colour=discord.Colour.orange()
    )
    embed.set_author(name=author)
    embed = await print_player(users, author, embed)
    await client.say(embed=embed)

async def set(ctx, attribute, direction, number, client):
    with open('users.json', 'r') as f:
        users = json.load(f)
    author = ctx.message.author
    ready = await helpers.ready(users, author)
    if ready:
        await client.say("No need to set attributes. Type z!Join to join the base")
    elif attribute == "":
        await client.say("Please put an attribute. Proper use: Z!set <attribute> <+/-> <number>")
    elif direction == "":
        await client.say("Please put an direction(+ or -). Proper use: Z!set <attribute> <+/-> <number>")
    elif number == 0 or type(number) != int:
        await client.say("Please enter a number. Proper use: Z!set <attribute> <+/-> <number>")
    else:
        await helpers.check_set_attribute(client, users, author, attribute, direction, number)
    with open('users.json', 'w') as f:
        json.dump(users, f)

async def delete(ctx, client):
    with open('users.json', 'r') as f:
        users = json.load(f)
    author = ctx.message.author
    users = await helpers.delete_character(users, author)
    with open('users.json', 'w') as f:
        json.dump(users, f)
    await client.say("Character has been deleted!")

# Outputs the Character Menu
async def print_character_menu():
    embed = discord.Embed(
        colour=discord.Colour.blue()
    )
    embed.add_field(name='Character Menu Commands', value="----", inline=False)
    embed.add_field(name='-z!begin', value="Character Creation. Start Here!", inline=False)
    embed.add_field(name='-z!character', value="Show Character Sheet", inline=False)
    embed.add_field(name='-z!set<attribute><+/-><number>', value="Example z!set s + 3", inline=False)
    embed.add_field(name='~z!join', value="Join Base when your character is ready!", inline=False)
    embed.add_field(name='~z!delete', value="Delete your character forever!", inline=False)
    return embed

# Outputs the Player Sheet.
async def print_player(users, user, embed):
    if user.id in users and users[user.id] != {}:
        embed.add_field(name='Name:', value=users[user.id]['name'])
        embed.add_field(name='Level:', value=users[user.id]['level'])
        embed.add_field(name='HP:', value=users[user.id]['hp'])
        embed.add_field(name='Kills:', value=users[user.id]['kills'])
        embed.add_field(name='-------------', value='Stats:', inline=False)
        embed.add_field(name='Agility:', value=users[user.id]['stats']['agility'], inline=False)
        embed.add_field(name='Charisma:', value=users[user.id]['stats']['charisma'], inline=False)
        embed.add_field(name='Strength:', value=users[user.id]['stats']['strength'], inline=False)
        embed.add_field(name='Intimidation:', value=users[user.id]['stats']['intimidation'], inline=False)
        embed.add_field(name='Tinkering:', value=users[user.id]['stats']['tinkering'], inline=False)
        embed.add_field(name='Exploration:', value=users[user.id]['stats']['exploration'], inline=False)

        embed.add_field(name='Kills:', value=users[user.id]['kills'])

    return embed

# method to initialize the character in the user json file
async def create_player(users, user, name):
    if user.id not in users or users[user.id] == {}:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 1
        users[user.id]['name'] = name
        users[user.id]['hp'] = 15
        users[user.id]['maxHp'] = 15
        users[user.id]['stats'] = {}
        users[user.id]['stats']['agility'] = 0
        users[user.id]['stats']['charisma'] = 0
        users[user.id]['stats']['strength'] = 0
        users[user.id]['stats']['intimidation'] = 0
        users[user.id]['stats']['tinkering'] = 0
        users[user.id]['stats']['exploration'] = 0
        users[user.id]['ready'] = "N"
        users[user.id]['kills'] = 0