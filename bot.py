#! /usr/bin/python3
import discord, os

TOKEN = os.environ.get('AUBOT_TOKEN')

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if(message.content == "!aubot"):
        return_message = "Hello! I'm AU Bot, and I hope to be actually useful!"
        await client.send_message(message.channel, return_message)

    if(message.content == "!roles"):
        server_roles = []
        for role in message.server.roles:
            if(role.name != "@everyone"):
                server_roles.append(role.name)
        return_message = ""
        if(len(server_roles) == 0):
            return_message = "There are currently no roles set on this server!"
        else:
            return_message = "The current roles for this server are: " + str(server_roles)
        await client.send_message(message.channel, return_message)

client.run(TOKEN)
