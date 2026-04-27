# server player
import socket
import json

# set up server connection using TCP
port = 5010
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', port))
server.listen()
c, address = server.accept()
print(f"Connected with {address}")

# dictionary of art for each hangman state
hangman_pics = [
    # 0 wrong
    """
  +---+
  |   |
      |
      |
      |
      |
=========""",
    # 1
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    # 2
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    # 3
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    # 4
    """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========""",
    # 5
    """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========""",
    # 6 — dead
    """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
========="""
]

# dictionary of the current state of the game
current_state = {
    "word": "",
    "display_word": "",
    "image": hangman_pics[0],
    "complete": False,
    "msg": "Guess a letter: ",
    "mistakes": 0,
    "turns_left": 0,
    "hide_turn": False,
}

# initial setup helper functions
def get_word(): # get word from server
    word = input("Enter a word: ")
    return list(word.upper())

def create_display_word(word): # fill in blanks based on word
    display_word = []
    for i in word:
        if i == " ":
            display_word.append(" ") # display spaces if space
        else:
            display_word.append("_") # display blank if letter
    return display_word

# create initial game state - client gets 5+number of letters turns to guess
def create_initial():
    current_state["word"] = get_word()
    current_state["display_word"] = create_display_word(current_state["word"])
    current_state["turns_left"] = len(current_state["word"]) + 5

# send and receive
def send(client, state):
    content = json.dumps(state).encode()
    length = len(content).to_bytes(4, "big")
    client.sendall(length + content)

def recv(client):
    return client.recv(1).decode()

# if the client guessed the wrong letter:
def wrong_guess_update():
    current_state["mistakes"] += 1 # update mistake count
    current_state["image"] = hangman_pics[current_state["mistakes"]]  # change hangman image
    # if they've made two (more) mistakes, let the server choose a letter to rehide
    if current_state["mistakes"] % 2 == 0 and current_state["mistakes"] != 0:
        current_state["hide_turn"] = True

# update every round
def update_state(l):
    updated = False
    current_state["turns_left"] -= 1 # use a turn
    for i in range(len(current_state["word"])):
        if (l == current_state["word"][i]): # if the letter is in the word, display
            current_state["display_word"][i] = l
            updated = True
    # if it isn't, update the wrong guess
    if not updated:
        wrong_guess_update()
    return

# option for server to rehide certain letters after every 2 mistakes
def rehide_letter():
    # make sure there's letters uncovered to rehide
    if all(c == "_" for c in current_state["display_word"]):
        current_state["hide_turn"] = False
        return

    choice = input("Choose a letter to rehide: ").upper()
    # loop through and re-hide the correct letter
    for i in range(len(current_state["word"])):
        if (choice == current_state["word"][i]):
            current_state["display_word"][i] = "_"
    current_state["hide_turn"] = False

# check to see if a win (word uncovered) /loss (6 mistakes or all turns used) condition has been met
def check_state():
    if current_state["mistakes"] > 5 or current_state["turns_left"] == 0:
        current_state["complete"] = True
        current_state["msg"] = "You lose!!!!"

    if current_state["hide_turn"]: # let server rehide letter if its that turn
        rehide_letter()

    if ("_" not in current_state["display_word"]):
        current_state["complete"] = True
        current_state["msg"] = "You win!!!!"
    return

def pretty_print():
    print(current_state["word"])
    print(current_state["display_word"])
    print("Turns remaining: " + str(current_state["turns_left"]))
    print("Mistakes: " + str(current_state["mistakes"]) + "/6")
    print("\n---------------------------------------\n")

if __name__ == "__main__":
    try:
        create_initial()

        while not current_state["complete"]: # while the game is going
            send(c, current_state)
            letter = recv(c)

            update_state(letter)
            check_state()
            pretty_print()

        send(c, current_state)

    except (KeyboardInterrupt, ConnectionResetError, BrokenPipeError):
        print("Disconnected from client")
        exit()
