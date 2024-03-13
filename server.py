
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
dm=[]
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
def dmsend(index,aliasx,message):
    now = datetime.now()
    current_time = ("<"+now.strftime("%H:%M:%S")+">").encode('utf-8')
    dm[index].send(current_time+aliasx+" (DM):".encode('utf-8')+message)
#This function handles the sending of files to the other clients and works in a similar way as above
def broadcastfile(dmessage,clientx,aliasx):
    print("HERE1")
    for client in clients:
        if client != clientx:
            print("HERE2")
            client.send(dmessage.encode("utf-8"))
            fname="1"+dmessage[6:]
            print("HERE3")
            with open(fname,'rb') as f:
                while True:
                    data=f.read(2048)
                    # print(data)
                    if not data:
                        break
                    client.send(data)
            client.send("***END***".encode('utf-8'));
    print("File Sent")
    os.remove("1"+dmessage[6:])
        
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
            #Switching between messaging one client and all the clients handled here
            elif(dmessage[0:3]==':Dm'):
                print("DMING")
                dmal=dmessage[4:].encode('utf-8')
                #print(dmal)
                if(dmal=="All".encode('utf-8')):
                    dm[index]=None
                    print("All");
                    client.send("Messaging everyone".encode('utf-8'))
                elif dmal in aliases and dmal!=alias:
                    print("Found")
                    client.send("Direct Messaging ".encode('utf-8')+dmal)
                    index2=aliases.index(dmal)
                    dm[index]=clients[index2]
                else:
                    print("Not found")
                    client.send("Alias Not found".encode('utf-8'))
            #Here we handle the sending of files to the clients
            elif(dmessage[0:5]==':File'):
                print("Recieving File")
                fname="1"+dmessage[6:]
                with open(fname,'wb') as f:
                    while True:
                        data=client.recv(2048)
                        if data==("***END***".encode("utf-8")):
                            break
                        f.write(data)
                        #print(data)
                print("Recieved File")
                print("File sent")
                broadcastfile(dmessage,client,alias)
            #Broadcast of normal messages
            else:
                if(dm[index]==None):
                    broadcast(message,client,alias)
                    print("Broadcasted");
                else:
                    dmsend(index,alias,message)
        except:
            print("Except");
            index = clients.index(client)
            clients.remove(client)
            if dmessage != ":Exit":
                client.close()
            alias = aliases[index]
            broadcast(alias+'has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            dm.pop(index)
            break

def receive():
    while True:
        client, address = server.accept()
        print('connection is established with',str(address))
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
        time.sleep(1)
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        dm.append(None)
        print('The alias of this client is ',(alias.decode('utf-8')))
        broadcast(alias+' has connected to the chat room'.encode('utf-8'), client)
        client.send('\nServer: You are now connected!\n'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()
