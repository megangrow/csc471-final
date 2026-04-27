# client player
import socket
import json

# connect to server
host, port = '127.0.0.1', 5010
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# receive current_state dictionary from server
def recv():
    buffer = b""
    while len(buffer) < 4:
        buffer += client.recv(4 - len(buffer))
    length = int.from_bytes(buffer, "big")
    buffer = b""
    while len(buffer) < length:
        buffer += client.recv(length - len(buffer))
    return json.loads(buffer.decode())

def pretty_print(state):
    print("Turns remaining: " + str(state["turns_left"]))
    print("Mistakes remaining: " + str(6 - state["mistakes"]))
    print(state["display_word"])
    print(state["image"])
    print("\n\n---------------------------------------\n")

if __name__ == "__main__":
    try:
        state = recv()
        while not state["complete"]: # while the game is going
            pretty_print(state)
            while True:
                letter = input(state["msg"]).upper() # enter a letter
                if len(letter) == 1: # make sure it's only one letter
                    break
                print("Only enter one letter!")

            client.send(letter.encode()) # send the letter back to the server
            state = recv()

        print(state["display_word"])
        print(state["image"])
        print(state["msg"])

    except (KeyboardInterrupt, ConnectionResetError, BrokenPipeError):
        print("Disconnected from server")
        exit()
