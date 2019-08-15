import discord
import random
import json
import basemenu
import charactermenu

# Used to check if the stat has already been set, during the set command
# Done after the attribute has already been determined
async def check_set_values(users, user, direction, number):
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


# checks if player is in the users list already
async def check_if_player(users, user):
    if user.id not in users:
        return False
    elif users[user.id] == {}:
        return False
    else:
        return True


# checks if uses is ready to join the server base
async def ready(users, user):
    flag = await check_if_player(users, user)
    if user.id in users:
        stats = users[user.id]['stats']
        for stat in stats:
            if stats[stat] == 0:
                flag = False
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


# Determines which attribute was input, and calls set_attribute below.
# Also will hold attribute specific logic. For example, Strength Hitpoint Modifier
async def check_set_attribute(client, users, user, attribute, direction, number):
    if user.id in users and users[user.id] != {}:
        flag = False
        if attribute.lower() == "agility" or attribute.lower() == "a":
            flag = await set_attribute(client, users, user, "agility", direction, number)
            if flag:
                await client.say("Agility set to %s%s" % (direction, number))
        elif attribute.lower() == "charisma" or attribute.lower() == "c":
            flag = await set_attribute(client, users, user, "charisma", direction, number)
            if flag:
                await client.say("Charisma set to %s%s" % (direction, number))
        elif attribute.lower() == "strength" or attribute.lower() == "s":
            flag = await set_attribute(client, users, user, "strength", direction, number)
            hp = users[user.id]['hp']
            s = users[user.id]['stats']['strength']
            await modify_hp_str(users, user, hp, s)
            if flag:
                await client.say("Strength set to %s%s" % (direction, number))
        elif attribute.lower() == "intimidation" or attribute.lower() == "i":
            flag = await set_attribute(client, users, user, "intimidation", direction, number)
            if flag:
                await client.say("Intimidation set to %s%s" % (direction, number))
        elif attribute.lower() == "tinkering" or attribute.lower() == "t":
            flag = await set_attribute(client, users, user, "tinkering", direction, number)
            if flag:
                await client.say("Tinkering set to %s%s" % (direction, number))
        elif attribute.lower() == "exploration" or attribute.lower() == "e":
            flag = await set_attribute(client, users, user, "exploration", direction, number)
            if flag:
                await client.say("Exploration set to %s%s" % (direction, number))
        else:
            await client.say("Please enter a valid attribute!")


# Set's the attribute.
# Calls check_set_values to make sure that the number has not already been used in the character sheet
async def set_attribute(client, users, user, attribute, direction, number):
    x = users[user.id]['stats'][attribute]
    used = await check_set_values(users, user, direction, number)
    if x != 0:
        await client.say("This attribute has already been set")
    elif not number < 4:
        await client.say("Please enter a number 3 or less")
    elif used:
        await client.say("That number has been used already")
    else:
        if direction == "+":
            x += number
            users[user.id]['stats'][attribute] = x
            return True
        elif direction == "-":
            x -= number
            users[user.id]['stats'][attribute] = x
            return True
        else:
            await client.say("Please enter a valid direction(+ or -)")


# Removes Character from the users.json
# TODO : need to remove from base if they are in a base as well.
async def delete_character(users, user):
    if user.id in users and users[user.id] != {}:
        users[user.id] = {}
        return users


'''
HP Values for Strength Modifiers
Base HP is 15
+3 = 21
+2 = 19
....
-3 = -6
'''
async def modify_hp_str(users, user, hp, s):
    s *= 2
    hp += s
    users[user.id]['hp'] = hp
    users[user.id]['maxHp'] = hp

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