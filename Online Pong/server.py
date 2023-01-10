import socket
from _thread import *
import sys
import json

with open('netconfig.json', 'r') as f:
	config = json.load(f)

server = config[network]
port = config[port]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



try:
	s.bind((server, port))

except socket.error as e:
	str(e)

s.listen(2)
print("Waiting for connection, Server Started")

def read_pos(str):
	if str is not None:
		str = str.split(",")
		return int(str[0]), int(str[1])

def make_pos(tuple):
    return str(tuple[0]) + "," + str(tuple[1])

pos = [(10, 200), (670, 200)]
def threaded_client(conn, player):
	conn.send(str.encode(make_pos(pos[player])))
	print(pos)
	reply = ""
	while True:
		try:
			data = read_pos(conn.recv(2048).decode())
			pos[player] = data

			if not data:
				print("Disconnected")
				break
			else:
				if player == 1:
					reply = pos[0]
				else:
					reply = pos[1]
				print("Received: ", data)
				print("Sending : ", reply)

			conn.sendall(str.encode(make_pos(reply)))
		except:
			break

	print("Lost Connection")
	conn.close()

currentplayer = 0
while True:
	conn, addr = s.accept()
	print("Connected to:", addr)

	start_new_thread(threaded_client, (conn, currentplayer))
	currentplayer += 1


