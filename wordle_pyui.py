from wordlefilter import *
import re

#display the results                             
def possible_guess_results(filtered_list: list):
    if len(filtered_list) == 0:
        try_again = input("\nHow do I say this? \n\nI have failed you.. or you have failed me.\n\nI have no possible answers that meet your conditions.\n\n Try again? [Y/N]: ")
        if try_again == "Y" or try_again == 'y':
            get_started()
        else:
            quit()
    elif len(filtered_list) == 1:
        print(f"   *:.Congratuations!.:*\n\n {filtered_list} is your answer! \n        ... right?")
        quit()
    else:
        print(filtered_list)
        
        
# validate the user input
def validate_input(user_input):
    pattern = r'^[A-Za-z]+$'
    if re.match(pattern, user_input):
        return True
    else:
        return False

# ask for guesses and correct letters    
def ask_guess(user_dict):
    username = input("Enter your username:\n")
    if username not in user_dict:
        user_dict[username] = create_new_user(username)
        
    player = user_dict[username]

    while True:
        while True:
            player.guess = input("\nInput your 5 letter guess:\n").strip()
            if player.guess == '!quit':
                print("\n Exiting wordle_bot now...\n")
                quit()
                
            elif validate_input(player.guess):
                break
            else:
                print("Invalid input. Please only use upper and lowercase letters")
        while True:
            player.guess_cl = input("\nWhich letters are in the word but out of position?:\n").lower().strip()
            if player.guess_cl == '!quit':
                print("\n Exiting wordle_bot now...\n")
                quit()
            elif player.guess_cl == "":
                break
            elif validate_input(player.guess_cl):
                break
            else:
                print("Invalid input. Please only use upper and lowercase letters\n")
            
        wordle_filter(player)
        possible_guess_results(player.filtered_list)
    
# how to play       
def get_started():
    print("\n   ###### Welcome to Wordle_Helper_Bot! ######\n")
    print("Input all incorrectly positioned letters in lowercase\nInput correctly positioned letters in UPPERCASE\nType '!quit' to exit")
    user_dict = {}
    ask_guess(user_dict)
    

get_started()
