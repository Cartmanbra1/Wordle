# Set array and dictionaries to be used in the program
triesarray = []
score_games = {}
score_winrate = {}
score_wins = {}
score_tries = {}
scoreboard = {}
winrate_multiplier = 100


def basic_settings():
    """
    Returns a dictionary of basic settings.

    Returns:
        dict: A dictionary containing the basic settings with the following keys:
            - 'tries': An integer representing the number of tries.
            - 'word_length': An integer representing the length of the word.
            - 'file_path': A string representing the file path of the word list.
    """
    # Set settings to their basic values
    settings = {'tries': 6, 'word_length': 5, 'file_path': 'words.txt'}
    # return the Set Settings dict
    return settings


# Creating the basic settings for the game
settings = basic_settings()


def openSettings():
    file_path = settings['file_path']
    # To get the list of words from the file:
    file = open(file_path, "r")
    words = file.read().splitlines()
    file.close()
    return words


def update_settings(settings):
    """
    Updates the settings dictionary based on user input.

    Args:
        settings (dict): The dictionary containing the current settings.

    Returns:
        dict: The updated settings dictionary.

    """
    # Prompt the user to enter settings
    print("Enter settings:")
    new_settings = input().strip()
    # Check if the settings input is enclosed in curly braces
    if new_settings[0] != '{' or new_settings[-1] != '}':
        print("Invalid settings")
        return
    # Remove the outer curly braces from the settings input
    new_settings = new_settings[1:-1]
    length = len(new_settings)
    # Check if there are leading or trailing spaces in the settings input
    if new_settings[0] == ' ' or new_settings[length - 1] == ' ':
        print("Invalid settings")
        return
    # Split the settings input into a list of key-value pairs
    settings_list = new_settings.split(',')
    # Process each key-value pair in the settings list
    for setting in settings_list:
        # Split the key-value pair into key and value
        key_value = setting.split(':')
        # Check if the key-value pair is valid
        if len(key_value) != 2:
            print("Invalid settings")
            return
        # Extract the key and remove leading/trailing spaces
        key = key_value[0].strip()
        # Extract the value and remove leading/trailing spaces
        if key == 'tries' or key == 'word_length':
            value = int(key_value[1].strip())
        else:
            value = key_value[1].strip()
        # Store the key-value pair in the settings dictionary
        settings[key] = value
    # Print the final settings dictionary
    print("Settings were updated")
    # Return the settings dictionary
    return settings


def start_game():
    """
    Starts the game by getting player's name and word input.

    Returns:
        None

    """
    # Prompt the user to enter the player's name
    print("Enter player's name:")
    name = input()
    # Prompt the user to enter a word
    print("Enter a word:")
    word = input()
    # Check if the word is in the list of valid words
    words = openSettings()
    if word not in words:
        print("That's not a word!")
        return
    # Check if the length of the word matches the expected word length from the settings
    elif len(word) != settings['word_length']:
        print("That word is the wrong length!")
        return
    # Call the play_game function with the provided word and player's name
    play_game(word, name)


def play_game(word, name):
    """
    Plays the Wordle game with the given word and player's name.

    Args:
        word (str): The word to be guessed.
        name (str): The player's name.

    Returns:
        None

    """
    # Welcome message with the number of tries and word length from the settings
    print("Welcome to Wordle! You have", settings['tries'], "tries to guess the word.")
    print("The word is", settings['word_length'], "letters long.")
    i = 0

    # Start the guessing loop
    while i < settings['tries'] + 1:
        # Prompt the user to guess a word
        print("Guess a word:")
        guess = input()

        # Check if the guess is invalid
        words = openSettings()
        if len(guess) != len(word) or guess not in words:
            print("Invalid guess")
            continue

        i += 1
        # Check the guessed word against the target word
        check = check_word(word, guess, name)

        # Check if the guessed word is correct
        if check == 1:
            return

        # Check if the maximum number of tries is reached
        if i == settings['tries']:
            print("\nYou lost! The word was", word)
            print("Game over!")
            for i in triesarray:
                print(i)
            add_to_scoreboard(name, 1, 0, 0)
            triesarray.clear()
            return

        print("")


def check_word(word, guess, name):
    """
    Checks the guessed word against the target word and provides feedback.

    Args:
        word (str): The target word to be guessed.
        guess (str): The player's guessed word.
        name (str): The player's name.

    Returns:
        int: Returns 1 if the guess matches the target word, otherwise returns 0.

    """
    # Get the length of the word
    length = len(word)
    # Initialize an empty string for recording tries
    compare = ""
    tries = ""
    count = 0
    # Check if the guessed word is correct
    if word == guess:
        print(word)
        print("You win!\nGame over!")
        for i in triesarray:
            print(i)
        add_to_scoreboard(name, 1, len(triesarray) + 1, 100)
        triesarray.clear()
        print(word)
        return 1
    # Process each character in the word and guess
    for i in range(len(word)):
        for k in range(len(word)):
            # Check if the characters at the same position match
            if word[i] == guess[i]:
                print(word[i], end="")
                tries += word[i]
                compare += word[i]
                break
            # Check if the characters at different positions match
            elif word[k] == guess[i]:
                # Check the edge case if the letter already appears in the correct spot
                for j in compare:
                    if word[k] in compare:
                        count += 1
                        break
                if count > 0:
                    count = 0
                    tries += "-"
                    print("-", end="")
                    break
                else:
                    print("+", end="")
                    tries += "+"
                    break
            # If no match is found
            elif k == len(word) - 1:
                print("-", end="")
                tries += "-"
                break
    # Record the current try in the triesarray list
    if not bool(triesarray):
        triesarray.append(tries)
    else:
        triesarray.append(tries)
    return 0


def print_settings(settings):
    """
    Prints the settings dictionary in a formatted manner.

    Args:
        settings (dict): The dictionary containing the settings.

    Returns:
        None

    """
    # Initialize an empty string to store the formatted settings
    settings_str = ''
    # Sort the settings dictionary by keys
    sorted_settings = sorted(settings.items())
    # Iterate over the sorted settings and format them as key-value pairs
    for key, value in sorted_settings:
        settings_str += key + ': ' + str(value) + '\n'
    # Print the formatted settings string (excluding the last newline character)
    print(settings_str[:-1])


def add_to_scoreboard(name, games_played, guesses, win_rate):
    """
    Adds player's score to the scoreboard based on the number of games played, guesses, and win rate.

    Args:
        name (str): The player's name.
        games_played (int): The number of games played.
        guesses (int or str): The number of guesses or 'NaN' if not applicable.
        win_rate (float): The win rate as a decimal.

    Returns:
        None

    """
    # Set default values for the scoreboard, score_games, score_winrate, and score_tries dictionaries
    scoreboard.setdefault(name, 0)
    score_games.setdefault(name, 0)
    score_winrate.setdefault(name, 0)
    score_wins.setdefault(name, 0)
    score_tries.setdefault(name, 0)
    # Update the number of games played for the player
    score_games[name] = score_games[name] + games_played
    # Calculate the amount of wins for the player
    if win_rate != 0:
        score_wins[name] += 1
    # Calculate the win rate for the player
    score_winrate[name] = score_wins[name] / (score_games[name])
    # Calculate the average number of tries for the player
    score_tries[name] = guesses + score_tries[name]
    # Calculate the total score for the player
    scoreboard[name] = score_games[name] + score_winrate[name] + score_tries[name]


def print_scoreboard():
    """
    Prints the scoreboard in a formatted manner.

    Args:
        None

    Returns:
        None

    """
    # Initialize an empty string to store the formatted scoreboard
    scoreboard_str = ''
    # Sort the score_winrate dictionary by win rate in descending order, and then by player name in ascending order
    sorted_winrate = sorted(score_winrate.items(), key=lambda x: (-x[1], x[0]))
    # Iterate over the sorted_winrate and format the scoreboard entries
    print("Scoreboard:")
    for key, value in sorted_winrate:
        # Check if the average number of tries is not NaN
        if score_tries[key] != 0:
            scoreboard_str += f"{key}: {score_games[key]} games, {winrate_multiplier * value:.2f}% win rate," \
                              f" {(score_tries[key] / score_wins[key]):.2f} average tries\n"
        else:
            scoreboard_str += f"{key}: {score_games[key]} games, {winrate_multiplier * value:.2f}% win rate," \
                              f" NaN average tries\n"
    # Print the formatted scoreboard string (stripping leading/trailing whitespaces)
    print(scoreboard_str.strip())


def menu(settings):
    """
    Displays a menu and performs actions based on user input.

    Args:
        settings (dict): The dictionary containing the settings.

    Returns:
        None

    """
    while True:
        # Prompt the user to choose an option
        print("Choose an option:\n"
              "0. Exit\n"
              "1. Update settings\n"
              "2. Play\n"
              "3. View settings\n"
              "4. Scoreboard")
        answer = input()
        # Check the user's chosen option and perform the corresponding action
        if answer == '0':
            # Exit the loop and end the program
            break
        elif answer == '1':
            # Update the game settings
            back_up = settings
            settings = update_settings(settings)
            if settings is None:
                settings = back_up
        elif answer == '2':
            # Start the game
            start_game()
        elif answer == '3':
            # View the current game settings
            print_settings(settings)
        elif answer == '4':
            # View the scoreboard
            print_scoreboard()
        else:
            # Handle invalid input
            print("Invalid Input")


def main():
    """
    Main function that starts the program.

    Args:
        None

    Returns:
        None

    """
    # Call the menu function
    menu(settings)


# Start the program
if __name__ == "__main__":
    main()
