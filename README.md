# CSC471-final

## Overview + Purpose
The purpose of this project is to allow a pair of people to play Hangman over the network.

## Project Features
One player (the server, Player S) will begin by selecting a word that the other player (the client, Player C) to guess. Player C will then have the option to guess a letter. If the letter is correct, the displayed word is updated. If the letter is incorrect, another piece is added to the hangman. Once the word is guessed, the attempts are used up, or the hangman is complete, the program will exit, allowing the players to re-run (either as the same player or different). After every two mistakes, Player S will have the ability to select a letter to re-hide.
