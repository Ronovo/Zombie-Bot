import json
import helpers
import characterdao
import discord

async def begin(ctx, client):
    author = ctx.message.author

    player = await characterdao.check_if_player(author)
    if player:
        await client.say("You have already created a character!")
    else:
        await client.say("Welcome! We will create your new character!")
        await client.say("What do you want to name your character?")
        userInput = await client.wait_for_message()
        name = userInput.content
        await characterdao.create_player(author, name)
        await client.say("Welcome, %s" % name)
    await client.say("type z!character to see your character")
    await client.say("type z!join after you have assigned your attributes!")


async def character(ctx, client):
    author = ctx.message.author
    embed = discord.Embed(
        colour=discord.Colour.orange()
    )
    embed.set_author(name=author)
    embed = await characterdao.print_player(author, embed)
    await client.say(embed=embed)

async def set(ctx, attribute, direction, number, client):
    author = ctx.message.author
    ready = await characterdao.ready(author)
    if ready:
        await client.say("No need to set attributes. Type z!Join to join the base")
    elif attribute == "":
        await client.say("Please put an attribute. Proper use: Z!set <attribute> <+/-> <number>")
    elif direction == "":
        await client.say("Please put an direction(+ or -). Proper use: Z!set <attribute> <+/-> <number>")
    elif number == 0 or type(number) != int:
        await client.say("Please enter a number. Proper use: Z!set <attribute> <+/-> <number>")
    else:
        await check_set_attribute(client, author, attribute, direction, number)

async def delete(ctx, client):
    author = ctx.message.author
    users = await characterdao.delete_character(author)
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

# Determines which attribute was input, and calls set_attribute below.
# Also will hold attribute specific logic. For example, Strength Hitpoint Modifier
async def check_set_attribute(client, user, attribute, direction, number):
    flag = False
    if attribute.lower() == "agility" or attribute.lower() == "a":
        flag = await characterdao.set_attribute(client, user, "AGILITY", direction, number)
        if flag:
            await client.say("Agility set to %s%s" % (direction, number))
    elif attribute.lower() == "charisma" or attribute.lower() == "c":
        flag = await characterdao.set_attribute(client, user, "CHARISMA", direction, number)
        if flag:
            await client.say("Charisma set to %s%s" % (direction, number))
    elif attribute.lower() == "strength" or attribute.lower() == "s":
        flag = await characterdao.set_attribute(client, user, "STRENGTH", direction, number)
        await characterdao.modify_hp_str(user)
        if flag:
            await client.say("Strength set to %s%s" % (direction, number))
    elif attribute.lower() == "intimidation" or attribute.lower() == "i":
        flag = await characterdao.set_attribute(client, user, "INTIMIDATION", direction, number)
        if flag:
            await client.say("Intimidation set to %s%s" % (direction, number))
    elif attribute.lower() == "tinkering" or attribute.lower() == "t":
        flag = await characterdao.set_attribute(client, user, "TINKERING", direction, number)
        if flag:
            await client.say("Tinkering set to %s%s" % (direction, number))
    elif attribute.lower() == "exploration" or attribute.lower() == "e":
        flag = await characterdao.set_attribute(client, user, "EXPLORATION", direction, number)
        if flag:
            await client.say("Exploration set to %s%s" % (direction, number))
    else:
        await client.say("Please enter a valid attribute!")