import argparse
import socket
import random
import threading
from time import sleep
import bots

# Create a parser object to process command line arguments
parse = argparse.ArgumentParser(description='Simple chatbot program - Client')

# Add a definition of the arguments to be received
parse.add_argument('ip', help='IP address: string')
parse.add_argument('port', help='Port number: integer', type=int)
parse.add_argument('bot', help='Bot name: string')

# Parse the arguments
args = parse.parse_args()
IP = args.ip
PORT = args.port
NAME = args.bot

# # TCP socket connection
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((IP, int(PORT)))


# Verb list for random choice
verbs = ['eat', 'complain', 'run', 'fight', 'walk', 'work', 'sing', 'howl', 'fly', 'sew',
         'box', 'bow', 'draw', 'steal', 'jump', 'cry', 'study', 'hunt', 'climb', 'swim',
         'crawl', 'talk', 'punch', 'slap', 'party', 'cook', 'drink', 'wisper', 'train']


# Function for the host client to send suggestions and the shutdown keyword to the server
def suggest():
    # Variable to count down the number of suggestions (The host can suggest 3 times)
    numSuggestion = 3
    # Variable to count number of chat rounds, starting from 1 as an initial round
    numRound = 1

    while numSuggestion > 0:
        sleep(4)
        showRound = f"\n<<Round {numRound}>>" + '}'
        suggestMessage = "Host: Hey, I'd like to " + random.choice(verbs) + " with you guys!" + '}'

        clientSocket.send(showRound.encode())
        clientSocket.send(suggestMessage.encode())

        numSuggestion -= 1
        numRound += 1

    # Send shutdown keyword to the server to close the connection after 3 suggestions
    sleep(5)
    clientSocket.send('SHUTDOWN}'.encode())


# Function for host to handle received messages
def hostHandle(messageBuffer):
    # Message buffer is split into individual messages using the splitting character
    messageList = messageBuffer.split('}')

    # Check the messages one by one
    for message in messageList:
        # If there is any messages...
        if message:
            # If it's a keyword 'NAME', send the own name to the server
            if message == 'NAME':
                clientSocket.send(NAME.encode())
            # If it's a keyword 'SHUTDOWN', close the connection
            elif message == 'SHUTDOWN':
                sleep(1)
                clientSocket.close()
                exit(0)
            # If it's not a keyword then print the message
            else:
                print(message)

            # If the last word of the split message is 'start!'...
            # Start suggesting bacause it means the server has confirmed all the clients' connections
            if message.split()[-1] == 'start!':
                suggestThread = threading.Thread(target=suggest)
                suggestThread.start()


# Function for bots to handle received messages
def botHandle(messageBuffer):
    # Message buffer is split into individual messages using the splitting character
    messageList = messageBuffer.split('}')

    # Check the messages one by one
    for message in messageList:
        # If there is any message...
        if message:
            # If it's a keyword 'NAME', send the own name to the server
            if message == 'NAME':
                clientSocket.send(NAME.encode())
            # If it's a keyword 'SHUTDOWN', close the connection
            elif message == 'SHUTDOWN':
                sleep(1)
                clientSocket.close()
                exit(0)
            # If it's not a keyword then print the message
            else:
                print(message)

            # If the message is from the host, then create suitable reply from bots
            if message.split()[0] == 'Host:':
                suggestVerb = ''
                words = message.split()
                for word in words:
                    if word in verbs:
                        index = verbs.index(word)
                        suggestVerb = verbs[index]
                response = bots.callBots(NAME.lower(), suggestVerb)
                clientSocket.send(response.encode())


# Main function to receive messages
def receive():
    while True:
        # Try to receive message from the socket
        try:
            messageBuffer = clientSocket.recv(1024)
            message = messageBuffer.decode()

            # If there is any messages in the buffer, call the other functions which can handle the message
            if message:
                # If the name of a connected client is 'Host'
                if NAME.lower() == 'host':
                    hostHandle(message)
                # If the name of a connected client is something else other than 'Host'
                else:
                    botHandle(message)

        # Close the connection if socket throws exception
        except:
            print("\nLost connection to the server.")
            clientSocket.close()
            exit(0)


# Run the main function
receive()
