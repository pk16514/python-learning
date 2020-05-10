
# PASTE YOUR WOFPlayer CLASS (from part A) HERE
# PASTE YOUR WOFHumanPlayer CLASS (from part B) HERE
# PASTE YOUR WOFComputerPlayer CLASS (from part C) HERE


import sys
sys.setExecutionLimit(600000) # let this take up to 10 minutes

import json
import random
import time

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
VOWELS  = 'AEIOU'
VOWEL_COST  = 250

#from random import randrange
#from random import randint

# Write the WOFPlayer class definition (part A) here

# Write the WOFHumanPlayer class definition (part B) here

# Write the WOFComputerPlayer class definition (part C) here

class WOFPlayer:
    def __init__(self, name):
        self.name = name
        self.prizes = []
        self.prizeMoney = 0


    def addMoney(self, amt):
        self.prizeMoney = self.prizeMoney + amt

    def goBankrupt(self):
        self.prizeMoney = 0

    def addPrize(self, prize):
        self.prizes.append(prize)

    def __str__(self):
        return "{} (${})".format(self.name, self.prizeMoney)


class WOFHumanPlayer(WOFPlayer):
    def getMove(self, category, obscuredPhrase, guessed):
        user_inp = input("\n{} has ${}\n\nCategory: {}\nPhrase: {}\nGuessed: {}\n\nGuess a letter, phrase, or type 'exit' or 'pass':".format(self.name, self.prizeMoney, category, obscuredPhrase, guessed))
        return user_inp

class WOFComputerPlayer(WOFPlayer):
    SORTED_FREQUENCIES = 'ZQXJKVBPYGFWMUCLDRHSNIOATE'
    def __init__(self, name, difficulty):
        super().__init__(name)
        self.difficulty = difficulty

    def smartCoinFlip(self):
        rnd_num = random.randint(1, 10)
        if rnd_num > self.difficulty:
            return True
        else:
            return False

    def getPossibleLetters(self, guessed):
        possible_letters = []
        for char in LETTERS:
            if char in guessed:
                continue
            if char in VOWELS:
                if self.prizeMoney < VOWEL_COST:
                    continue
                else:
                    possible_letters.append(char)
            else:
                possible_letters.append(char)
        return possible_letters

    def getMove(self, category, obscuredPhrase ,guessed):
        gl = self.getPossibleLetters(guessed)
        letters_sorted_by_freq = [x for x in self.SORTED_FREQUENCIES if x in gl]
        if len(gl) < 1:
            return 'pass'
        scf = self.smartCoinFlip()
        if scf == True:
            return letters_sorted_by_freq[-1]
        elif scf == False:
            return random.choice(letters_sorted_by_freq)


# Repeatedly asks the user for a number between min & max (inclusive)
def getNumberBetween(prompt, min, max):
    userinp = input(prompt) # ask the first time

    while True:
        try:
            n = int(userinp) # try casting to an integer
            if n < min:
                errmessage = 'Must be at least {}'.format(min)
            elif n > max:
                errmessage = 'Must be at most {}'.format(max)
            else:
                return n
        except ValueError: # The user didn't enter a number
            errmessage = '{} is not a number.'

        # If we haven't gotten a number yet, add the error message
        # and ask again
        userinp = input('{}\n{}'.format(errmessage, prompt))

# Spins the wheel of fortune wheel to give a random prize
# Examples:
#    { "type": "cash", "text": "$950", "value": 950, "prize": "A trip to Ann Arbor!" },
#    { "type": "bankrupt", "text": "Bankrupt", "prize": false },
#    { "type": "loseturn", "text": "Lose a turn", "prize": false }
def spinWheel():
    with open("wheel.json", 'r') as f:
        wheel = json.loads(f.read())
        return random.choice(wheel)

# Returns a category & phrase (as a tuple) to guess
# Example:
#     ("Artist & Song", "Whitney Houston's I Will Always Love You")
def getRandomCategoryAndPhrase():
    with open("phrases.json", 'r') as f:
        phrases = json.loads(f.read())

        category = random.choice(list(phrases.keys()))
        phrase   = random.choice(phrases[category])
        return (category, phrase.upper())

# Given a phrase and a list of guessed letters, returns an obscured version
# Example:
#     guessed: ['L', 'B', 'E', 'R', 'N', 'P', 'K', 'X', 'Z']
#     phrase:  "GLACIER NATIONAL PARK"
#     returns> "_L___ER N____N_L P_RK"
def obscurePhrase(phrase, guessed):
    rv = ''
    for s in phrase:
        if (s in LETTERS) and (s not in guessed):
            rv = rv+'_'
        else:
            rv = rv+s
    return rv

# Returns a string representing the current state of the game
def showBoard(category, obscuredPhrase, guessed):
    return """
    Category: {}
    Phrase:   {}
    Guessed:  {}""".format(category, obscuredPhrase, ', '.join(sorted(guessed)))

# GAME LOGIC CODE
print('='*15)
print('WHEEL OF PYTHON')
print('='*15)
print('')

num_human = getNumberBetween('How many human players? ', 0, 10)
num_computer = getNumberBetween('How many computer players? ', 0, 10)

# If there are computer players, ask how difficult they should be
if num_computer >= 1:
    difficulty = getNumberBetween('What difficulty for the computers? (1-10) ', 1, 10)

# Create the player instances
human_players = [WOFHumanPlayer(input('Enter the name for player #{} '.format(i+1))) for i in range(num_human)]
computer_players = [WOFComputerPlayer('Computer {}'.format(i+1), difficulty) for i in range(num_computer)]
players = human_players + computer_players

# No players, no game :(
if len(players) == 0:
    print('We need players to play!')
    raise Exception

category, phrase = getRandomCategoryAndPhrase()
guessed = []

playerIndex = 0

winner = False
while True:
    player = players[playerIndex]
    wheelPrize = spinWheel()

    print('-'*15)
    print(showBoard(category, obscurePhrase(phrase, guessed), guessed))
    print('')
    print('{} spins...'.format(player.name))
    time.sleep(2)
    print('{}!'.format(wheelPrize['text']))

    if wheelPrize['type'] == 'bankrupt':
        player.goBankrupt()
    elif wheelPrize['type'] == 'cash':
        move = player.getMove(category, obscurePhrase(phrase, guessed), guessed)
        move = move.upper()
        if move == 'EXIT':
            break
        elif move != 'PASS':
            if len(move) == 1:
                if move not in LETTERS:
                    print('Guesses should be alphanumeric. Try again.')
                    continue
                if move in guessed:
                    print('{} has already been guessed. Try again.'.format(move))
                    continue

                if move in VOWELS:
                    if player.prizeMoney < VOWEL_COST:
                        print('Need {} to guess a vowel. Try again.'.format(VOWEL_COST))
                        continue
                    else:
                        player.prizeMoney -= VOWEL_COST

                guessed.append(move)

                print('{} says "{}"'.format(player.name, move))

                count = phrase.count(move)
                if count > 0:
                    if count == 1:
                        print("There is one {}".format(move))
                    else:
                        print("There are {} {}'s".format(count, move))

                    player.addMoney(count * wheelPrize['value'])

                    if wheelPrize['prize']:
                        player.addPrize(wheelPrize['prize'])

                    if obscurePhrase(phrase, guessed) == phrase:
                        winner = player
                        break

                    continue

                elif count == 0:
                    print("There is no {}".format(move))
            else:
                if move == phrase:
                    player.addMoney(wheelPrize['value'])
                    if wheelPrize['prize']:
                        player.addPrize(wheelPrize['prize'])
                    winner = player
                    break
                else:
                    print('{} was not the phrase'.format(move))

    # Move on to the next player (or go back to player[0] if we reached the end)
    playerIndex = (playerIndex + 1) % len(players)

if winner:
    print('{} wins! The phrase was {}'.format(winner.name, phrase))
    print('{} won ${}'.format(winner.name, winner.prizeMoney))
    if len(winner.prizes) > 0:
        print('{} also won:'.format(winner.name))
        for prize in winner.prizes:
            print('    - {}'.format(prize))
else:
    print('Nobody won.')
