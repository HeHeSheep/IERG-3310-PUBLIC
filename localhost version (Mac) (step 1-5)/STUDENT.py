import socket
import random
import time


localhost = '' 
server_IP = 'localhost' # setting IP address
port = 3310  #port number to connect to

print ("Creating s_1")
# create a socket object
s_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect the client socket to the server
s_1.connect((server_IP, port))
print ("s_1 connected to server at port: ", port)

# Step 2: send a message to the server
print ("Sending message to server")
s_1.send("1155176266".encode())

# Step 3: receive a response from the server and creater a new socket
print ("Waiting for response")
response = s_1.recv(1024)
print ("Response: ", response.decode())

# Use response as port number to create new socket listenSocket
print ("Creating s_2")
listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listenSocket.bind((localhost, int(response.decode())))
listenSocket.listen(1)
print("Done")

# accept connections from outside
s_2, address = listenSocket.accept()
auto_serverIP = address[0] #server IP address from s_2 accepted data
print ("\nClient from %s at port %d connected" %(auto_serverIP,address[1]))
listenSocket.close()


# Step 4: Receive “fffff,eeeee.” from s_2 and create UDP socket s_3
response = s_2.recv(1024)
print ("Response: ", response.decode()) #fffff,eeeee. succeed

fffff = response.decode()[0:5] #filter out fffff
eeeee = response.decode()[6:11] #filter out eeeee
print ("fffff: ", fffff)
print ("eeeee: ", eeeee)

# create a socket object
addr = (auto_serverIP, int(eeeee))
s_3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s_3.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #copy from provided code
s_3.bind(('0.0.0.0', int(eeeee)))

# send a message to the server
message = random.randint(6, 9) #send a random variable 5<num<10
message_to_send = str(message)
s_3.sendto(message_to_send.encode(), (auto_serverIP, int(fffff)))


# Receive message from server 
string_xxx , addr = s_3.recvfrom(message * 10)
print ("Received message: ", string_xxx.decode())

# Step 4 completed

# step 5: send string_xxx to server by s_3 port fffff
for i in range(1, 6): #send 5 times
    print ("UDP packet ", i, " sent")
    s_3.sendto(string_xxx, (auto_serverIP, int(fffff)))
    time.sleep(1) #wait for 1 second
print ("All packet sent")
# Step 5 completed

