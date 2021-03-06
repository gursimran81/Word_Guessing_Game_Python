"""
    File name: guess.py
    Author: Gursimran Singh
    Python Version: 3.7
    Date Created: 17/05/2019
"""


import random
import sys

from game import Game
from stringDatabase import StringDatabase


class Guess:
    """Class Guess to represent the game of guess

        Attributes:
            words_list (str): The random word for each game
            random_word: The number of game
            game_Obj: The game.py object list
            tuple_word: the word to be displayed on the screen
            missed_letters: The number of missed letters
            game_count: the number of game
            status: status of the game
            end_game: The end_game flag
            total_score: The final score of the game
            frequency_words: Frequency of the words
            number_of_times_letter_requested: number_of_times_letter_requested

    """
    def __init__(self):
        """Guess init method"""
        self.words_list = StringDatabase().load_file()
        self.random_word = "random"
        self.game_Obj = []
        self.tuple_word = ['-', '-', '-', '-']
        self.bad_guesses = 0
        self.missed_letters = 0
        self.game_count = 1
        self.status = None
        self.end_game = False
        self.total_score = 0
        self.frequency_words = StringDatabase().get_frequencies()
        self.number_of_times_letter_requested = 0

    def get_random_word(self):
        """The getter to get random word from the list"""
        self.random_word = random.choice(self.words_list)
        print(self.random_word)

    def set_tuple_letter(self, index, letter):
        """Method to set the letter on the display as user guesses"""
        self.tuple_word[index] = letter
        temp_word = ''
        for w in self.tuple_word:
            temp_word += w

        if temp_word == self.random_word:
            self.status = 'Success'
            self.end_game = True

    def end_game_func(self):
        """Method to reset values when the game ends"""
        self.create_new_game_obj()
        self.game_count += 1
        self.tuple_word = ['-', '-', '-', '-']
        self.status = None
        self.end_game = True
        self.get_random_word()
        self.bad_guesses = 0
        self.missed_letters = 0
        self.total_score = 0

    def print_tuple_current_guess(self):
        """Method to print the current guess"""
        print("Current Guess: ", self.tuple_word)

    @staticmethod
    def print_gave_up(self):
        """Static methof to print the gaveup message"""
        print('$' * 50)
        print('You Gave Up! \n Want to Play Again?\nThe word was: "{}"'.format(self.random_word))
        print('%' * 50)

    @staticmethod
    def print_success(self):
        """Static methof to print the Success message"""

        print('$' * 50)
        print('SUCCESS! You Guessed It!\nThe word is: "{}"\n Want to Play Again?'.format(self.random_word))
        print('%' * 50)

    def calc_gaveup_score(self):
        """The method to calculate the gaveup score"""
        temp_w = []
        for w in self.tuple_word:
            if w != '-':
                temp_w.append(w)

        for l in temp_w:
            self.total_score -= round(float(self.frequency_words[l]), 2)

    def cal_score(self):
        """The method to calculate the common score"""
        index = []
        for w, i in zip(self.tuple_word, range(len(self.tuple_word))):
            if w == '-':
                index.append(i)

        for i in index:
            self.total_score += round(float(self.frequency_words[self.random_word[i]]), 2)

    def cal_success_score(self):
        """Method to calculate success score"""

        if self.number_of_times_letter_requested > 0:
            self.total_score = self.total_score+1/self.number_of_times_letter_requested

        for i in range(self.bad_guesses):
            self.total_score *= 0.9

    def print_menu(self):
        """Method for printing the menu each time the game starts"""
        self.get_random_word()
        loop = 1
        while loop == 1:
            if self.status == 'Success':
                self.print_success(self)
                self.end_game_func()

            if self.status == 'Gave up':
                self.print_gave_up(self)
                self.end_game_func()

            for o in self.game_Obj:
                print(o)

            self.end_game = False

            print('*' * 20 +
                  ' The great guessing game ' +
                  '*' * 20 + '\n')
            self.print_tuple_current_guess()
            print("\n\ng = guess, t = tell me, l for a letter, and q to quit\n")
            ans = input("Please select a choice.")

            if ans == 'l':
                self.guess_letter()

            elif ans == 'g':
                self.guess_word()

            elif ans == 't':
                print('The word is: "{}"\n'.format(self.random_word))
                self.status = 'Gave up'
                self.cal_score()
                self.calc_gaveup_score()
                self.end_game = True

            elif ans == 'q':
                self.quit_func()

            else:
                print("Wrong choice Selected! Please Try again!")

    def guess_word(self):
        """THis checks if the user correctly guessed the word"""
        guessed_word = input('Enter the whole word.')
        if guessed_word == self.random_word:
            print("You Guessed it!")
            print('The word is: "{}"!\n'.format(self.random_word))
            self.status = 'Success'
            self.cal_score()
            self.cal_success_score()
        else:
            print("Wrong! Sorry try again!")
            self.bad_guesses += 1

    def guess_letter(self):
        """THis checks if the user correctly guessed the letter"""
        self.number_of_times_letter_requested += 1
        letter = input('\n\nEnter a letter.')
        indexes = [index for index, element in enumerate(self.random_word) if element == letter]
        count = 1
        # print(indexes)
        if letter in self.random_word:
            count += 1
            if count >= 3:
                self.cal_score()
            print("You found {} letter(s)! : ".format(len(indexes)))
            if len(indexes) > 1:
                for i in indexes:
                    self.set_tuple_letter(i, letter)
            else:
                self.set_tuple_letter(self.random_word.find(letter), letter)

        else:
            print("Sorry no such letter found!")
            self.missed_letters += 1

    def quit_func(self):
        """Function to quit the game"""
        print("Sorry to See you go! Here is your Game Summary:\n\n")
        print('Game\tWord\t\tStatus\t   Bad_Guesses\t  Missed_Letters\t  Score\n')
        print('-'*90)

        for o in self.game_Obj:
            print(str(o)+'\n')

        sys.exit()

    def create_new_game_obj(self):
        """Function to create the new game object after each round"""
        gameObj = Game()
        gameObj.bad_guesses = self.bad_guesses
        gameObj.game_number = self.game_count
        gameObj.words = self.random_word
        gameObj.missed_letterss = self.missed_letters
        gameObj.statuss = self.status
        gameObj.scores = self.total_score

        self.game_Obj.append(gameObj)


if __name__ == '__main__':
    guess_game = Guess()

    guess_game.print_menu()
