import settings
import discord
from discord.ext import commands
from wordlefilter import *

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix= "!", intents=intents)
    
    @bot.event
    async def on_ready():
        print(bot.user)
        print(bot.user.id)
        print("____________________")
    
    @bot.command(
    aliases = ['p'],
    help = "this is help",
    description = "this is description",
    brief = "this is brief"
    )
    
    async def ping(ctx):
        filter_list = ["pong", "dad", "slate", "rubber"]
        await ctx.send(filter_list)
        
    @bot.command()
    async def say(ctx, *user_input): #this is giving me user_input as a tuple
        if user_input == "":
            await ctx.send("you must enter a word for me to say because I can't send empty messages")
        else:
            await ctx.send(user_input)
    
    @bot.command()
    async def say2(ctx, user_input = "user_input??", user_input2 = "Why"): # adding "user_input" and "why" as defaults if no parameter is passed by the user
        await ctx.send(user_input +" "+ user_input2)
    
    @bot.command()
    async def sayindex(ctx, *user_input):
        await ctx.send(user_input[:])
        await ctx.send(user_input[0])
    
    @bot.command()
    async def saylist(ctx, *user_input):
        i = 0
        for word in user_input:
            await ctx.send(user_input[i])
            i = i+1
    
    @bot.command()
    async def wordle(ctx, guess, guess_cl):
        player = WordleUser()
        player.guess = guess
        player.guess_cl = guess_cl
        filter_list = []
        filter_list = wordle_filter(player)
        #filter_list = ['pong', 'dad', 'slate', 'rubber']
        await ctx.send(filter_list) 
    
    
        
    bot.run(settings.DISCORD_API_SECRET)
if __name__ == "__main__":
    run()

#filter_list = ["pong", "dad", "slate", "rubber"]