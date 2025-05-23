import discord
from discord.ext import commands, tasks
from datetime import datetime

# === Configuration ===
TOKEN = "MTM3NTI0MjYxNDY3MTkzMzQ1MA.G_Q0zE.7OK0VfJXJP4ZlZnXto3_WkHdEbVHQ4eOfXJGV0"
GUILD_ID = 1214986426886660167
CHANNEL_ID_CALL = 1375232770607026227  # "In Call" voice channel
CHANNEL_ID_MEMBERS = 1375246531296497774  # "Members" count channel

# === Intents ===
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# === Events ===
@bot.event
async def on_ready():
    print(f"✅ Bot connected as {bot.user}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=".gg/balalove"))
    update_channel_names.start()

# === Loop: Update Channel Names ===
@tasks.loop(seconds=30)
async def update_channel_names():
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("❌ Server not found")
        return

    # Update "In Call" channel
    call_channel = guild.get_channel(CHANNEL_ID_CALL)
    if call_channel:
        total_in_call = sum(len(vc.members) for vc in guild.voice_channels)
        call_name = f"🔊 In Call: {total_in_call}"
        try:
            if call_channel.name != call_name:
                await call_channel.edit(name=call_name)
                print(f"✅ Call channel updated: {call_name}")
        except Exception as e:
            print(f"❌ Error updating call channel: {e}")

    # Update "Members" channel
    member_channel = guild.get_channel(CHANNEL_ID_MEMBERS)
    if member_channel:
        total_humans = sum(1 for m in guild.members if not m.bot)
        member_name = f"👥 Members: {total_humans}"
        try:
            if member_channel.name != member_name:
                await member_channel.edit(name=member_name)
                print(f"✅ Member count channel updated: {member_name}")
        except Exception as e:
            print(f"❌ Error updating member count channel: {e}")

# === Commands ===

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Latency: {round(bot.latency * 1000)}ms")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(member.avatar.url)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"User Info - {member}", color=discord.Color.blue())
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Name", value=str(member))
    embed.add_field(name="Account Created", value=member.created_at.strftime("%d/%m/%Y %H:%M"))
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%d/%m/%Y %H:%M"))
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    embed = discord.Embed(title=f"Server Info - {server.name}", color=discord.Color.green())
    embed.add_field(name="ID", value=server.id)
    embed.add_field(name="Owner", value=str(server.owner))
    embed.add_field(name="Members", value=server.member_count)
    embed.add_field(name="Created On", value=server.created_at.strftime("%d/%m/%Y"))
    embed.set_thumbnail(url=server.icon.url if server.icon else None)
    await ctx.send(embed=embed)

@bot.command()
async def say(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(text)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 Cleared {amount} messages.")
    await msg.delete(delay=3)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member} has been banned. Reason: {reason}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member} has been kicked. Reason: {reason}")

# === Run Bot ===
bot.run(TOKEN)
