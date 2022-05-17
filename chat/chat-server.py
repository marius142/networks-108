import socket, threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5378
separator_token = "<SEP>"

client_name = ''
client_book = {}
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# make the port as reusable port
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((SERVER_HOST, SERVER_PORT))
sock.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cl):
    while True:
        try:
            recipient = ''
            recipient_no = 0
            recipient_addr = ''
            # keep listening for a message from `cl` socket
            msg = cl.recv(1024).decode()
            msg = msg.replace(separator_token, ": ")

            if "-FROM" in msg:
                msg = msg.replace("-FROM", '')
                client_name = msg.split(' ')[1]
                client_book[client_name] = cl
                print(client_book)
            elif "WHO" in msg:
                msg = "WHO-OK"
                msg += ''.join(client_book)
            elif "SEND" in msg:
                cl.send(("SEND-OK").encode())
                client_name = msg.split(' ')[1]
                client_book[client_name].send("DELIVERY " + msg.split(' ')[2])

                

            cl.send(msg.encode())

        except Exception as e:
            # client no longer connected, remove it from the set
            print(f"[!] Error: {e}")
            client_book.pop(client_name)

while True:
    # we keep listening for new connections all the time
    client, client_address = sock.accept()
    print(f"[+] {client_address} connected.")
    # add the new connected client to connected sockets

    threading.Thread(target=listen_for_client, args={client,}, daemon = True).start()

# close client sockets
for cl in client_sockets:
    cl.close()
# close server socket
sock.close()
