#*************************************************************************************************
#Name            :    Amit Joshi
#Project name    :    Internet Relay Chat Application. 
#Project Guide   :    prof : Nirupama Bulusu
#School Name     :    Portland State University
#Reference Used  :    https://www.tutorialspoint.com/python.
#**************************************************************************************************
from Functionality_Module import Functions, Room, User
import Functionality_Module
import select
import socket
import sys

host_address = sys.argv[1]
listen_socket = Functionality_Module.create_socket((host_address, 1234))      # Creating socket and attaching it to Host at port number 1234.

functions = Functions()
connection_list = []
connection_list.append(listen_sock)

while True:
    
    read_users, write_users, error_sockets = select.select(connection_list, [], [])
    for user in read_users:
        if user is listen_socket:
            new_socket, add = user.accept()
            new_user = User(new_socket)
            connection_list.append(new_user)
            functions.welcome_new(new_user)

        else:
            msg = user.socket.recv(4096)
            if msg:
                msg = msg.decode().lower()
                functions.command_execution(user, msg)

            else:
                user.socket.close()
                connection_list.remove(user)
                print 'Sorry! User ' + str(user.name) + '  is not available at the moment'



    for sock in error_sockets:
        sock.close()
        connection_list.remove(sock)
