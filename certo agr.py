import discord
from discord.ext import commands, tasks
from datetime import datetime

# Configurações
TOKEN = "MTM3NTI0MjYxNDY3MTkzMzQ1MA.G_Q0zE.7OK0VfJXJP4ZlZnXto3_WkHdEbVHQ4eOfXJGV0"
GUILD_ID = 1214986426886660167
CHANNEL_ID_CALL = 1375232770607026227  # Canal de "Em call"
CHANNEL_ID_MEMBROS = 1375232770607026228  # Novo canal: "Membros"

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=".gg/balalove"))
    atualizar_nome_canais.start()

@tasks.loop(seconds=30)
async def atualizar_nome_canais():
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("❌ Servidor não encontrado")
        return

    # Atualizar canal de voz "Em call"
    canal_call = guild.get_channel(1375232770607026227)
    if canal_call:
        total_em_chamada = sum(len(vc.members) for vc in guild.voice_channels)
        nome_call = f"🔊 Em call: {total_em_chamada}"
        try:
            if canal_call.name != nome_call:
                await canal_call.edit(name=nome_call)
                print(f"✅ Canal de call atualizado: {nome_call}")
        except Exception as e:
            print(f"❌ Erro ao atualizar canal de call: {e}")

    # Atualizar canal de membros humanos
    canal_membros = guild.get_channel(1375246531296497774)
    if canal_membros:
        total_humanos = sum(1 for m in guild.members if not m.bot)
        nome_membros = f"👥 Membros: {total_humanos}"
        try:
            if canal_membros.name != nome_membros:
                await canal_membros.edit(name=nome_membros)
                print(f"✅ Canal de membros atualizado: {nome_membros}")
        except Exception as e:
            print(f"❌ Erro ao atualizar canal de membros: {e}")

# COMANDOS PADRÕES

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Latência: {round(bot.latency * 1000)}ms")

@bot.command()
async def avatar(ctx, membro: discord.Member = None):
    membro = membro or ctx.author
    await ctx.send(membro.avatar.url)

@bot.command()
async def userinfo(ctx, membro: discord.Member = None):
    membro = membro or ctx.author
    embed = discord.Embed(title=f"Informações de {membro}", color=discord.Color.blue())
    embed.add_field(name="ID", value=membro.id)
    embed.add_field(name="Nome", value=str(membro))
    embed.add_field(name="Criado em", value=membro.created_at.strftime("%d/%m/%Y %H:%M"))
    embed.add_field(name="Entrou no servidor", value=membro.joined_at.strftime("%d/%m/%Y %H:%M"))
    embed.set_thumbnail(url=membro.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    servidor = ctx.guild
    embed = discord.Embed(title=f"Informações do servidor {servidor.name}", color=discord.Color.green())
    embed.add_field(name="ID", value=servidor.id)
    embed.add_field(name="Dono", value=str(servidor.owner))
    embed.add_field(name="Membros", value=servidor.member_count)
    embed.add_field(name="Criado em", value=servidor.created_at.strftime("%d/%m/%Y"))
    embed.set_thumbnail(url=servidor.icon.url if servidor.icon else None)
    await ctx.send(embed=embed)

@bot.command()
async def say(ctx, *, texto):
    await ctx.message.delete()
    await ctx.send(texto)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, quantidade: int = 5):
    await ctx.channel.purge(limit=quantidade + 1)
    msg = await ctx.send(f"🧹 {quantidade} mensagens apagadas.")
    await msg.delete(delay=3)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, membro: discord.Member, *, motivo="Sem motivo"):
    await membro.ban(reason=motivo)
    await ctx.send(f"🔨 {membro} foi banido. Motivo: {motivo}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, membro: discord.Member, *, motivo="Sem motivo"):
    await membro.kick(reason=motivo)
    await ctx.send(f"👢 {membro} foi expulso. Motivo: {motivo}")

# Rodar bot
bot.run(TOKEN)
