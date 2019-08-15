import json
import helpers
import discord

async def join(ctx, client):
    with open('users.json', 'r') as f:
        users = json.load(f)
    with open('bases.json', 'r') as f:
        bases = json.load(f)
    author = ctx.message.author
    server = ctx.message.server
    ready = await helpers.ready(users, author)
    baseExists = await helpers.check_server_existance(server, bases)
    if not baseExists:
        await helpers.create_base(bases, server)
    if ready:
        await client.say("Welcome to the land of Discord Zombies!")
        await client.say("Type y to confirm joining the %s base" % server.name)
        x = await client.wait_for_message()
        x = x.content

        if x.lower() == "y":
            await helpers.update_base(bases, author, server)
        else:
            await client.say("Please try again!")

        with open('bases.json', 'w') as f:
            json.dump(bases, f)
        await client.say("Congrats! You have joined the roster!")
    else:
        await client.say("You are not ready yet! Assign your attributes! Go Back to the Character Menu!")

async def roster(ctx, client):
    with open('bases.json', 'r') as f:
        bases = json.load(f)
    author = ctx.message.author
    server = ctx.message.server
    embed = await print_base(bases, author, server)
    await client.say(embed=embed)

# Outputs the Character Menu
async def print_base_menu():
    embed = discord.Embed(
        colour=discord.Colour.blue()
    )
    embed.add_field(name='Base Menu Commands', value="----", inline=False)
    embed.add_field(name='-z!join', value="Join Base after Character Creation", inline=False)
    embed.add_field(name='-z!roster', value="Show Character Sheet", inline=False)
    return embed

# Outputs the contents of the base Information.
# Currently only includes a Roster and the name.
# Change to Embed when you change the player sheet below.
# Check why this is not working
async def print_base(bases, user, server):
    if server.id in bases or bases[server.id] != {}:
        embed = discord.Embed(
            colour=discord.Colour.red()
        )
        embed.set_author(name=user)
        embed.add_field(name='Name:', value=bases[server.id]['name'])
        embed.add_field(name='Members:', value='-------------', inline=False)
        userList = bases[server.id]['members']
        for member in userList:
            x = server.get_member(member)
            embed.add_field(name=x.name, value=x.top_role, inline=False)
        return embed