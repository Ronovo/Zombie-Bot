import discord
import random
import json
import basemenu
import charactermenu
import asyncio
import characterdao

# Used to check if the stat has already been set, during the set command
# Done after the attribute has already been determined
async def check_set_values(user, direction, number):
    flag = False
    if user.id in users:
        stats = users[user.id]['stats']
        for stat in stats:
            if direction == '+':
                if stats[stat] == number:
                    flag = True
                    break
            elif direction == '-':
                neg = 0 - number
                if stats[stat] == neg:
                    flag = True
                    break
    return flag




# method to set the author into the server roster.
# if the server hasn't been added to the bases file, it is initialized before the user
async def update_base(bases, user, server):
    if server.id not in bases or bases[server.id] == {}:
        create_base(bases, server)
        bases[server.id]['members'] = [user.id]
    else:
        bases[server.id]['members'].append(user.id)

async def create_base(bases, server):
    bases[server.id] = {}
    bases[server.id]['name'] = server.name
    bases[server.id]['defense'] = False
    bases[server.id]['members'] = []
    bases[server.id]['resources'] = {}
    bases[server.id]['resources']['food'] = 10
    bases[server.id]['resources']['water'] = 10
    bases[server.id]['resources']['medical'] = 2
    bases[server.id]['resources']['wood'] = 10
    bases[server.id]['resources']['stone'] = 10
    bases[server.id]['resources']['metal'] = 10

async def check_server_existance(server, bases):
    if server.id not in bases or bases[server.id] == {}:
        return False
    else:
        return True

# Outputs the contents of the base Information.
# Currently only includes a Roster and the name.
# Change to Embed when you change the player sheet below.
# Check why this is not working
async def print_main_menu(user):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(name=user)
        embed.add_field(name='Main Menu', value='---', inline=False)
        embed.add_field(name='1.) Character Menu', value='---', inline=False)
        embed.add_field(name='2.) Base Menu', value='---', inline=False)
        embed.add_field(name='3.) Action Menu', value='---', inline=False)
        embed.add_field(name='4.) Sign Out', value='---', inline=False)
        return embed

# Checks if player is in the user Id
# And that they have joined the base
# In order to do that, you need to set all attributes
# So that check is covered by base check
async def readyUp(users, user, bases, server):
    if user.id in users and users[user.id] != {} and bases[server.id]['members'] is not None:
        for member in bases[server.id]['members']:
            if member == user.id:
                users[user.id]['ready'] = 'Y'
                return users


async def readyStatus(users, user):
    if user.id in users and users[user.id] != {}:
        flag = users[user.id]['ready']
        return flag

async def rollDice(sides, number):
    total = 0
    for n in range(number):
        x = random.randint(1, sides)
        total += x
    return total

async def menuStart(ctx, client):
    author = ctx.message.author
    with open('users.json', 'r') as f:
        users = json.load(f)
    player = await check_if_player(users, author)
    if player:
        # main Menu
        await client.say("Welcome back!")
        leave = False
        while not leave:
            embed = await print_main_menu(author)
            await client.say(embed=embed)
            userInput = 0
            userInput = await client.wait_for_message()
            try:
                userInput = int(userInput.content)
            except ValueError:
                await client.say("That's not a number!!")
            if userInput == 1:
                embedChar = await charactermenu.print_character_menu()
                await client.say(embed=embedChar)
                leave = True
            elif userInput == 2:
                embedBase = await basemenu.print_base_menu()
                await client.say(embed=embedBase)
                leave = True
            elif userInput == 3:
                embedAction = await actionmenu.print_action_menu()
                await client.say(embed=embedBase)
                leave = True
            elif userInput == 4:
                await client.say("Goodbye!")
                leave = True
            else:
                await client.say("Please enter a valid number!")
        with open('users.json', 'w') as f:
            json.dump(users, f)
    else:
        await client.say("I see you are a new player!")
        await client.say("Type z!begin to start creating your character")

async def zombieAttack(client):
    testServer = client.get_server("525101619612745729")
    role = discord.utils.get(testServer.roles, name="Active Tester")
    atRole = str(role.mention)
    await client.send_message(discord.Object(id="525128557328859157"), "{}s, there is a zombie attacking the gate! Type z!fight to defend".format(atRole))

async def checkForZombies(client, testServerId):
    with open('bases.json', 'r') as f:
        bases = json.load(f)

    x = await rollDice(100, 1)
    print(str(x))
    if x >= 75:
        await zombieAttack(client)
        bases[testServerId]['defense'] = True
        with open('bases.json', 'w') as f:
            json.dump(bases, f)

        await asyncio.sleep(60 * 5)

        with open('bases.json', 'r') as f:
            bases = json.load(f)
        if bases[testServerId]['defense']:
            await zombieAttack(client)
        with open('bases.json', 'w') as f:
            json.dump(bases, f)

        await asyncio.sleep(60 * 5)

        if bases[testServerId]['defense']:
            await client.send_message(discord.Object(id="525128557328859157"), "Bad Things Go Here!")
    with open('bases.json', 'w') as f:
        json.dump(bases, f)

# TODO : Add success to player, so it can be modified
# TODO : Add damage to character
async def fight(users, user, enemy):
    pHp = users[user.id]['hp']
    pSuccess = 10
    zHp = enemy['hp']
    zSuccess = enemy['success']

    pHit = await rollDice(20, 1)
    zHit = await rollDice(20, 1)

    if pHit > pSuccess:
        zHp -= 5
    if zHit > zSuccess:
        pHp -= enemy['attack']

    enemy['hp'] = zHp
    users[user.id]['hp'] = pHp