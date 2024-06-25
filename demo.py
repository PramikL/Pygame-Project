import random
def display_hangman(tries):
    stages = [  # list of strings representing the hangman
        """
           --------
           |      |
           |      O
           |     \|/
           |      |
           |     / \
           -
        """,
        """
           --------
           |      |
           |      O
           |     \|/
           |      |
           |     /
           -
        """,
        """
           --------
           |      |
           |      O
           |     \|/
           |      |
           |     
           -
        """,
        """
           --------
           |      |
           |      O
           |      |/
           |      |
           |      
           -
        """,
        """
           --------
           |      |
           |      O
           |      |
           |      |
           |      
           -
        """,
        """
           --------
           |      |
           |      O
           |    
           |      
           |      
           -
        """,
        """
           --------
           |      |
           |      
           |    
           |      
           |      
           -
        """
    ]
    return stages[tries]

def play_hangman():
    word_list = ["python", "java", "kotlin", "javascript", "ruby"]
    word = random.choice(word_list)
    word_letters = set(word)
    alphabet = set("abcdefghijklmnopqrstuvwxyz")
    used_letters = set()
    tries = 3
    print("H A N G M A N")
    while tries > 0:
        print()
        print(display_hangman(tries))
        if len(word_letters) == 0:
            print("You won! The word was", word)
            break
        print("\nUsed letters:", " ".join(used_letters))
        print("\nWord: ", end="")
        for letter in word:
            if letter in used_letters:
                print(letter, end=" ")
            else:
                print("_", end=" ")
        print()
        print("\nEnter a letter:")
        letter = input().lower()
        if letter in alphabet - used_letters:
            used_letters.add(letter)
            if letter in word_letters:
                word_letters.remove(letter)
        else:
            print("You already used that letter or entered an invalid character. Try again.")
            tries -= 1
    else:
        print("You lost! The word was", word)

play_hangman()