import discord
from discord.ext import commands
import csv
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

invite_links = {}

def load_invite_roles():
    data = {}
    with open("invite_roles.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[row["invite"]] = row["role"]
    return data

invite_roles = load_invite_roles()

@bot.event
async def on_ready():
    print(f"BOT 已上線 {bot.user}")

    for guild in bot.guilds:
        invites = await guild.invites()
        invite_links[guild.id] = invites

@bot.event
async def on_member_join(member):

    guild = member.guild
    new_invites = await guild.invites()
    old_invites = invite_links[guild.id]

    for invite in new_invites:
        for old in old_invites:

            if invite.code == old.code and invite.uses > old.uses:

                if invite.code in invite_roles:

                    role_name = invite_roles[invite.code]

                    role = discord.utils.get(guild.roles, name=role_name)

                    if role:
                        await member.add_roles(role)

    invite_links[guild.id] = new_invites

bot.run(os.getenv(""TOKEN""))
