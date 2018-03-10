import zmq
import time

def serve():
    context = zmq.Context()

    pull = context.socket(zmq.PULL) #pull messages from client
    pull.bind("tcp://127.0.0.1:5678")

    publish = context.socket(zmq.PUB) #publish messages to clients
    publish.bind("tcp://127.0.0.1:5677")

    poller = zmq.Poller()
    poller.register(pull, zmq.POLLIN)

    while True:
        events = dict(poller.poll()) #socket has a new event = new message
        if ((pull in events) and (events[pull] == zmq.POLLIN)): #pull from sockets. if message is received, publish
            message = pull.recv_string()
            publish.send_string(message)
            print(message)

if __name__ == "__main__":
    try:
        serve()
    except Exception as e:
        print("Exception: " + e)




