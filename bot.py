import discord
import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

# Funções #

# Função para pickar um agente aleatório por role #
def pick_random_agent(role):
  controladores = ['Astra', 'Brimstone', 'Omen', 'Viper']
  duelistas = ['Jett', 'Phoenix', 'Raze', 'Reyna', 'Yoru']
  iniciadores = ['Breach', 'Skye', 'Sova']
  sentinelas = ['Cypher', 'Killjoy', 'Sage']

  if role == 'controlador':
    return random.choice(controladores)
  elif role == 'duelista':
    return random.choice(duelistas)
  elif role == 'iniciador':
    return random.choice(iniciadores)
  elif role == 'sentinela':
    return random.choice(sentinelas)
  else:
    return

# Bot conectado no Discord #
@bot.event
async def on_ready():
  print(f'{bot.user.name} has connected to Discord!')

# Bot recepciona novo membro #
@bot.event
async def on_member_join(self, member):
  guild = member.guild
  if guild.system_channel is not None:
    to_send = 'Bem-vindo {0.mention} ao server {1.name}!'.format(member, guild)
    await guild.system_channel.send(to_send)

# Comandos do Bot #

# Bot manda um salve #
@bot.command( 
  help='Mandamos um salve pra tu'
)
async def salve(ctx):
  user = ctx.author
  await ctx.send(f'Salve, {user.name} :call_me:')

# Bot picka um agente aleatório pra você dada uma role #
@bot.command(
  help='Escolheremos um agente para você (ex.: !pick duelista)'
)
async def pick(ctx, role):
  user = ctx.author
  agent = pick_random_agent(role)

  await ctx.send(f'{user.name} vai de {agent} :handshake:')

# Bot cria um squad de n players precisando apenas passar a role do agente #
@bot.command(
  help='Montamos seu squad maneiro'
)
async def squad(ctx, players: int, name: str):
    await ctx.send(f'Squad {name} criada, adicione {players} pessoas:')

    def check(m):
      return m.content == 'controlador' or m.content == 'duelista' or m.content == 'iniciador' or m.content == 'sentinela'
    
    players_agents = []

    for i in range(players):
      msg = await bot.wait_for('message', check=check)
      agent = pick_random_agent(msg.content) 
      if i < players - 1:
        await ctx.send(f'Faltam {players - i - 1} players...')
        players_agents.append(f'{msg.author.name} vai de {agent}.')
      else: 
        players_agents.append(f'{msg.author.name} vai de {agent}.')
        await ctx.send('Squad completo!')
    
    for player_agent in players_agents:
      await ctx.send(player_agent)
    await ctx.send('Bom jogo rapaziada :handshake:')

bot.run(TOKEN)