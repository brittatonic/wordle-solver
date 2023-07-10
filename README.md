## Python Z3 Wordle Solver

This repository contains a Python implementation of a Wordle solver using the Z3 libraries. 

The goal of this project is to implement the rules of Wordle into the Z3 solver to better understand how automated verification can be used
in development. Z3 is a SMT solver that uses propositional logic to determine if something is accurate and true. The first step is to instantiate a solver instance, in this program it is assigned to the variable `solver`. With the solver, contraints are then added, which includes the varaibles, and the rules. There are 4 rules in the Wordle game, words must be legal (no weird characters), the word is 5 letters, and the word is not plural (not a proven rule, but all wordles to date have never been a plural), and the player is allowed up to 6 guesses to get the word. 

The solver uses a simple dictionary and randomly draws the first word to guess. From there, the logic of checking the letters for placement takes place. There are 4 checks done on each guess: the letter is in the solution and is in the correct spot, the letter is in the solution but is in the wrong spot, the letter is not in the solution, and the letter appears more than once in the solution. 

As words are guessed, letters that are not in the solution are appended to a 'bad' dictionary such that words contain said letters are filtered from the guessing pool. For letters that do appear in the solution, if the letter is in the wrong spot, the index of the letter guessed will be set to false in the solver, while the other slots will remain as true indicating that the letter can go into one or more of said spots. If the letter is in the correct spot, and only appears once, the index of that variable is then set to true and all other spots are set to false indicating that letter cannot lie in any other spot. If a letter appears more than once, all instances of the letter in the correct spot is set to true, and all instances of the letter in the wrong spot is set to false. 

The process of the solver can go for up to a maximium of 6 iterations to solve the word, if it is not solved by the 6th guess, the program will move on to the next word in the dictionary and a flag indicating correctness is set to false. 

Once all wordles have been attempted, a .csv file is created to store all the results from the process. 

The dictionary of wordle words was created using a BeautifulSoup webscraper on a site that is updated daily with each word. The guessing dictionary was downloaded and is occasionally appeneded. 

The analysis script will use the .csv from the solver to create a time analysis, and histograms of how the solver did. 

