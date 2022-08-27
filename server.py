import argparse
import socket
import threading
from time import sleep

# Create a parser object to process a command line argument
parse = argparse.ArgumentParser(description='Simple chatbot program - Server')

# Add a definition of the argument to be received
parse.add_argument('port', help='Port number: integer', type=int)

# Parse the argument
args = parse.parse_args()
PORT = args.port

# TCP socket connection
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('localhost', int(PORT)))
serverSocket.listen()

# Empty lists
clientList = []  # Store bots as a socket object
nameList = []  # Store connected clients' names as a string

# When this variable becomes True, shutting down the program will start
shutdownFlag = False


# Send messages to all connected clients
def broadcast(message):
    for client in clientList:
        client.send(message.encode())


# Handle messages sent from clients
def handle(client):
    global shutdownFlag

    while True:
        try:
            # Receive messages from clients
            messageBuffer = client.recv(1024).decode()
            # Message buffer is split into individual messages using the splitting character
            messageList = messageBuffer.split('}')

            # Check the messages one by one
            for message in messageList:
                # If there is any message...
                if message:
                    # If the message is a keyword 'SHUTDOWN', turn the shutdownFlag into True
                    if message == 'SHUTDOWN':
                        shutdownFlag = True
                    # If it's just a normal message, print and broadcast it
                    else:
                        print(message)
                        broadcast(message + '}')

        except:
            if shutdownFlag:
                break
            else:
                # Remove a client from the lists and close connection with it
                index = clientList.index(client)
                clientList.remove(client)
                client.close()
                name = nameList[index]
                broadcast(f"{name} has left the chat!")
                nameList.remove(name)
                break


# Main function to accept client connections
def accept():
    # When this variable becomes False, it means the server has confirmed 5 client-connections, and the chat will start
    startFlag = True

    print("Waiting for exactly 5 connections...\n")

    while True:
        # While it has less than 5 clients connected and the variable startFlag is True
        while len(clientList) < 5 and startFlag:
            # Accepts client connections and Store the client in the list
            client, address = serverSocket.accept()
            clientList.append(client)

            # Request the client's name using the keyword 'NAME' and store the name in the list
            client.send('NAME'.encode())
            name = client.recv(1024).decode()
            nameList.append(name)

            # Send welcome message to a new connected client
            client.send("========== Welcome to Chat Client! ==========}".encode())
            client.send("You are now connected to the server!}".encode())

            # Print and broadcast the info of a new connected client
            print(f"New connection with {address} has been established.")
            print(f"Name is {name}.\n")
            broadcast(f"{name} joined the chat!\n" + '}')

            # Start handling thread
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

        # When 5 clients joined and the variable startFlag is True
        if len(clientList) == 5 and startFlag:
            print("5 connections confirmed, waiting for the host's suggestion...")
            broadcast("We have 5 connections now, let's start!" + '}')
            startFlag = False  # Turn this into False since the server is no longer accepts a new connection

        # When shutdown keyword is sent after suggesting finished
        if shutdownFlag:
            print("\nSuggestion finished. Terminating the program...")
            broadcast("\nThe chat is finished. Let's chat again someday, bye!" + '}')
            sleep(1)

            # Forward the received keyword 'SHUTDOWN' to all the clients in the clientList
            for client in clientList:
                client.send('SHUTDOWN}'.encode())
                try:
                    client.shutdown(socket.SHUT_RDWR)
                    client.close()
                except:
                    print("ERROR: Closing connection failed.")
                    pass

            # After sleeping for 5 seconds, the server will close the connection
            sleep(5)
            serverSocket.close()
            break


# Welcome message to the server
print("========== Welcome to Chat Server! ==========")

# Run the main function
accept()
