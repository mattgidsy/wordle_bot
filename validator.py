import re
def validate_guess(user_input):
    pattern = r'^[A-Za-z]+$'
    if re.match(pattern, user_input) and len(user_input) == 5:
        return user_input
    else:
        return False
def validate_guess_cl(user_input):
    pattern = r'^[A-Za-z]+$'
    if user_input == "":
        return user_input
    elif re.match(pattern, user_input) and len(user_input) <= 5:
        return user_input.lower()
    else:
        return False

def test():
    guess = "slAte"
    guess_cl = "A"
    print(validate_guess(guess))
    print(validate_guess_cl(guess_cl))
    
    
#test()