import json
import helpers
import discord

async def ready(ctx, client):
    with open('users.json', 'r') as f:
        users = json.load(f)
    with open('bases.json', 'r') as f:
        bases = json.load(f)
    author = ctx.message.author
    server = ctx.message.server
    await client.say("You are about to ready up. This will put your character in danger.")
    await client.say("Are you ready? Type Y to continue.")
    await client.say("Type anything else to cancel.")
    x = await client.wait_for_message()
    x = x.content
    if x.lower() == "y":
        users = await helpers.readyUp(users, author, bases, server)
        with open('users.json', 'w') as f:
            json.dump(users, f)
        await client.say("You are now ready. You will be notified when you are attacked!")
    else:
        await client.say("Type z!ready when you are ready to battle.")

async def status(ctx, client):
    with open('users.json', 'r') as f:
        users = json.load(f)

    author = ctx.message.author
    ready = await helpers.readyStatus(users, author)
    if ready == 'Y':
        await client.say("You are ready! You will be notified if you are attacked!")
    else:
        await client.say("You are not ready. Use z!ready to ready up")


# TODO : Make Bestiary File
async def fight(ctx, client):
    with open('users.json', 'r') as f:
        users = json.load(f)

    zombie = {'hp': 10, 'attack': 3, 'success': 12}
    author = ctx.message.author
    dead = False
    round = 1
    while not dead:
        embed = discord.Embed(
            colour=discord.Colour.orange()
        )
        embed.set_author(name=author)
        embed.add_field(name='"Combat Round:', value=round)

        await helpers.fight(users, author, zombie)

        zHp = zombie['hp']
        pHp = users[author.id]['hp']

        embed.add_field(name='Your HP:', value=pHp, inline=False)
        embed.add_field(name='Zombie HP:', value=zHp, inline=False)
        round += 1
        if zHp <= 0:
            dead = True
            kill = users[author.id]['kills']
            kill += 1
            users[author.id]['kills'] = kill
            embed.add_field(name='You Beat the Zombie!!!', value="Your Zombie Count is now %s" % kill, inline=False)
        elif pHp <= 0:
            dead = True
            embed.add_field(name='The zombie has eaten you!', value="You must start over!",
                            inline=False)
            await helpers.delete_character(users, author)
            await client.say("Your character has been deleted")
        await client.say(embed=embed)
        await client.say("Type anything to continue")
        x = await client.wait_for_message()
    with open('users.json', 'w') as f:
        json.dump(users, f)

# Outputs the Character Menu
async def print_action_menu():
    embed = discord.Embed(
        colour=discord.Colour.blue()
    )
    embed.add_field(name='Action Menu Commands', value="----", inline=False)
    embed.add_field(name='-z!ready', value="Become active in the base", inline=False)
    embed.add_field(name='-z!status', value="Provides Ready Status", inline=False)
    embed.add_field(name='-z!fight', value="Fight Zombies", inline=False)
    return embed
