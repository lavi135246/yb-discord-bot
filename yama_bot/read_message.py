import os
import numpy as np
import asyncio

from discord.ext import commands

token = os.getenv("DISCORD_TOKEN")
my_guild = os.getenv("DISCORD_GUILD")

# intents = discord.Intents.default()
# client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='yb ')


def set_check_user(userid: str):
    name, discriminator = userid.split("#")

    def check(message):
        return (message.author.name == name and
                message.author.discriminator == discriminator)
    return check


@client.command(
    name="delete", pass_context=True,
    help="Delete number of messages from user. "
    "(e.g. yb delete 10 AAAAA#1357)"
    )
@commands.has_permissions(manage_roles=True)
async def delete(ctx, number: int, userid: str = None):
    if userid is None:
        return
    elif userid == "all":
        print(f"Deleting {number} of messages.")
        await ctx.channel.purge(limit=int(number))
    else:
        print(f"Deleting {number} of messages. From {userid}")
        check_func = set_check_user(userid=userid)
        await ctx.channel.purge(limit=int(number), check=check_func)


# @client.command(
#     name="purge", pass_context=True,
#     help="Purge every message from a user."
# )
# @commands.has_permissions(manage_roles=True)
# async def purge(ctx, number: int, userid: str = None):
#     if userid is None:
#         return
#     else:
#         print(f"Deleting {number} of messages. From {userid}")
#         check_func = set_check_user(userid=userid)

#         msg_list = []
#         async for m in ctx.channel.history(limit=number):

#             if check_func(m):
#                 msg_list.append(m)

#             if len(msg_list) == 100:
#                 await ctx.channel.delete_messages(msg_list)
#                 print("100 msg deleted")
#                 msg_list.clear()
#                 await asyncio.sleep(1.2)


@client.command(
    name="random", pass_context=True,
    help="Generate random number in givin range."
    "(e.g. yb random 10)"
    )
async def random_number(ctx, number: int):
    n = np.random.randint(number) + 1
    result = f"Number {n}"
    await ctx.channel.send(result)


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == my_guild:
            break

    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if "唱歌" in msg and "我" in msg and "不" not in msg and "沒有":
        response = "<@&860526805504491560>"
        await asyncio.sleep(1)
        await message.channel.send(response)

    if "沒人" in msg and "我" in msg and "不" not in msg:
        comfort_strs = [
            "沒事的，雖然我能做的不多，但是不管你說什麼我都會認真聆聽 ：）",
            "我在呢 (*´ω`)人(´ω`*) ",
            "我不許你這樣說自己 (`д´)"
        ]
        response = np.random.choice(comfort_strs)
        await asyncio.sleep(1)
        await message.channel.send(response)

    await client.process_commands(message)

client.run(token)
