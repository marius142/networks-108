import socket, threading

SERVER_HOST = "192.168.0.104"
SERVER_PORT = 5378
separator_token = "<SEP>"

client_name = ''
client_book = {}
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
active_connections = {sock}

# make the port as reusable port
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((SERVER_HOST, SERVER_PORT))
sock.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cl):
    sender = ''
    while True:
        try:
            # keep listening for a message from `cl` socket
            msg = cl.recv(1024).decode()
            msg = msg.replace(separator_token, ": ")

            if "-FROM" in msg:
                client_name = msg.split(' ')[1]
                if client_name in client_book:
                    msg = "IN-USE\n"
                else:
                    msg = msg.replace("-FROM", '')
                    client_name = client_name.replace('\n', '')
                    sender = client_name
                    client_book[client_name] = cl
            elif "WHO" in msg:
                msg = "WHO-OK"
                for key in client_book:
                    msg += key + ", "
                msg = msg[:-2]
                msg += "\n"
            elif "SEND" in msg:
                client_name = msg.split(' ')[1]
                #SEND client_name msg
                #DELIVERY client_name msg
                if client_name in client_book:
                    recipient = client_book[client_name]
                    recipient.send(("DELIVERY" + sender + ": " + msg.split(' ')[2] + '\n').encode())
                    msg = "SEND-OK\n"
                else:
                    msg = "UNKNOWN\n"

            cl.send(msg.encode())

        except Exception as e:
            # client no longer connected, remove it from the set
            print(f"[!] Error: {e}")
            client_book.pop(client_name)

while True:
    # we keep listening for new connections all the time
    client, client_address = sock.accept()
    print(f"[+] {client_address} connected.")
    # add the client to the active connections listen
    active_connections.add(client)

    if len(active_connections) > 2:
        client.send(("BUSY\n").encode())

    threading.Thread(target=listen_for_client, args={client,}, daemon = True).start()

# close client sockets
for cl in client_sockets:
    cl.close()
# close server socket
sock.close()
