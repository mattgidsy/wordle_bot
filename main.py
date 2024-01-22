import settings
import discord
from discord import app_commands
from discord.ext import commands
from wordlefilter import *
from validator import *

def run():
 
    #create a dictionary to store multiple users 
    user_dict ={}
   
    intents = discord.Intents.all()
    intents.message_content = True
    intents.members = True
    bot = commands.Bot(command_prefix= "!", intents=intents)
    
    
    # bot logging
    @bot.event
    async def on_ready():
        print(f"Bot User: {bot.user}")
        print(f"Bot Id: {bot.user.id}")
        print(f"Bot Guild ID:{bot.guilds[0].id}")
        print("____________________")
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='/wordle'))

    
    #when the bot is being rude    
    @bot.hybrid_command(
        help = "when the bot is being rude.",
        description = "when the bot is being rude."
    )
    async def rude(ctx): 
        await ctx.send(f"I'm sorry, ~~Dave~~...{ctx.author.name}") 
                 
    #enter !wordle guess guess_correct_letters example: !wordle slAtE s
    @bot.hybrid_command(
        user_dict,
        aliases = ['w'],
        help = "This is the Wordle Helper Bot",
        description = "Type your guess: using CAPS for green letters, correct letters = yellow letters",
        brief = "This bot helps solve wordles"
        )
    async def wordle(ctx, guess, correct_letters = ""):
        
        #creates a user tied to the discord username   
        user_name = ctx.author.name
        user_id = ctx.author.id
        guess_cl = correct_letters
        
        if user_id not in user_dict:
            user_dict[user_id] = create_new_user(user_id)
        
        player = user_dict[user_id]
        player.name = user_name
        
        if guess == validate_guess(guess):
            player.guess = guess
            if guess_cl == "":
                player.guess_cl = guess_cl
                wordle_filter(player)
                if len(player.filtered_list) == 0:
                    await ctx.send(f"Dear, {player.name}, I'm sorry that I (or you) are at fault here. Your list of possible answers looks empty. Much like my care cup.", ephemeral=True)               
                elif len(player.filtered_list) >= 1000:
                    await ctx.send(f"I'm sorry {player.name}, you are not a good guesser. There are over 1000 words for you to choose from and I'll get rate limited if I send them all to you now. How about you take another guess. Maybe a better guess. like slate or trope. once you get your list below 1000, I'll send you the word list.", ephemeral=True)
                else:
                    #batch the lists into 200 word lists to stay under 2k character count on discord
                    for i in range(0, len(player.filtered_list), 200):
                            await ctx.send(f"{player.name}'s list of possible wordle words:\n{player.filtered_list[i:i + 200]}", ephemeral=True)                                     
            elif guess_cl == validate_guess_cl(guess_cl):
                    player.guess_cl = guess_cl
                    wordle_filter(player)
                    if len(player.filtered_list) == 0:
                        await ctx.send(f"Dear, {player.name}, I'm sorry that I (or you) are at fault here. Your list of possible answers looks empty. Much like my care cup.", ephemeral=True)
                    elif len(player.filtered_list) >= 1000:
                        await ctx.send(f"I'm sorry {player.name}, you are not a good guesser. There are over 1000 words for you to choose from and I'll get rate limited if I send them all to you now. How about you take another guess. Maybe a better guess. like slate or trope. once you get your list below 1000, I'll send you the word list.", ephemeral=True)
                    else:
                        for i in range(0, len(player.filtered_list), 200):
                                await ctx.send(f"{player.name}'s list of possible wordle words:\n{player.filtered_list[i:i + 200]}", ephemeral=True)                    
            else:
                await ctx.send(f"{player.name}, there was a problem with your second input. Please remember that I am dumb and can only accept 5 letter words with no special characters (except for an empty field here).", ephemeral=True)     
        else:
            await ctx.send(f"{player.name}, there was a problem with your guess's first input. Please remember that I am dumb and can only accept 5 letter words with no special characters.", ephemeral=True)
            await ctx.send("type /wordle to try again. \nHere's an example: \n!wordle SlAte e", ephemeral=True)
            
    #clears the user's saved data  
    @bot.hybrid_command(
        user_dict,
        help = "This clears your old guesses",
        description = "This clears your old guesses",
        brief = "This clears your old guesses")
    async def clear(ctx):
        user_name = ctx.author.name
        user_id = ctx.author.id
        
        if user_id in user_dict:
            player = user_dict[user_id]
            player.filtered_list = []
            await ctx.send(f"{player.name}, your wordle list has been cleared.", ephemeral=True)
        else:
            await ctx.send(f"{user_name}, I don't seem to have a list for you, fam.", ephemeral=True)
    
    #sync with discord, use when changes are made to slash commands
    @bot.command(hidden=True)
    async def sync(ctx):
        user_id = ctx.author.id
        owner_id = ctx.guild.owner_id
        user_name = ctx.author.name
        if user_id == owner_id:
            bot.tree.copy_global_to(guild=settings.GUILDS_ID)
            await bot.tree.sync(guild=settings.GUILDS_ID)
            await ctx.send(f"{user_name}, I have requested to sync with the hive.", ephemeral=True)
        else:
            await ctx.send(f"Sorry, {user_name}, you don't have permission to use that command.\n Dad doesn't want to get rate limited.")
            
    bot.run(settings.DISCORD_API_SECRET)
    
if __name__ == "__main__":
    run()
