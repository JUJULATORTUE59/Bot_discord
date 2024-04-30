import discord
from discord.ext import commands
from flask import Flask, request
import requests

TOKEN = "repalce token"

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

# Commande pour afficher la liste des commandes du bot
@bot.command()
async def command(ctx):
    embed = discord.Embed(title="Bot Commands", description="Liste des commandes du bot.", color=0x0000FF)
    embed.add_field(name="/members", value="Liste les membres du serveur, rôle, nom.", inline=False)
    embed.add_field(name="/ping", value="Le bot répond pong suivis de l'émojie.", inline=False)
    embed.add_field(name="/touché", value="Le bot répond coulé.", inline=False)
    embed.add_field(name="/joke", value="Donne une blague aléatoire de l'api https://icanhazdadjoke.com/.", inline=False)
    embed.add_field(name="/welcome", value="Dit bienvenue à une personne spécifiée", inline=False)
    embed.add_field(name="bonjour", value="Le bot detecte le mot le mot bonjour et répond .", inline=False)
    embed.add_field(name="bannis", value="Le bot bannis l'utilisateur avec le mot bannis.", inline=False)
    await ctx.send(embed=embed)

# Événement déclenché lorsque le bot est prêt
@bot.event
async def on_ready():
    print(f"{bot.user.name} le bot est prêt à l'emploi")

# Commande ping-pong
@bot.command()
async def ping(ctx):
    await ctx.send(f"pong :ping_pong:")

# Commande touché
@bot.command()
async def touché(ctx):
    await ctx.send(f"coulé :sweat_drops:")  

# Commande pour afficher la liste des membres du serveur
@bot.command()
async def members(ctx):
    members = ctx.guild.members
    member_list = [] # Création d'un tableau pour récupérer les listes

    # Parcours de la liste pour afficher les noms de chaque membre
    for member in members:
        roles = [role.name for role in member.roles]
        member_list.append(f"{member.display_name} - {' | '.join(roles)}")
    
    await ctx.send("Liste des membres sur le serveur:\n" + "\n".join(member_list))   

# Commande pour obtenir une blague aléatoire
@bot.command()
async def joke(ctx):
    joke_text = get_random_joke()
    await ctx.send(joke_text)

# Fonction pour obtenir une blague aléatoire depuis l'API
def get_random_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['joke']
    else:
        return "Aucune blague trouvée :("

# Événement déclenché à chaque nouveau message
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # Le bot teste si "bonjour" est entré dans le salon et répond par l'émoji vulcan
    if "bonjour" == message.content:
        await message.channel.send(":vulcan:")    
    mot_banni = "aurevoir"
    if message.author == bot.user:  # Ne pas traiter les messages du bot lui-même
        return

    if mot_banni in message.content.lower():
        await message.delete()  # Supprimer le message contenant le mot interdit
        await message.author.send(f"Votre message contenant le mot '{mot_banni}' a été supprimé.")
        
        # Bannir l'utilisateur qui a envoyé le message
        await message.guild.ban(message.author, reason=f"Utilisation du mot interdit '{mot_banni}'")
        
        print(f"Utilisateur {message.author.name} banni pour utilisation du mot interdit '{mot_banni}'")

    await bot.process_commands(message)

# Événement déclenché lorsqu'un nouveau membre rejoint le serveur
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel:
        # Insérer le lien vers le GIF de Discord entre les points d'exclamation
        gif_url = "https://media.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif"
        await channel.send(f"Bienvenue dans la taverne, {member.mention} ! Voici un accueil chaleureux pour toi : {gif_url}")


# Commande pour dire bienvenue à une personne spécifiée
@bot.command()
async def welcome(ctx):
    await ctx.send("Bienvenue dans la taverne!") 

# Commande pour saluer le bot
@bot.command()
async def salutBot(ctx, nom_bot):
    await ctx.send(f"Bonjour le bot : {nom_bot}")

# Lancement du bot
if __name__ == "__main__":
    bot.run(TOKEN)
