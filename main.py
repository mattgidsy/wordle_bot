import settings
import discord
from discord.ext import commands
from wordlefilter import *
from validator import *



def run():
 
 #create a dictionary to store multiple users 
    user_dict ={}
   
    intents = discord.Intents.all()
    intents.message_content = True
    bot = commands.Bot(command_prefix= "!", intents=intents)
    
#bot logging
    @bot.event
    async def on_ready():
        print(bot.user)
        print(bot.user.id)
        print("____________________")
    
    # @bot.command(
    # aliases = ['p'],
    # help = "this is help",
    # description = "this is description",
    # brief = "this is brief"
    # )
    
    
    
    # async def ping(ctx):
    #     filter_list = ["pong", "dad", "slate", "rubber"]
    #     await ctx.send(filter_list)
         
    # @bot.command()
    
    # async def say(ctx, *user_input): #this is giving me user_input as a tuple
    #     #global counter
    #     counter = counter +1
    #     userdict[ctx.author.name] = counter
    #     if user_input == "":
    #         await ctx.send("you must enter a word for me to say because I can't send empty messages")
    #     else:

    #         await ctx.send(user_input)
    #         await ctx.send(ctx.author.name)
    #         await ctx.send(userdict)
            
    
    # @bot.command()
    # async def say2(ctx, user_input = "user_input??", user_input2 = "Why"): # adding "user_input" and "why" as defaults if no parameter is passed by the user
    #     await ctx.send(user_input +" "+ user_input2)
    
    # @bot.command()
    # async def sayindex(ctx, *user_input):
    #     await ctx.send(user_input[:])
    #     await ctx.send(user_input[0])
    
    # @bot.command()
    # async def saylist(ctx, *user_input):
    #     i = 0
    #     for word in user_input:
    #         await ctx.send(user_input[i])
    #         i = i+1
    
#when the bot is being rude    
    @bot.command()
    async def rude(ctx):
        await ctx.send(f"I'm sorry, ~~Dave~~...{ctx.author.name}")

 
#enter !wordle guess guess_correct_letters example: !wordle slAtE s
    @bot.command(
        user_dict,
        aliases = ['w'],
        help = "This is the Wordle Helper Bot",
        description = "To use wordle bot, type your 5 letter guess and the correct letters (yellow letters). \n\nBe sure to CAPITALIZE letters that are in the correct position (green letters) \n\nexample:\n !wordle slAtE s",
        brief = "This bot helps solve wordles"
        )
    async def wordle(ctx, guess, guess_cl = ""):
        
        #creates a user tied to the discord username   
        user_name = ctx.author.name
        
        if user_name not in user_dict:
            user_dict[user_name] = create_new_user(user_name)
        
        player = user_dict[user_name]
        
        if guess == validate_guess(guess):
            player.guess = guess
            if guess_cl == "":
                player.guess_cl = guess_cl
                wordle_filter(player)
                if len(player.filtered_list) == 0:
                    await ctx.send(f"Dear, {player.name}, I'm sorry that I (or you) are at fault here. Your list of possible answers looks empty. Much like my care cup.")               
                else:
                    #batch the lists into 200 word lists to stay under 2k character count on discord
                    for i in range(0, len(player.filtered_list), 200):
                            await ctx.send(f"{player.name}'s list of possible wordle words:")
                            await ctx.send(player.filtered_list[i:i + 200])                                     
            elif guess_cl == validate_guess_cl(guess_cl):
                    player.guess_cl = guess_cl
                    wordle_filter(player)
                    if len(player.filtered_list) == 0:
                        await ctx.send(f"Dear, {player.name}, I'm sorry that I (or you) are at fault here. Your list of possible answers looks empty. Much like my care cup.")
                    else:
                        for i in range(0, len(player.filtered_list), 200):
                                await ctx.send(f"{player.name}'s list of possible wordle words:")
                                await ctx.send(player.filtered_list[i:i + 200])                    
            else:
                await ctx.send(f"{player.name}, there was a problem with your second input. Please remember that I am dumb and can only accept 5 letter words with no special characters (except for an empty field here).")     
        else:
            await ctx.send(f"{player.name}, there was a problem with your guess's first input. Please remember that I am dumb and can only accept 5 letter words with no special characters.")
            await ctx.send("type !wordle to try again. \nHere's an example: \n!wordle SlAte e")
            
#clears the user's saved data  
    @bot.command(user_dict)
    async def clear(ctx):
        user_name = ctx.author.name
        if user_name in user_dict:
            player = user_dict[user_name]
            player.filtered_list = []
            await ctx.send(f"{user_name}, your wordle list has been cleared.")
        else:
            await ctx.send(f"{user_name}, I don't seem to have a list for you, fam.")
            
#  #testing wordle command for multiuser
#     @bot.command(user_dict)
#     async def tword(ctx, guess, guess_cl = ""):
#         user_name = "Test_User"
#         #username = input("Enter your username:\n")
#         if user_name not in user_dict:
#             user_dict[user_name] = create_new_user(user_name)
        
#         player = user_dict[user_name]
#         if guess == validate_guess(guess):
#             #print("guess validated")
#             player.guess = guess
#             if guess_cl == "":
#                 #print("guess_cl validated")
#                 player.guess_cl = guess_cl
#                 wordle_filter(player)
#                 if len(player.filtered_list) == 0:
#                     await ctx.send(f"Dear, {player.name}, I'm sorry that I (or you) are at fault here. Your list of possible answers looks empty. Much like my care cup.")
#                 else:
#                     for i in range(0, len(player.filtered_list), 200):
#                             await ctx.send(f"{player.name}'s list of possible wordle words:")
#                             await ctx.send(player.filtered_list[i:i + 200])                
#             elif guess_cl == validate_guess_cl(guess_cl):
#                     player.guess_cl = guess_cl
#                     wordle_filter(player)
#                     if len(player.filtered_list) == 0:
#                         await ctx.send(f"Dear, {player.name}, I'm sorry that I (or you) are at fault here. Your list of possible answers looks empty. Much like my care cup.")
#                     else:
#                         for i in range(0, len(player.filtered_list), 200):
#                                 await ctx.send(f"{player.name}'s list of possible wordle words:")
#                                 await ctx.send(player.filtered_list[i:i + 200])                    
#             else:
#                 await ctx.send(f"{player.name}, there was a problem with your second input. Please remember that I am dumb and can only accept 5 letter words with no special characters (except for an empty field here).")     
#         else:
#             await ctx.send(f"{player.name}, there was a problem with your guess's first input. Please remember that I am dumb and can only accept 5 letter words with no special characters.")
#             await ctx.send("type !wordle to try again. \nHere's an example: \n!wordle SlAte e")
# #testing clear for multiuser            
#     @bot.command(user_dict)
#     async def tclear(ctx):
#         user_name = "Test_User"
#         if user_name in user_dict:
#             player = user_dict[user_name]
#             player.filtered_list = []
#             await ctx.send(f"{user_name}, your wordle list has been cleared.")
#         else:
#             await ctx.send(f"{user_name}, I don't seem to have a list for you, fam.")
                    
    bot.run(settings.DISCORD_API_SECRET)
    
if __name__ == "__main__":
    run()
# player = WordleUser()
# player.name = "matt."
# player.guess = "guAva"
# player.guess_cl = ""
# wordle_filter(player)
# print(player.filtered_list)

#filter_list = ["pong", "dad", "slate", "rubber"]