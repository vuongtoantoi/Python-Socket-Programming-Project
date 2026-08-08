import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(socket.gethostname())
server.bind((ip,3333))
server.listen(10)

clients = []
nicknames = []

def broadcast(msg):
    for client in clients:
        client.send(msg)

def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                #raise ConnectionResetError  # Client disconnected
                index = clients.index(client)
                clients.remove(client)
                broadcast(f'{nickname} left the chat!'.encode('utf-8'))
                nicknames.remove(nickname)
                break
            
            print(f'{msg.decode("utf-8")}')
            broadcast(msg)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break
def receive():
    while True:
        client, addr = server.accept()
        print(f'Connected with {str(addr)}')
        try:
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            nicknames.append(nickname)
            clients.append(client)
            print(f'Nickname of the client is {nickname}')
            broadcast(f'{nickname} joined the chat'.encode('utf-8'))
            #client.send('Connected to the server'.encode('utf-8'))
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except:
            print*('Error during client setup')
            client.close()
if __name__ == "__main__":
    print('Server is running...')
    receive()
