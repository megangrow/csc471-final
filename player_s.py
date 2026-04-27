# server player
import socket
import json

# set up server connection
port = 5010
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', port))
server.listen()
c, address = server.accept()
print(f"Connected with {address}")

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

# initial setup
def get_word():
    word = input("Enter a word: ")
    return list(word.upper())

def create_display_word(word):
    display_word = []
    for i in word:
        display_word.append("_")
    return display_word

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

# make updates
def change_picture():
    current_state["mistakes"] += 1
    if current_state["mistakes"] % 2 == 0 and current_state["mistakes"] != 0:
        current_state["hide_turn"] = True

    current_state["image"] = hangman_pics[current_state["mistakes"]]

def update_state(l):
    updated = False
    current_state["turns_left"] -= 1
    for i in range(len(current_state["word"])):
        if (l == current_state["word"][i]):
            current_state["display_word"][i] = l
            updated = True

    if not updated:
        change_picture()
    return

# option for server to rehide certain letters after every 2 mistakes
def rehide_letter():
    if all(c == "_" for c in current_state["display_word"]):
        current_state["hide_turn"] = False
        return

    choice = input("Choose a letter to rehide: ").upper()
    for i in range(len(current_state["word"])):
        if (choice == current_state["word"][i]):
            current_state["display_word"][i] = "_"

    current_state["hide_turn"] = False

def check_state():
    if current_state["mistakes"] > 5 or current_state["turns_left"] == 0:
        current_state["complete"] = True
        current_state["msg"] = "You lose!!!!"

    if current_state["hide_turn"]:
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
    create_initial()

    while not current_state["complete"]:
        send(c, current_state)
        letter = recv(c)

        update_state(letter)
        check_state()
        pretty_print()

    send(c, current_state)


