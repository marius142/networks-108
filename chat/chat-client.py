import socket, threading, os, sys

SERVER_TARGET = '192.168.0.104'
SERVER_PORT = 5378

def listen(connection: socket.socket):
	while True:
		try:
			buf = ''
			msg = []
			while True:
				msg = connection.recv(1024).decode()
				buf += msg
				if '\n' in buf:
					if "HELLO" in buf:
						buf = buf.replace("HELLO", "Welcome")
						buf = buf.replace('\n', '!\n')
					elif "WHO-OK" in buf:
						buf = buf.replace("WHO-OK", "Online:\n")
					elif "SEND-OK" in buf:
						buf = "Message sent.\n"
					elif "UNKNOWN" in buf:
						buf = "User offline.\n"
					elif "DELIVERY" in buf:
						buf = buf.replace("DELIVERY", '')
					elif "IN-USE" in buf:
						buf = 'Name in use, please try again\n'
						print(buf)
						sys.stdout.flush()
						os.execl(sys.executable, sys.executable, *sys.argv)
					elif "BUSY" in buf:
						buf = 'Reached maximum number of clients.\n\tPlease try again later.'
						print(buf)
						os._exit(0)
					elif "BAD-RQST-HDR" in buf:
						buf = 'Last message contains an error in header.'
					elif "BAD-RQST-BODY" in buf:
						buf = 'Last message contains an error in body.'
					break
			print(buf)

		except Exception as e:
			print(f'Error receiving message: {e}')
			connection.close()
			break
	pass
def client():
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((SERVER_TARGET, SERVER_PORT))
		threading.Thread(target=listen, args=[sock], daemon = True).start()

		name = input("Enter name: ")
		handshake = f"HELLO-FROM {name}\n"
		sock.sendall(handshake.encode("utf-8"))

		while True:
			message = input()
			if "!quit" in message:
				break
			elif "!who" in message:
				message = "WHO"
			elif message[0] == '@':
				message = message.replace("@", "SEND ")
			sock.sendall(message.encode("utf-8"))

	except Exception as e:
		print(f"Error connecting to server socket: {e}")
		sock.close()
if __name__ == "__main__":
    client()
