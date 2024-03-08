
#Client.py
import threading
import socket
import sys
alias=""
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))
exit_flag=True
def client_receive():
    global exit_flag
    global alias
    while exit_flag:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "Password?":
                password=input('Enter the Password>>> ');
                client.send(password.encode('utf-8'))
                continue
            elif message == "alias?":
                alias = input('Choose an alias >>> ')
                client.send(alias.encode('utf-8'))
                send_thread.start()
                continue
            elif message == "Incorrect Password" or message ==":Exit":
                if message == "Incorrect Password":
                    print("You entered the incorrect password")
                print("Exiting the program")
                exit_flag=False
                client.close();
                continue
            elif message[0:5]==":FILE":
                fname="2"+message[5:]
                with open(fname,'wb') as f:
                    while True:
                        data=client.recv(2048)
                        if data=="***END***".encode("utf-8"):
                            break
                        f.write(data)
                        #print(data)
                print("Recieved File "+message[5:])
            else:
                print(message)
        except:
            print('Error!')
            exit_flag=False
            client.close()
            break

def client_send():
    global exit_flag
    while exit_flag:
        message = input("")
        client.send(message.encode('utf-8'))
        if message[0]==':' and message!=":Exit":
            print("Sending File");
            fname=message[1:]
            with open(fname,'rb') as f:
                while True:
                    data=f.read(2048)
                    #print(data)
                    if not data:
                        break
                    client.send(data)
            client.send("***END***".encode('utf-8'));
            print("File sent")
            
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
