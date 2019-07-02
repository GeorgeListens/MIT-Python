# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Lynette

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 3

SCRABBLE_LETTER_VALUES = {
    '*':0,'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# Provided function

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
    # Score = partA * partB
    
    #partA
    sum=0        
    word = word.lower(); # make all chars in string lower case
    for c in word:
        sum += SCRABBLE_LETTER_VALUES[c]

    #partB
    total = 7*len(word) - 3*(n-len(word))
    if 1>total:
        total=1

    # return Score = partA * partB
    return sum*total
        

#
# Display_hand prints out the letter in a hand
# Provided function
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
# Get a hand via a random choice of vowels and consonants
# Provided Function
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
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    # Put wildcard into vowels place in hand
    # For vowels, start range at "1" since "0" occupied by wildcard
    hand['*'] = 1; # give first element wildcard
    for i in range(1, num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    # Fill remaining positions with consonants
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

    #First make copy of original hand to modify
    mod_hand = hand.copy()

    # check if the letter in the word exists in the given hand
    # if not, give it a defalut value of zero
    for letter in word:
        if(mod_hand.get(letter, 0) != 0):
            mod_hand[letter] -= 1 # decrement by 1

    # take out the zero value elements from modified hand dictionary (mod_hand)
    empty_keys = [k for k,v in mod_hand.items() if v==0]
    for k in empty_keys:
        del mod_hand[k]

    return mod_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    
    #First set all letters to lower case since all functions operate on lower
    word = word.lower(); # make all chars in string lower case
    
    if '*' in word: # Check if valid word with wildcard is present
        if not valid_word_with_wildcard(word, word_list):
            return False
    else: # Check if valid word with no wildcard
        if not word_in_valid_list(word, word_list):
            return False
  
                
    # Next Check if each letter in the word exists in the hand
    # if it does, check the value (frequency)
    mod_hand = hand.copy(); # make a copy of the hand    
    word_dict = get_frequency_dict(word); # get dictionary of word (for repeated letters)

    for letter in word_dict:
        if(mod_hand.get(letter, 0) == 0): # if letter in word is not present in hand
            return False
        elif (mod_hand[letter] < word_dict[letter]): # if num occurances of letter in word
            return False                             # greater than num occurances in hand

    return True;

# Sub vowels for wildcard.  Checked for presence of wildcard before calling function
# If a valid word is made, then return True
def valid_word_with_wildcard(word, word_list):
    result = word.find('*') # get index of wildcard
    for vowel in VOWELS:
        word = word[:result] + vowel + word[result+1:] # at index, sub in vowel for wildcard
        if word_in_valid_list(word, word_list): 
            return True
    # If no valid word formed, then return False
    return False

# Check if word is present in word_list
def word_in_valid_list(word, word_list):
    if word in word_list:
        return True
    else:
        return False


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    # len() returns total length of dictionary or number of items in dictionary
    return len(hand)
       

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
     # Keep track of the total score
    totalPoints=0
    
    # As long as there are still letters left in the hand:
    while len(hand)>0:
        # Display the hand
        print(do_current_hand_line(hand));
        
        # Ask user for input
        print('Please enter a word or "!!" to exit the hand (or "##" to exit entirely):');
        word=input() # Capture user input into variable "word"
        word = word.strip().lower()
        
        # If the input is '!!', then exit the hand being played
        # If input is '##', then exit the game
        if word == '!!' or word == '##':
            break;                     
            
        # Otherwise
        else:
            if is_valid_word(word, hand, word_list):
                # Tell the user how many points the word earned,
                # and the updated total score
                # eg. "fix" earned 117 points. Total: 117 points
                
                wordPoints = get_word_score(word, len(hand))# Calc points for word
                totalPoints += wordPoints # Add wordPoints to totalPoints

                data = {'inputWord':word, 'score':wordPoints, 'total': totalPoints}
                print ('"{inputWord}" earned {score} points. Total: {total} points'.format(**data));
                print("\r");
                
            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print("That is not a valid word. Please choose another word.");
                print("\r");
                
        # update the user's hand by removing the letters of their inputted word
        hand = update_hand(hand, word)

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score       
    if len(hand)==0:
        prologue = "Ran out of letters."
    elif word == '!!' or word == '##':
        prologue = ""
        
    data = {'note': prologue, 'total':totalPoints}
    print("{note} Total score for this hand: {total}".format(**data));
    print("----------");

    # Return the total score as result of function
    ret_tuple = totalPoints, word
    return  ret_tuple 
          
#
# Build string for current_hand_line()
#
def do_current_hand_line(hand):
    line = "Current Hand: "
    
    for i in hand:
        for j in range(hand[i]):
            line += i
            line += ' '

    
    return line


#
# procedure used to substitute a letter in a hand
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
    # If the letter is not in the hand, return hand unchanged
    letter = letter.lower()
    if (hand.get(letter, 0) == 0):
        return hand
    
    # Make copy of current hand
    sub_hand = hand.copy()
    
    # Make a string of VOWELS string and CONSTANT string
    alphabet = VOWELS+CONSONANTS
    
    # Remove letters in hand from the alphabet
    for k in sub_hand:
        alphabet = remove_letter_from_string(alphabet, k)
        #print(alphabet);
        
    # Get new letter using random
    new_letter = random.choice(alphabet)
    
    # Add new letter and give (old) letter's value to it
    sub_hand[new_letter] = sub_hand[letter]

    # Delete (old) letter element
    del sub_hand[letter]

    #print(sub_hand);
    # Return changed hand
    
    return sub_hand
    
def remove_letter_from_string(s, letter):
    # get index of letter
    result = s.find(letter) 

    # remove the letter from the string
    s = s[:result] + s[result+1:]

    # return the modified string 
    return s
#
# Process user response to question
# Input: question
# User response: yes, no, or garbage
#
def query_question(question):
    response_not_okay = True

    while response_not_okay:
        print(question)
        response = input()
        response = response.lower().strip()
 
        if (response == "no"):
            response_not_okay = False
            ret_value = False
        elif (response == "yes"):
            response_not_okay = False
            ret_value = True
        else:
            print('Please enter "yes" or "no"')
            print("")

    return ret_value
#
# Ask user if letter substitution is desired
# If so, substitute letter into current hand and return revised hand
# Else, do not alter hand or letter_sub_available flag and return original variables values
#
def do_letter_sub_routine(hand):
    response_not_okay = True

    # Does user want to substitute a letter?
    if (query_question("Would you like to substitute a letter? (substitution available once)")):
        # if response is yes, then the one letter substitution option is used
        letter_sub_available = False
        
        while( response_not_okay):
            print('Which letter would you like to replace:');
            letter=input() # Capture user input into variable "word"
            letter = letter.strip().lower()

            #Check if the response is well conditioned
            if(len(letter)==1 and letter.isalpha()):
                response_not_okay = False
                hand = substitute_hand(hand, letter) # sub new letter into hand            
            else:
                print("Please enter a single letter from the current hand")
    else: # Since user doesn't want to sub a letter, the option remains available
        letter_sub_available = True

    # Build the response tuple
    response_tuple = letter_sub_available, hand
    return response_tuple

#
# Build a hand
#
def get_a_hand(letter_sub_available):
    hand = deal_hand(HAND_SIZE) # get a hand of letters            
    print(do_current_hand_line(hand)) # print out the current hand
    print("");

    # Process letter substitution
    if(letter_sub_available):
        letter_sub_tuple = do_letter_sub_routine(hand)
        # tuple unpacking
        letter_sub_available, hand = letter_sub_tuple
        print("");

    # record the existing hand for future replay_hand request
    previous_hand = hand 

    # Build the tuple
    the_tuple = hand, letter_sub_available, previous_hand

    #reutrn the tuple
    return the_tuple
  

#
#  Problem #6: Playing a game
#   
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
 
    num_hands_played = 0 # number of hands played thus far
    points = 0 # points per hand
    total_points = 0 # accumulated points over number of hands
    previous_points = 0 # points from previous hand
    previous_hand = {} # empty dictionary to record previous_hand

    #flags
    first_hand = True # first hand in game
    replayed_hand = False # replay hand once
    letter_sub_available = True # sub letter once
    include_replayed_hand_points = True # include replayed_hand points once

     # Ask user for input
    print('');
    print('Rules of the game:');
    print("Any vowel may be assumed for '*'.");
    print('A letter may be substituted once and a hand may be replayed once.');
    print('A replayed hand does not count towards the number of games played.');
    print('The letter substitution option is not available in a replayed hand.');
    print('However, if a letter is substituted in the original hand, then that');
    print('hand is presented as the hand to be replayed.');
    print('The highest score between the replayed hand and the original hand will count.');
    print('To exit, please enter "##" when asked to enter a word');
    print('');

    # Get user input and convert response to int
    print("Let's start! Please enter the total number of hands you'd like to play:");
    response=input() 
    total_hands_to_play=int(response)

    #
    # Here we play the game
    #
    while num_hands_played < total_hands_to_play:
        #
        # First get the hand to be played
        #
        # If it's the first hand in the game or a hand where replaying a hand has already been used
        # then do the following
        if(first_hand or replayed_hand):
            first_hand = False 
            num_hands_played += 1 # increment num_hands_played
            # Get a hand, process letter substitution, return tuple and unpack it
            hand_tuple = get_a_hand(letter_sub_available)
            hand, letter_sub_available, previous_hand = hand_tuple
        #
        # Otherwise, if it's a hand where replaying a hand is an option
        #
        elif (not replayed_hand):
            if(query_question("Would you like to replay the hand? (replay available once)")):
                replayed_hand = True # flip the flag
                hand = previous_hand # the previous hand is to be replayed
                # replay hand is not counted in total_hand_to_play
                print("");
            else: # decline replay means get a new hand
                num_hands_played += 1 # increment num_hands_played
                # Get a hand, process letter substitution, return tuple and unpack it
                hand_tuple = get_a_hand(letter_sub_available)
                hand, letter_sub_available, previous_hand = hand_tuple
       
        #
        # Second, now that the hand is set, play a game
        #
        game_tuple = play_hand(hand, word_list)
        points, word = game_tuple

        #
        # Process results of game - points scored and word entered
        # Check for exit request
        #
        if word == '##':
            num_hands_played = total_hands_to_play # exit while loop cleanly
         
        # for replayed_hand,
        # use highest score of original hand or replayed hand to add to total_points      
        if (replayed_hand and include_replayed_hand_points):
            include_replayed_hand_points = False # flip flag now that it's been included once
             
            if points>previous_points:
                total_points -= previous_points
                total_points += points
                
        # Accumulate points in total_points and record previous_points
        else:
            total_points += points
            previous_points = points
           
    #
    # End of game (after the while loop) 
    #
    data = {'total':total_points}
    print("Congratulations! The total score over all hands is {total}".format(**data));

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
