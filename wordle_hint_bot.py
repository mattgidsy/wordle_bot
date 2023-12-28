
#filter words with letters that were correct but out of position, filter words with the correct letter's incorrrect position
def filter_incorrect_positions(guess: str, guess_cl: str, filtered_list: list) -> list:

    # Create the list of tuples (index, letter) for each letter in guess_cl and its corresponding index in guess
    guess_cl_positions = []
    for index, char in enumerate(guess):
        if char in guess_cl:
            guess_cl_positions.append((index, char))  # Storing as (index, char)

    # If there are letters to check in guess_cl and filtered_list is not empty
    if guess_cl_positions and filtered_list:
        temp_possible_words = []

        for word in filtered_list:
            # Initialize a flag to indicate a match
            match = False
            for index, char in guess_cl_positions:  # Adjusted order here
                # Check if any of the letters in guess_cl_positions matches the same position in the word
                if word[index] == char:
                    match = True
                    break  # Break the loop if a match is found

            # Add the tuple to temp_possible_words if there is no match
            if not match:
                temp_possible_words.append((word))

        # Update filtered_list with the filtered list
        filtered_list = temp_possible_words
    else:
        pass
    
    return filtered_list

# filter the words that have letters that should be totally excluded from the word (letters neither correct nor in posistion)
def filter_excluded_letter(guess: str, guess_cl: str, filtered_list: list) -> list:
    temp_possible_words = []
    
    # Create the list of excluded letters
    excluded_letters = []
    for letter in guess:
        if letter.islower() and letter not in guess_cl:
            excluded_letters.append(letter)
            
    #create a list of tuples containing the correct letters and their indexed positions    
    correct_positions = []
    for index, char in enumerate(guess):
        if char not in guess_cl and char.isupper():
            correct_positions.append((index, char.lower()))
    
    #filter through possible words ignoring letters in the correct positions. allows for repeat letters
    for word in filtered_list:
        contains_excluded = False
        for index,char in enumerate(word):
             if (index,char) not in correct_positions and char in excluded_letters:
                 contains_excluded = True
                 break # Break the inner loop if an excluded letter is found
             
        # Add the tuple to temp_possible_words if it does not contain any excluded letter
        if not contains_excluded:
            temp_possible_words.append(word)
    filtered_list = temp_possible_words
    
    return filtered_list

# filter words that don't include the correct letter in the correct position
def filter_correct_position(guess: str, word_list: str, filtered_list: list) -> list: 
    temp_possible_words = []
    
    #check if there are any uppercase letters and if filtered_list is empty
    if any(letter.isupper() for letter in guess) and len(filtered_list) == 0:
        #index the guessed word's letters for parsing
        guessed_positions = [(index, char.lower()) for index, char in enumerate(guess) if char.isupper()]
        #search word_list
        for word in word_list:
            # Check if all guessed letters are in the correct positions
            if all((i,c) in guessed_positions and c == word[i] for i,c in guessed_positions):
                filtered_list.append(word)
    elif any(letter.isupper() for letter in guess) and len(filtered_list) > 0:
        guessed_positions = [(index, char.lower()) for index, char in enumerate(guess) if char.isupper()]
        #if word not in filtered_list append to a temp list and replace filtered list to deduce
        for word in filtered_list:
            if all((i,c) in guessed_positions and c == word[i] for i,c in guessed_positions):
                temp_possible_words.append(word)
        filtered_list = temp_possible_words
    else: 
        pass
    
    return filtered_list

#filter words that include the correct letters        
def filter_correct_letter(guess_cl: str,word_list: str, filtered_list: list) -> list:
    
    guess_letters = list(guess_cl)
    temp_possible_words = []

    if len(filtered_list) == 0:
        for word in word_list:
            # Check if at least one of the specified letters is present in the word
            if all(char in word for char in guess_letters):
                if word not in filtered_list:
                # If true, append the word to the filtered list if it's not there
                    filtered_list.append(word)
                    
    else:
        for word in filtered_list:
            # Check if at least one of the specified letters is present in the word
            if all(char in word for char in guess_letters):
                #if word not in filtered_list append to a temp list and replace filtered list to deduce
                temp_possible_words.append(word)
        filtered_list = temp_possible_words
        
    return filtered_list

#display the results                                        
def possible_guess_results(filtered_list: list):
    if len(filtered_list) == 0:
        try_again = input("\nHow do I say this? \nI have failed you, there are no possible answers.\nTry again? [Y/N]: ")
        if try_again == "Y" or try_again == 'y':
            get_started()
        else:
            quit()
    elif len(filtered_list) == 1:
        print(f"   *:.Congratuations!.:*\n\n {filtered_list} is your answer! \n        ... right?")
        quit()
    else:
        print(filtered_list)
        
 #send the guess and correct letters to be parsed and used to filter a possible guess list       
def filter_guess(guess: str, guess_cl: str, filtered_list: list ) -> list:
    
    #open the file containing a list of 5 letter words
    with open("guess_list.txt") as guess_list:
        lines = guess_list.readlines()
        
    #iterate through the word list (this one contains 5 letter words for wordle)   
    word_list = [word.strip() for word in lines]
    
    #search for letters and filter a list of possible words to guess
    filtered_list = filter_correct_position(guess, word_list, filtered_list)
    filtered_list = filter_correct_letter(guess_cl,word_list, filtered_list)
    filtered_list = filter_excluded_letter(guess, guess_cl, filtered_list)
    filtered_list = filter_incorrect_positions(guess, guess_cl, filtered_list)
    
    return filtered_list

def ask_guess():
    #create list to hold the possible words to guess
    filtered_list = []
    
    for i in range(5):
        guess = input("\nInput your 5 letter guess:\n")
        if guess == "quit":
            quit()
        guess_cl = input("\nWhich letters are in the word but out of position?:\n")
        if guess_cl == 'quit':
            quit()
        filtered_list = filter_guess(guess, guess_cl, filtered_list)
        possible_guess_results(filtered_list)
        
def get_started():
    print("\n   ###### Welcome to Wordle_Helper_Bot! ###### \n\nInput all incorretly positioned letters in lowercase \n   Input correctly positioned letters in UPPERCASE\n      Type 'quit' to exit")
    print("\n   ###### Welcome to Wordle_Helper_Bot! ######")
    ask_guess() 
 
get_started()