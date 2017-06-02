# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
quit = False
original_hand = {}

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*':0,
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    word = word.lower()
    word_value = 0
    word_length = len(word)
    for letter in word:
        letter_value = SCRABBLE_LETTER_VALUES[letter]
        word_value = word_value + letter_value  
    second_value = (7 * word_length) - 3 * (n - word_length)
    if second_value < 1:
        second_value = 1
    return word_value * second_value
        

#print(get_word_score("fork", 7))

# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """    
    
    hand={'*':1}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    return hand
     

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    new_hand = dict(hand)
    fail_list = []
    for letter in word.lower():
        try:            
            new_hand[letter] -= 1
            if new_hand[letter] == 0:
                del new_hand[letter]
        except KeyError:
            #for letter in word.lower():
            #if KeyError:
                fail_list.append(letter)
    if len(fail_list) == 1:
        print (fail_list[0], ' isn\'t in your hand!\n')
    elif len(fail_list) > 1:
        
        print (", ".join(fail_list), ' aren\'t in your hand!\n')
    return new_hand

#hand = {'j':2, 'o':1, 'l':2, 'w':1, 'n':2}
#print (update_hand(hand, 'jolly'))


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    new_hand = dict(hand)
    word = word.lower()
        

    for vowel in VOWELS:
        test_word = word.replace('*', vowel)
        if test_word in word_list:
            break
    
    if test_word in word_list:
        for letter in word:
            try:
                new_hand[letter] -=1
                if -1 in new_hand.values():
                    return False
            except KeyError:
                return False         
        return True
    else:
        return False
                
#print (is_valid_word('*owz', {'c':1, 'o':1, 's':1, 'w':1, '*':3, 'z':1}, ['cows', 'titties', 'anal', 'chocolate', 'hello',]))


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    hand_values = hand.values()
    total = 0
    for number in hand_values:
        total = total + number
    return int(total)

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    letters_in_hand = 'The letters in your hand are:'
    points = '\nYour word ({}) earned you {} points!'
    not_valid = 'That is not a valid word.'
    word_score = 0
        
    print (letters_in_hand)
    display_hand(hand)
    word = input('\nWhat word would you like to guess?\n')
    if word == '!!':
        return None
    
    if not is_valid_word(word, hand, word_list): #if it's not a valid word
        print (not_valid)
        hand = update_hand(hand, word)
        
    else: #if a valid word, update hand and print score
        word_score = get_word_score(word, HAND_SIZE)                
        print (points.format(word, word_score))
        hand = update_hand(hand, word)
         

    return word_score

   
            # If the word is valid:

                # Tell the user how many points the word earned,
                # and the updated total score

            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
                
            # update the user's hand by removing the letters of their inputted word
            

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function

#play_hand(deal_hand(11), load_words())

#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    def choose_random_letter(hand):  
        letters = VOWELS + CONSONANTS
        random_letter = random.choice(letters)
        return random_letter
            
    random_letter = choose_random_letter(hand) 
    if letter in hand: #While the letter is already in hand or it's the same as they chose to swap, choose again
        while random_letter in hand or random_letter == letter:
            random_letter = choose_random_letter()
    
        hand[random_letter] = hand[letter]
        del(hand[letter])
        return hand
    else: # if they chose a letter that they didn't have in their hand
        return hand

#hand = {'a':1, 'b':2, 'c':1}
#substitute_hand(hand, 'g')


    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    total_score_message = 'Your total score is: {}'
    replay_message = 'Would you like to replay your hand? You only get to replay once during the game! Enter Y or N:'
    sub_message = '\nWould you like to substitute one of your letters for another? (This can only be done once during the game): Y or N\n'
    sub_letter = 'Which letter in your hand would you like to substitute?:\n'
    print ('Welcome to the 6.00 Word Game! Exit at any time by entering your word guess as: \n!!\n\nYou can use a wildcard (*) to replace a VOWEL only. Play the wildcard by entering * in place of the vowel.\n \nIf you enter an invalid word or forget to use the * key for your wildcard, you will still lose all valid cards you tried to play.\nLets begin.\n')

    hands_left = None
    while not isinstance(hands_left, int):
        try:
            hands_left = input('\nHow many hands would you like to play in this game?\n')
            hands_left = int(hands_left)        
        except ValueError:
            print ('You have not entered a valid number.')
    
    game_score = 0
    replay_used = False
    sub_used = False
    hand_score = 0
    words = load_words()
   
    while hand_score is not None and hands_left != 0:
        print ('The letters in your hand are:')        
        hand = deal_hand(HAND_SIZE)
        original_hand = dict(hand)
        if sub_used is False: #If it's not the first hand, ask if you want to substitute a letter
            display_hand(hand)            
            substitute = input(sub_message)
            if substitute.lower() == 'y':
                new_letter = input(sub_letter)
                substitute_hand(hand, new_letter)
                sub_used = True
            else:
                print ('\nNo substitutions have been made.')
         
        try:
            hand_score = (play_hand(hand, words)) #play hand
            game_score = (game_score + hand_score)
        except TypeError:
                print ('Exiting the game.', total_score_message.format(game_score))
                return None
        #if hand_score is None: #if you decided to quit 
        if replay_used is False: #if you haven't used your replay
            replay = input(replay_message)
            if replay.lower() == 'y': #If you want to replay the hand, change replay_used to True and run play hand function with same letters
               hand_score = play_hand(original_hand, words)
               replay_used = True
            else:
                print ('This hand will not be replayed.\n')
                
        hands_left -= 1    
        print (total_score_message.format(game_score))           
                    
        """    
        if replay.lower() == 'y': #If you want to replay the hand, change replay_used to True and run play hand function
            replay_used = True
            hand_score = play_hand(original_hand, load_words())
        else:
            hand_score = play_hand(deal_hand(HAND_SIZE), load_words())
            if hand_score is None:
                print (total_score.format(game_score))
        game_score = hand_score + game_score
        print (total_score.format(hand_score))

  
    print ('replay_used =', replay_used, 'hand_score = ', hand_score, 'game_score =', game_score, ', original hand = ', original_hand)
        # TO DO... Remove this line when you implement this function
    """
(play_game(WORDLIST_FILENAME))

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
#if __name__ == '__main__':
 #   word_list = load_words()
  #  play_game(word_list)
