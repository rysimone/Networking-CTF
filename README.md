## Networking-CTF
A Capture the flag game designed between a client and server. 

# Description
The goal of the program is to create a client that can connect to a server and perform tasks to receive a flag. The tasks go in rounds and are as follows: 
Each round consists of three messages:

1.**Task Request Message**: The first message is from the client to the server, asking for a task.  

2.**Task Message**: The second message is from the server to the client. It specifies a specific task that the client must carry out.  

3.**Task Response Message**: The third message is from the client to the server. It is sent once the client has performed the given task, and it contains the task's result or status.  

# Message Format
The message format is made with protobuf to easily specify different message types

# Responses
The responses are determined based on the type value in the message. 

0 (C->S): Request a task. 

1 (S->C): Send <Key, Value> to be stored. 

2 (C->S: Alert server <Key, Vaue> was stored. 

3 (S->C): Return the value of the given key  

4 (C->): Return requested value from given key. 

5 (C->S): Alert server no such key exists  

6 (S->C): Request number of stored <Key, Value>. 

7 (C->S): Return number of stored <Key, Value>. 

8 (S->C): Return an error for either a wrong answer or an error. 

9 (S->C): Server sends the client the flag
