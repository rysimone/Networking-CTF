import socket
import message_pb2
import struct
import sys

# initialize variables that will be used
# destination address and port
ADDRESS = 'cs177.seclab.cs.ucsb.edu'
PORT = 37221
# dictionary to store values
rec_vals = {}
# variables used to determine length of packets
m_len = 0
length = 0
unparsed_str_len = ""
flg = 0
flg_string = ""
length_buffer = b''
message_buffer = b''

# Socket Creation
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket Created")
except socket.error as err:
    print("Socket creation failed with error")

# Connect to server
s.connect((ADDRESS,PORT))

# Iterate through rounds to convince the server I am a client
while(flg != 1):

    # Prompt the user for a Task
    print("Requesting Task")
    start_msg = message_pb2.Msg()
    start_msg.type = 0
    start_data = start_msg.SerializeToString()

    # calculate length of message and send to the server
    length = len(start_data)
    m_len = struct.pack('>H', length)
    s.sendall(m_len)
    s.sendall(start_data)
    print("Sent Task Request")

    # Receive the message length in a buffer to 
    # ensure entire message is received
    length_buffer = b''
    while(len(length_buffer) < 2):
        length_buffer += s.recv(1)

    # Unpack the buffer from Big Endian bytes
    m_len = struct.unpack('>H', length_buffer)[0]

    # Receive the message in a buffer to 
    # ensure entire message is received
    message_buffer = b''
    while(len(message_buffer) < m_len):
        message_buffer += s.recv(1)
    

    # Unpack data
    new_data = message_pb2.Msg()
    new_data.ParseFromString(message_buffer)

    # Determine what type of message response to send 
    # back to the server and prepare the Message 
    # per specifications
    if new_data.type == 1:
        # Add <Key, Value> to dictionary and alert server 
        parsedMsg1 = new_data.SerializeToString()
        msg1 = message_pb2.Msg1()
        msg1.ParseFromString(parsedMsg1)
        rec_vals[msg1.key] = msg1.value
        messageSend = message_pb2.Msg2()
        messageSend.type = 2
        messageSendString = messageSend.SerializeToString

    elif new_data.type == 3:
        # Return the value of a stored key if available
        parsedMsg3 = new_data.SerializeToString()
        msg3 = message_pb2.Msg3()
        msg3.ParseFromString(parsedMsg3)
        if not(msg3.key in rec_vals.keys()):
            messageSend = message_pb2.Msg5()
            messageSend.type = 5
        else:
            messageSend = message_pb2.Msg4()
            messageSend.type = 4
            messageSend.value = rec_vals[msg3.key]

    elif new_data.type == 6:
        # Return the number of unique stored <Key, Value>
        parsedMsg6 = new_data.SerializeToString()
        msg6 = message_pb2.Msg6()
        msg6.ParseFromString(parsedMsg6)
        messageSend = message_pb2.Msg7()
        messageSend.type = 7
        messageSend.count = len(rec_vals)

    elif new_data.type == 8:
        # An error has occured or an incorrect response
        # has been submitted
        parsedMsg8 = new_data.SerializeToString()
        msg8 = message_pb2.Msg8()
        msg8.ParseFromString(parsedMsg8)
        print(new_data.error)
        break

    elif new_data.type == 9:
        # Successfully convinced the server and retrieve the flag
        parsedMsg9 = new_data.SerializeToString()
        msg9 = message_pb2.Msg9()
        msg9.ParseFromString(parsedMsg9)
        print(f"FLAG FOUND. I REPEAT FLAG FOUND!!! = {msg9.flag}")
        flg = 1
        flg_string = msg9.flag
        break

    # Return Response message
    message_string = messageSend.SerializeToString()
    m_len = len(message_string)
    m_len = struct.pack('>H', m_len)
    s.sendall(m_len)
    s.sendall(message_string)

print(f"Flag Has been Captured!!   {flg_string}")
s.close()
