import random
import string


def generate_random_string():
    '''A string that starts with a character and is followed by 2 numbers (3 characters in total)'''
    letter = random.choice(string.ascii_letters).lower()
    numbers = f"{random.randint(0, 9)}{random.randint(0, 9)}"  
    return letter + numbers