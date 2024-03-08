
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
clients = [] #Stores the client (well call them ID's)
aliases = [] #Stores the aliases of the clients
passw=""
print('Server is up')

#The below function handles the transfer of messaages from one client to all other client
def broadcast(message,clientx="",aliasx="Server".encode('utf-8')):
    #Iterate through the list of clients but skip the sending client (As we dont want to send the same message to the one who sent it in the first place)
    for client in clients:
        if client != clientx:
            now = datetime.now()
            current_time = ("<"+now.strftime("%H:%M:%S")+">").encode('utf-8')
            client.send(current_time+aliasx+":".encode('utf-8')+message)
            
#This function handles the sending of files to the other clients and works in a similar way as above
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
            #Recieves a message from a client and then extracts the corresponding client id and alias
            index = clients.index(client)
            alias = aliases[index]
            dmessage=message.decode('utf-8')
            print(dmessage)
            #Handle the EXIT command here
            if(dmessage==':Exit'):
                print("Exiting");
                client.send(":Exit".encode("utf-8"));
                client.close();
                raise ValueError("Invalid value")
            #Here we handle the sending of files to the clients
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
            #Broadcast of normal messages
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
        #here we handle the setting of password for the first client
        client.send("Password?".encode('utf-8'))
        passwst=client.recv(1024)
        if not clients:
            passw=passwst
            client.send("Password Set Successfully".encode('utf-8'))
        #And the authentication of the password entered by other clients
        else:
            if passw==passwst:
                client.send("Welcome...".encode('utf-8'))
            else:
                client.send("Incorrect Password".encode('utf-8'))
                client.close()
                continue
        #Requesting for the clients alias and confirming connection to the chat room
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
