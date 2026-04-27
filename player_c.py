# client player
import socket
import json

host, port = '127.0.0.1', 5010
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

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
    state = recv()
    while not state["complete"]:
        pretty_print(state)

        letter = input(state["msg"]).upper()
        client.send(letter.encode())
        state = recv()

    print(state["display_word"])
    print(state["image"])
    print(state["msg"])
