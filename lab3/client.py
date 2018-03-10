import zmq
import sys
import threading 


global user
global lastUser
lastUser = ""
def sendRequest(): # to send message requests to server
    context = zmq.Context()
    sock = context.socket(zmq.PUSH) #list of queued items need to be routed for the one asking for it
    sock.connect("tcp://127.0.0.1:5678")
    while True:
        try:
            msg = promptMessage()
        except KeyboardInterrupt:
            break
        if msg != '':
            sock.send_string("[{}]: ".format(user) + msg)

def promptMessage():
    msg = input("[%s] > " % user) 
    return msg 

def receiveMessage(): #subscriber receives message
    context = zmq.Context()
    sock = context.socket(zmq.SUB) #subscribe to server
    sock.setsockopt_string(zmq.SUBSCRIBE, '') #subscribe to all messages
    sock.connect("tcp://127.0.0.1:5677")

    output = sock.recv()
    printOutput(output.decode())
    threading.Thread(target=receiveMessage).start()


def printOutput(m):
    if m.find(user) == -1: #print all outputs other than the user's output again
        print('\n' + m + ("\n[%s] > " % user), end='')



if __name__ == "__main__":
    global user
    try:
        user = " ".join(sys.argv[1:]) #name, if two names or more
        print("User[%s] Connected to the chat server." % user)
        #Process(target=receiveMessage).start()
        threading.Thread(target=receiveMessage).start()
        sendRequest()
    except Exception as e:
        print(e)

""" 
SAMPLE OUTPUT: 
(my-venv) MacBook-Pro:lab3 Aditi$ python3 client.py Bob
User[Bob] Connected to the chat server.
[Bob] > What's up guys?
[Bob] > 
[Alice]: Not much, you?
[Bob] > 
[Smith]: You guys want food?
[Bob] > Yeah let's get something
[Bob] > 
[Alice]: I'm also hungry
[Bob] >  
"""

