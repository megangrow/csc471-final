# CSC471-final

## Overview + Purpose
The purpose of this project is to allow a pair of people to play Hangman over the network.

## Project Features
One player (the server, Player S) will begin by selecting a word that the other player (the client, Player C) to guess. Player C will then have the option to guess a letter. If the letter is correct, the displayed word is updated. If the letter is incorrect, another piece is added to the hangman. Once the word is guessed, the attempts are used up, or the hangman is complete, the program will exit, allowing the players to re-run (either as the same player or different). After every two mistakes, Player S will have the ability to select a letter to re-hide.

## Running the Program and Playing the Game
Using two different computers or terminals, run your selected program (either player_s.py or player_c.py) by typing ```python3 player_s.py```. Words and letters can be entered directly into the terminal and submitted by pressing the 'Enter' key. The server must run their program first, otherwise the client will have nothing to connect to.

## Code Examples
Example of server connection code using TCP:
```
port = 5010
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', port))
server.listen()
c, address = server.accept()
print(f"Connected with {address}")
```

Example of game logic (from server):
```
create_initial()

while not current_state["complete"]: # while the game is going
  send(c, current_state) # send the current state to the client
  letter = recv(c) # receive the guessed letter from client

  update_state(letter) # remove 1 turn, if correct: update the display_word to reveal that letter, else, increase by 1 mistake, update the hangman image
  check_state() # see if the client has won or lost, or if it's the turn for the server to rehide a letter (if so, call rehide_letter())
  pretty_print() # print the current game board to server

send(c, current_state) # at the end, send the current state to the client
```
