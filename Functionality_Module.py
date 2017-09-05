#*************************************************************************************************
#Name            :    Amit Joshi
#Project name    :    Internet Relay Chat Application. 
#Project Guide   :    prof : Nirupama Bulusu
#School Name     :    Portland State University
#Reference Used  :    https://www.tutorialspoint.com/python.
#**************************************************************************************************
import socket
import sys

QUIT_STRING = '<$quit$>'
def create_socket(address):                              
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # 1st arg Socket domain Af_Inet, Sock_Stream which is for the connnection oriented protocol varition could be 
	s.setblocking(0)                                             # variation to this could be SOCK_DGRAM for the Connectionless protocol.
 	s.bind(address)                                              # Protocol argument which is set to zero in most cases. 
    s.listen(10)                                                 # Wait fot Client Connection and it can serve at max 10 connection.
    print("Connected to: ", address)                             # bind method binds address(Host machine and port name) to Socket.
    return s

class Room:
    def __init__(self, name):
	     
        self.users = []
        self.name = name
      
	  # To welcome the new User. This funcation is executed once the user joins the chat room.
	  
    def welcome_new_user(self, from_user):
        msg = self.name + " welcomes: " + from_user.name + '\n'       
        for user in self.users:
            user.socket.sendall(msg.encode())

	  #	To broadcast the message to all the users who are part of the same chat room. 
	  
    def broadcast_to_users(self, from_user, msg):
        msg = from_user.name.encode() + ":" + msg
        for user in self.users:
            user.socket.sendall(msg)

	    
    def multiple(self, from_user, msg):
        msg = from_user + " says: " + msg + '\n'
        for user in self.users:
            user.socket.sendall(msg)

	 # To remove user from the chatroom on leave command. 
			
    def remove_user(self, user):
        self.users.remove(user)
        leave_msg = user.name.encode() + " is not currenlty present in the room \n"
        self.broadcast_to_users(user, leave_msg)
	
	

class Functions:
    counter = 0
    def __init__(self):
        self.rooms = {}
		
		# To store the mapping between the room and user. 
		
        self.room_user_map = {}
		
		# To store record of each users presence in the room 
		# In short it stores the User to Room mapping (One user to multiple rooms)  
		
        self.user_room_map = {}
		
		#List of currenentl active users 
		
        self.user_list = {}
 
        # To welcome user upon connecting to server.
			  
    def welcome_new_user(self, new_user):
        new_user.socket.sendall('Welcome!\n Please type in your name:\n')

	# Function implements the list Room command.	 
	
    def list_active_rooms(self, user):

        if len(self.rooms) == 0:
            msg = 'No active Chatrooms available. Create using join\create command\n'
            user.socket.sendall(msg.encode())
        else:

            msg = 'Currently Active Chatrooms are: \n'
            for room in self.rooms:
                msg += room + ": " + str(len(self.rooms[room].users)) + " user(s)\n"
            user.socket.sendall(msg.encode())
			
     # Depending upon the command given by the user this funcation performes right operation. 
	 # The typical command used by the users such as listrooms, join, Send, helpdesk, quit, private chatting etc. 
	 
    def command_execution(self, user, msg):

        instructions = '...............Helpdesk:................................\n' \
                       + '.............listrooms                :  List active chatrooms............\n' \    # All the commands that are supported by 
                       + '.............join room                :  Join/create a room............\n' \       # this Application.
                       + '.............listmembers room         :  List all members in the room.....\n' \
                       + '.............send room sender msg     :  Broadcast meassage in a particular room...\n' \
                       + '.............leave room               :  To leave a room.............\n' \
                       + '.............helpdesk                 :  For Helpdesk...........\n' \
                       + '.............quit                     :  To quit..........\n' \
                       + '............ private receiver message :  To send private message to any user.......\n' \
                       + '...............................................................................\n'

        if "username:" in msg:
            name = msg.split()[1]
            user.name = name
            self.user_list[name] = user.socket
            print("New connection from:", user.name)
            user.socket.sendall(instructions)
           
		   
		 #  Implementaion for joining new room. 
         #	Using join command
		 
        elif "join" in msg:
            same_room = False
            if len(msg.split()) >= 2:
                room_name = msg.split()[1]
				
				# Check the room to user mapping and if it's true.
				# Then print that user is alreday in the room.
				
                if user.name in self.room_user_map:
                    if self.room_user_map[user.name] == room_name:
                        user.socket.sendall('You are already in room: ' + room_name.encode())         
                        same_room = True
						
						# else add the user to the room.

                if not same_room:
                    if not room_name in self.rooms:
                        new_room = Room(room_name)
                        self.rooms[room_name] = new_room
                    self.rooms[room_name].users.append(user)

                    self.rooms[room_name].welcome_new(user)
                    print 'User name is: ' + user.name
                    self.room_user_map[user.name] = room_name
                    print 'in join,mapped value: ' + str(self.room_user_map[user.name]) + '\n'
                    if room_name in self.user_room_map:
                        name = user.name
                        self.user_room_map[room_name].append(name)
                    else:
                        name = user.name
                        self.user_room_map[room_name] = list()
                        self.user_room_map[room_name].append(name)
            else:
                user.socket.sendall(instructions)

             
       # Implementaion for leaving the room.
	   # Using leave command.
	   
        elif "leave" in msg:
            room_name = msg.split()[1]
            if user.name in self.room_user_map:
			
			    # Try catch to ensure that user is not trying to leave the room which he has not joined. 
				# If they tries to do so then throw it as an exceptoin and handle it.
                try:

                    if room_name in self.user_room_map:
                        if user.name in self.user_room_map[room_name]:
                            self.rooms[room_name].remove_user(user)
                            self.user_room_map[room_name].remove(user.name)
                            print 'left successfully'
                            msg = 'Left successfully' + '\n'
                            user.socket.sendall(msg.encode())
                except:
                    msg += 'Sorry!You are not joined in the room' + '\n'
                    user.socket.sendall(msg.encode())
            else:
                print('You are not joined in any room')
				
				 
        
        elif "listmembers" in msg:
            if len(msg.split()) >= 2:
               room_name = msg.split()[1]
               self.list_active_members(user,room_name)

        elif "listrooms" in msg:
            self.list_active_rooms(user)

        elif "helpdesk" in msg:
            user.socket.sendall(instructions)

        elif "quit" in msg:
            user.socket.sendall(QUIT_STRING.encode())
            self.remove_user(user)

        elif "private" in msg:
            self.private_messaging (user,msg)

			# sending message into a specified room.
            # USing this code Long length messages can be handled 			
        elif "send" in msg:
            room_name = msg.split()[1]
            print room_name
            user.name = msg.split()[2]
            print 'Message generated from: ' + user.name
            if len(msg.split()) > 4:
                msg1=msg.split()[3]                                      
                msg2=msg.split()[4]
                message = msg1 + ' ' + msg2                
            elif len(msg.split()) > 5:
                msg1=msg.split()[3]
                msg2=msg.split()[4]
                msg3=msg.split()[5]        
                message = msg1 + ' ' + msg2+' '+msg3
            else:
                message = msg.split()[3]
                print 'msg' + message
            print 'Message is: ' + message
            if user.name in self.user_room_map[room_name]:
                list_users = self.user_room_map[room_name]
                print 'Users in ' + str(list_users)
                for users in list_users:
                    print ''.join(str(users)) + '\n'
                self.broadcast_multiple(room_name, user.name,message)
            else:
                msg += 'Not connected to this room! Please join first!\n'
                user.socket.sendall(msg.encode())


			# if user tries to send message even if htey have not joined one. 	
        else:
            if user.name in self.room_user_map_map:
                self.rooms[self.room_user_map[user.name]].broadcast_to_users(user, msg.encode())
            else:
			
                msg = 'You are currently not in any room! Please use Join Command to join/Create one! \n'
                user.socket.sendall(msg.encode())
				
				

    def broadcast_multiple(self, room_name, user, msg):
            self.rooms[room_name].multiple(user, msg.encode())


			
	# Funcation to Imeplement list members. 
	# listmembers command is used to invoke this funcation. 
	
    def list_active_members(self,user,room):
        room_name = room
        print 'Listmembers: ' + room_name
        msg = 'Members are: ' + ' \n'
        if room_name in self.rooms:
		
		    # if user tries to list the members of the room when room is empty it is handled has exception 
            try:
                members = self.user_room_map[room_name]
                print 'members in room blue: ' + str(members) + '\n'
                for i in members:
                    msg += (str(i)) + '\n'
                user.socket.sendall(msg)                                             
            except:
                msg += 'no members in room' + '\n'
                user.socket.sendall(msg.encode())
        else:
            msg = 'No such room exist'
            user.socket.sendall(msg.encode())
			
     # Funcation to implementing the Private messaging between two users.
	 # Input Sender name and message.
	 
    def private_messaging (self, sender, msg):
        receiver = msg.split()[1]
        if receiver in self.user_list:
            user = self.user_list[receiver]
            try:
                user.sendall('Private message from ' + sender.name + ': ' + msg.rsplit(receiver, 1)[1] + '\n')
            except:
                sender.socket.sendall('Sorry! Receiver is offline')
        else:
            msg += 'Sorry! No such user online' + '\n'
 
 
      # Remove the user from the chat room upon the leave command.  
	  
    def remove_user(self, user):
        if user.name in self.room_user_map:
            self.rooms[self.room_user_map[user.name]].remove_user(user)
            del self.room_user_map[user.name]
        print("User: " + user.name + " has left\n")




	# Class to encapuslate the user details. 	 
	
class User:
    def __init__(self, socket, name="new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name


    def fileno(self):
       return self.socket.fileno()
