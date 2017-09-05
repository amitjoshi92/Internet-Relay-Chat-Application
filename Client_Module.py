#*************************************************************************************************
#Name            :    Amit Joshi
#Project name    :    Internet Relay Chat Application. 
#Project Guide   :    prof : Nirupama Bulusu
#School Name     :    Portland State University
#Reference Used  :    https://www.tutorialspoint.com/python.
#**************************************************************************************************
import select
import socket
import sys
import Functionality_Module

if len(sys.argv) < 2:
    print("Please provide Host!")
    sys.exit(1)
else:
    server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          # Connecting to Server on the port 1234.
    server_connection.connect((sys.argv[1], 1234))

print("Connected to server\n")
msg_prefix = ''

socket_list = [sys.stdin, server_connection]

while True:
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    for s in read_sockets:
        if s is server_connection:
            msg = s.recv(4096)
            if not msg:                                                
			       #If no response from the server the it implies that sever is down.
                print("Server is Down! We are looking into it. We appricaite your patience!")   
                sys.exit(2)
            else:
                if msg == Functionality_Module.QUIT_STRING.encode():
                    sys.stdout.write('Bye\n')
                    sys.exit(2)
                else:
				     #  Take user name as Input.
                    sys.stdout.write(msg.decode())
                    if 'Please type in your name' in msg.decode():
                        msg_prefix = 'username: '
                    else:
                        msg_prefix = ''
        else:
            msg = msg_prefix + sys.stdin.readline()
            server_connection.sendall(msg.encode())