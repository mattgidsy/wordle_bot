class WordleUser:
    def __init__(self, user_id=None, name=None,  guess=None, guess_cl=None, filtered_list=None, word_list=None):
        if filtered_list is None:
            filtered_list = []
        if word_list is None:
            try:
                with open("wordle_list.txt") as wordle_list:
                    lines = wordle_list.readlines()
                word_list = [word.strip() for word in lines]
            except FileNotFoundError:
                print("\n'wordle_list.txt' could not be found")
                print("\nExiting the program...\n")
                quit()
        self.user_id = user_id
        self.name = name
        self.guess = guess
        self.guess_cl = guess_cl
        self.filtered_list = filtered_list
        self.word_list = word_list
    
    #filter any words that do not contain all of the correct letters (this catches repeat letters)    
    def filter_all_correct(self) -> list:
        # Dictionary to store the required letters and their counts
        required_letters = {}

        # Process letters from self.guess (uppercase only)
        for letter in self.guess:
            if letter.isupper():
                lower_letter = letter.lower()
                required_letters[lower_letter] = required_letters.get(lower_letter, 0) + 1

        # Process letters from self.guess_cl (all letters)
        for letter in self.guess_cl:
            lower_letter = letter.lower()
            required_letters[lower_letter] = required_letters.get(lower_letter, 0) + 1

        # Filter words based on required letters and counts
        temp_possible_words = []
        for word in self.filtered_list:
            if all(word.count(letter) >= count for letter, count in required_letters.items()):
                temp_possible_words.append(word)
                
        self.filtered_list = temp_possible_words
        return self.filtered_list

    #filter words with letters that were correct but out of position, filter words with the correct letter's incorrrect position
    def filter_incorrect_positions(self) -> list:
        
        temp_possible_words = []
        # Create the list of tuples (index, letter) for each letter in guess_cl and its corresponding index in guess
        guess_cl_positions = [(index, char) for index, char in enumerate(self.guess) if char in self.guess_cl]
        # If there are letters to check in guess_cl and filtered_list is not empty
        if guess_cl_positions and self.filtered_list:

            for word in self.filtered_list:
                # Initialize a flag to indicate a match
                match = False
                for index, char in guess_cl_positions:  # Adjusted order here
                    # Check if any of the letters in guess_cl_positions matches the same position in the word
                    if word[index] == char:
                        match = True
                        break  # Break the loop if a match is found

                # Add the word to temp_possible_words if there is no match
                if not match:
                    temp_possible_words.append((word))

            # Update filtered_list with the filtered list
            self.filtered_list = temp_possible_words 
        else:
            pass
        
        return self.filtered_list

    # filter the words that have letters that should be totally excluded from the word (letters neither correct nor in posistion)
    def filter_excluded_letter(self) -> list:
        
        temp_possible_words = []    
        # create the list of excluded letters
        excluded_letters = [letter for letter in self.guess if letter.islower() and letter not in self.guess_cl]
        # create a list of tuples containing the correct letters and their indexed positions   
        correct_positions = [(index, char.lower()) for index, char in enumerate(self.guess) if char.isupper() and char not in self.guess_cl]
        
        #if the filtered list is empty make the filtered list the word list
        if len(self.filtered_list) == 0:
            self.filtered_list = self.word_list
            
        #filter through possible words ignoring letters in the correct positions. allows for repeat letters
        for word in self.filtered_list:
            contains_excluded = False
            for index,char in enumerate(word):
                if (index,char) not in correct_positions and char in excluded_letters:
                    contains_excluded = True
                    break # Break the inner loop if an excluded letter is found
                
            # Add the tuple to temp_possible_words if it does not contain any excluded letter
            if not contains_excluded:
                temp_possible_words.append(word)
        self.filtered_list = temp_possible_words
        
        return self.filtered_list

    #filter words that have the correct letters in the correct postion
    def filter_correct_position(self) -> list: 
        temp_possible_words = []
        #index the guessed word's letters for parsing
        guessed_positions = [(index, char.lower()) for index, char in enumerate(self.guess) if char.isupper()]
        
        #check if there are any uppercase letters and if filtered_list is empty
        if any(letter.isupper() for letter in self.guess) and len(self.filtered_list) == 0:
            #search word_list
            for word in self.word_list:
                # Check if all guessed letters are in the correct positions
                if all((i,c) in guessed_positions and c == word[i] for i,c in guessed_positions):
                    temp_possible_words.append(word)
                else:
                    pass
            self.filtered_list = temp_possible_words
        elif any(letter.isupper() for letter in self.guess) and len(self.filtered_list) > 0:
            #if word not in filtered_list append to a temp list and replace filtered list to deduce
            for word in self.filtered_list:
                if all((i,c) in guessed_positions and c == word[i] for i,c in guessed_positions):
                    temp_possible_words.append(word)
                else:
                    pass
            self.filtered_list = temp_possible_words
        else: 
            pass
        
        return self.filtered_list

    #filter words that include the correct letters        
    def filter_correct_letter(self) -> list:
        temp_possible_words = []    
        correct_letters = list(self.guess_cl)
        
        #pass if guess_cl is empty
        if self.guess_cl == "":
            pass
            
        elif len(self.filtered_list) == 0:
            for word in self.word_list:
                if all(char in word for char in correct_letters) and word not in temp_possible_words:
                    # If true, append the word to the filtered list if it's not there
                    temp_possible_words.append(word)
                self.filtered_list = temp_possible_words
            
                        
        else:
            for word in self.filtered_list:
                # Check if at least one of the specified letters is present in the word
                if all(char in word for char in correct_letters):
                    #if word not in filtered_list append to a temp list and replace filtered list to deduce
                    temp_possible_words.append(word)
            self.filtered_list = temp_possible_words
            
        return self.filtered_list
        
def wordle_filter(player: WordleUser ) -> list:
    
    player.filter_correct_letter()
    player.filter_correct_position()
    player.filter_excluded_letter()
    player.filter_incorrect_positions()
    player.filter_all_correct()
    
    return player.filtered_list 

def create_new_user(user_id):
    return WordleUser(user_id=user_id)
  
