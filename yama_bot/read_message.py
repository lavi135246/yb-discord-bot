import os
import random

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


@client.command(
    name="random", pass_context=True,
    help="Generate random number in givin range."
    "(e.g. yb random 10)"
    )
async def random_number(ctx, number: int):
    n = random.randint(1, number + 1)
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
        await message.channel.send(response)

    await client.process_commands(message)

client.run(token)
