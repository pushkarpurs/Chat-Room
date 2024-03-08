
#Server.py
import threading
import socket
from datetime import datetime
import time
import os

host = '127.0.0.1'
port = 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []
passw=""
print('Server is up')

def broadcast(message,clientx="",aliasx="Server".encode('utf-8')):
    for client in clients:
        if client != clientx:
            now = datetime.now()
            current_time = ("<"+now.strftime("%H:%M:%S")+">").encode('utf-8')
            client.send(current_time+aliasx+":".encode('utf-8')+message)
def broadcastfile(dmessage,clientx,aliasx):
    print("HERE1")
    for client in clients:
        if client != clientx:
            print("HERE2")
            client.send((":FILE"+dmessage[1:]).encode("utf-8"))
            fname="1"+dmessage[1:]
            print("HERE3")
            with open(fname,'rb') as f:
                while True:
                    data=f.read(2048)
                    #print(data)
                    if not data:
                        break
                    client.send(data)
            client.send("***END***".encode('utf-8'));
    os.remove("1"+dmessage[1:])
        
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            index = clients.index(client)
            alias = aliases[index]
            dmessage=message.decode('utf-8')
            print(dmessage)
            if(dmessage==':Exit'):
                print("Exiting");
                client.send(":Exit".encode("utf-8"));
                client.close();
                raise ValueError("Invalid value")
            elif(dmessage[0]==':'):
                print("Recieving File")
                fname="1"+dmessage[1:]
                with open(fname,'wb') as f:
                    while True:
                        data=client.recv(2048)
                        if data=="***END***".encode("utf-8"):
                            break
                        f.write(data)
                        print(data)
                print("Recieved File")
                broadcastfile(dmessage,client,alias)
            else:
                broadcast(message,client,alias)
                print("Broadcasted");
        except:
            print("Except");
            index = clients.index(client)
            clients.remove(client)
            if dmessage != ":Exit":
                client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send("Password?".encode('utf-8'))
        passwst=client.recv(1024)
        if not clients:
            passw=passwst
            client.send("Password Set Successfully".encode('utf-8'))
        else:
            if passw==passwst:
                client.send("Welcome...".encode('utf-8'))
            else:
                client.send("Incorrect Password".encode('utf-8'))
                client.close()
                continue
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        client.send('\nyou are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
