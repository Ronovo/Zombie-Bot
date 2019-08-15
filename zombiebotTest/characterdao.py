import sqlite3
import helpers


async def create_player(user, name):
    conn = sqlite3.connect('test.db')
    print("Opened database successfully")
    # Create New Character
    conn.execute('INSERT INTO CHARACTER (EXPERIENCE,LEVEL,NAME,HP,MAXHP,AGILITY,CHARISMA,STRENGTH,'
                 'INTIMIDATION, TINKERING, EXPLORATION,READY,KILLS)'
                 'VALUES (0, 1, ?, 15, 15, 0, 0, 0, 0, 0, 0,"N",0)', (name,))

    conn.commit()

    # Search for new Character created to get rowID
    cursor = conn.execute('SELECT rowid FROM CHARACTER WHERE NAME = ?', (name,))
    for row in cursor:
        # Link Character to User
        conn.execute('INSERT INTO USER (USERID,CHARACTER) VALUES (?,?)', (user.id, row[0]))

    conn.commit()
    print("Records created successfully")
    conn.close()


async def check_if_player(user):
    # Search for new Character created to get rowID
    conn = sqlite3.connect('test.db')
    print("Opened database successfully")
    cursor = conn.execute('SELECT * FROM USER WHERE USERID = ?', (user.id,))
    isPlayer = False
    if cursor.fetchone() is not None:
        isPlayer = True
    else:
        conn.close()
        return False
    if c.fetchall() is None or c.fetchall() == 0:
        isPlayer = False
    conn.close()
    return isPlayer


async def get_character(user):
    conn = sqlite3.connect('test.db')
    # Get Character ID
    cursor = conn.execute('SELECT CHARACTER FROM USER WHERE USERID = ?', (user.id,))
    cid = ''
    for row in cursor:
        cid = row[0]
    # Get Character Info
    cursor = conn.execute('SELECT * FROM CHARACTER WHERE rowid = ?', (cid,))
    row = cursor.fetchone()
    conn.close()
    return row


async def get_attribute(character, attribute):
    value = 0
    # Get Character Info
    if attribute == "AGILITY":
        value = character[5]
    elif attribute == "CHARISMA":
        value = character[6]
    elif attribute == "STRENGTH":
        value = character[7]
    elif attribute == "INTIMIDATION":
        value = character[8]
    elif attribute == "TINKERING":
        value = character[9]
    elif attribute == "EXPLORATION":
        value = character[10]
    return value


async def update_attribute(user, attribute, number):
    conn = sqlite3.connect('test.db')
    # Get Character ID
    cursor = conn.execute('SELECT CHARACTER FROM USER WHERE USERID = ?', (user.id,))
    cid = ''
    for row in cursor:
        cid = row[0]
    # Update Character Info
    # Dynamic won't work. did it statically to finish it
    # Refactor might be in order
    if attribute == "AGILITY":
        conn.execute("UPDATE CHARACTER SET AGILITY=? WHERE rowid = ?", (number, cid))
    elif attribute == "CHARISMA":
        conn.execute("UPDATE CHARACTER SET CHARISMA=? WHERE rowid = ?", (number, cid))
    elif attribute == "STRENGTH":
        conn.execute("UPDATE CHARACTER SET STRENGTH=? WHERE rowid = ?", (number, cid))
    elif attribute == "INTIMIDATION":
        conn.execute("UPDATE CHARACTER SET INTIMIDATION=? WHERE rowid = ?", (number, cid))
    elif attribute == "TINKERING":
        conn.execute("UPDATE CHARACTER SET TINKERING=? WHERE rowid = ?", (number, cid))
    elif attribute == "EXPLORATION":
        conn.execute("UPDATE CHARACTER SET EXPLORATION=? WHERE rowid = ?", (number, cid))
    conn.commit()
    conn.close()

async def delete_character(user):
    conn = sqlite3.connect('test.db')
    # Get Character ID
    cursor = conn.execute('SELECT CHARACTER FROM USER WHERE USERID = ?', (user.id,))
    cid = ''
    for row in cursor:
        cid = row[0]
    conn.execute("DELETE from CHARACTER where rowid = ?", (cid,))
    conn.execute("UPDATE USER SET CHARACTER=0 WHERE CHARACTER = ?", (cid,))
    conn.commit()
    conn.close()


async def print_player(user, embed):
    row = await get_character(user)
    embed.add_field(name='Name:', value=row[2])
    embed.add_field(name='Level:', value=row[1])
    embed.add_field(name='HP:', value=row[3])
    embed.add_field(name='Kills:', value=row[12])
    embed.add_field(name='-------------', value='Stats:', inline=False)
    embed.add_field(name='Agility:', value=row[5], inline=False)
    embed.add_field(name='Charisma:', value=row[6], inline=False)
    embed.add_field(name='Strength:', value=row[7], inline=False)
    embed.add_field(name='Intimidation:', value=row[8], inline=False)
    embed.add_field(name='Tinkering:', value=row[9], inline=False)
    embed.add_field(name='Exploration:', value=row[10], inline=False)
    return embed


async def ready(user):
    flag = await check_if_player(user)
    if flag:
        row = await get_character(user)
        if row[5] == 0 or row[6] == 0 or row[7] == 0 or row[8] == 0 or row[9] == 0 or row[10] == 0:
            flag = False
    return flag


# Set's the attribute.
# Calls check_set_values to make sure that the number has not already been used in the character sheet
async def set_attribute(client, user, attribute, direction, number):
    conn = sqlite3.connect('test.db')
    # Get Character ID
    character = await get_character(user)
    used = await check_set_values(character, direction, number)
    result = await get_attribute(character, attribute)
    if result != 0:
        await client.say("This attribute has already been set")
    elif not number < 4:
        await client.say("Please enter a number 3 or less")
    elif used:
        await client.say("That number has been used already")
    else:
        if direction == "+":
            await update_attribute(user, attribute, number)
            conn.commit()
            conn.close()
            return True
        elif direction == "-":
            number = 0 - number
            await update_attribute(user, attribute, number)
            conn.commit()
            conn.close()
            return True
        else:
            await client.say("Please enter a valid direction(+ or -)")


async def check_set_values(character, direction, number):
    flag = False
    x = 5
    while x < 11:
        if direction == "+":
            if character[x] == number:
                flag = True
                break
        elif direction == '-':
            neg = 0 - number
            if character[x] == neg:
                flag = True
                break
        x += 1
    return flag


'''
HP Values for Strength Modifiers
Base HP is 15
+3 = 21
+2 = 19
....
-3 = -6
'''
async def modify_hp_str(user):
    conn = sqlite3.connect('test.db')
    # Get Character ID
    character = await get_character(user)
    s = character[7]
    hp = character[3]
    s *= 2
    hp += s
    # Update Character Info
    cursor = conn.execute('SELECT CHARACTER FROM USER WHERE USERID = ?', (user.id,))
    cid = ''
    for row in cursor:
        cid = row[0]
    conn.execute('UPDATE CHARACTER set MAXHP = ?, HP = ? WHERE rowid = ?', (hp, hp, cid,))
    conn.commit()
    conn.close()