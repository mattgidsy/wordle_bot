from wordlefilter import *
import re
import discord
from discord.ext import commands
fh = open(r'C:\Users\mattl\Documents\wordlebot_secret\WordleSecretToken.txt')
TOKEN = fh.read()

intents = discord.Intents.default()
intents.message_content = True


client = commands.Bot(command_prefix='.', intents=intents)

@client.event
async def on_ready():
    print('bot ready')
    
# @client.event
# async def on_message(message):
#     #channel = client.get_channel(1030698526075785298)
#     #await channel.send('testing')
#     print(message.author, message.content, message.channel.id)
# #     pass
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

@client.command()
async def hello(ctx):
    channel = client.get_channel(691441597388161139)
    await channel.send(f'hello there {ctx.author.mention}')
    
client.run(TOKEN)


# #display the results                                        
# def possible_guess_results(filtered_list: list):
#     if len(filtered_list) == 0:
#         try_again = input("\nHow do I say this? \n\nI have failed you.. or you have failed me.\n\nI have no possible answers that meet your conditions.\n\n Try again? [Y/N]: ")
#         if try_again == "Y" or try_again == 'y':
#             get_started()
#         else:
#             quit()
#     elif len(filtered_list) == 1:
#         print(f"   *:.Congratuations!.:*\n\n {filtered_list} is your answer! \n        ... right?")
#         quit()
#     else:
#         print(filtered_list)
        
        
# # validate the user input
# def validate_input(user_input):
#     pattern = r'^[A-Za-z]+$'
#     if re.match(pattern, user_input):
#         return True
#     else:
#         return False

# # ask for guesses and correct letters    
# def ask_guess():
#     player = WordleUser()
#     while True:
#         while True:
#             player.guess = input("\nInput your 5 letter guess:\n").strip()
#             if player.guess == '!quit':
#                 print("\n Exiting wordle_bot now...\n")
#                 quit()
                
#             elif validate_input(player.guess):
#                 break
#             else:
#                 print("Invalid input. Please only use upper and lowercase letters")
#         while True:
#             player.guess_cl = input("\nWhich letters are in the word but out of position?:\n").lower().strip()
#             if player.guess_cl == '!quit':
#                 print("\n Exiting wordle_bot now...\n")
#                 quit()
#             elif player.guess_cl == "":
#                 break
#             elif validate_input(player.guess_cl):
#                 break
#             else:
#                 print("Invalid input. Please only use upper and lowercase letters\n")
            
#         wordle_filter(player)
#         possible_guess_results(player.filtered_list)
    
# # how to play       
# def get_started():
#     print("\n   ###### Welcome to Wordle_Helper_Bot! ###### \n\nInput all incorretly positioned letters in lowercase \n   Input correctly positioned letters in UPPERCASE\n      Type '!quit' to exit")
#     print("\n   ###### Welcome to Wordle_Helper_Bot! ######")
#     ask_guess() 
 
# get_started()
