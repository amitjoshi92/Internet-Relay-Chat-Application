IRC is an open protocol that uses TCP and, optionally, TLS. An IRC server can connect to other IRC servers to expand the IRC network. Users access IRC networks by connecting a client to a server. The standard structure of a network of IRC servers is a tree. Messages are routed along only necessary branches of the tree but network state is sent to every server and there is generally a high degree of implicit trust between servers.

Server: The server is the central point to which clients may connect and talk to each other. The traditional IRC protocol supports multiple servers in a spanning tree configuration. However, for the purpose of this project we will limit the number of servers to one. This single server will act as the backbone of our IRC network, providing a unique point for clients to connect to and talk to one another.

Client: Client is anything that connects to our single server. Each client is identified by a unique username. In this version of our IRC protocol, there is no registered user database, no persistent clients. Users connect to the server by providing a username at the beginning of every session and the end of the session all of the user’s information is erased.

Chatrooms: The basic means of communicating to a group of users in IRC session is through chat rooms. Channels on a network can be displayed using the IRC command LIST, which lists all currently available channels that do not have the modes +s or +p set, on that particular network. Users can join a channel using the JOIN command, in most clients available as /join #channelname. Messages sent to the joined channels are then relayed to all other users.

IRC Working concept: (a) At first, client is asked for the IP address of the server to which he/she wishes to connect to. Depending on whether the server-side and client-side programs are running on same system or two different systems, we will give an IP address either as “localhost” or an IP of server such as “127.0.0.1”

(b) Client is able to send messages to other clients through the server and the server identifies each user by its unique player.name.

(c) Second, Client will be asked to give chatroom name which he/she wants to connect with. The client then gives the chat room name to start broadcasting messages in it.

(d) When the client joins the specified chat room, he/she has the ability to see other chatrooms available. Client can view all the available chat rooms using command “listrooms”.

(e) When the client has finished sending messages to other clients, he/she can leave the chat room by simply using command “leave <room_name>” or can type to end session with server. The server then closes the connection to that client.
