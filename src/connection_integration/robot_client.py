import socket

def connect_to_robot():
    # Define the server's IP and port
    host = '10.197.116.213'  # Raspberry Pi's IP address
    port = 12345  # Same port number as server

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")

    return client_socket

def receive_message(client_socket):
    # Receive the server's response
    message = client_socket.recv(1024).decode('utf-8')
    print(f"Received: {message}")

    return message

def main():
    client_socket = connect_to_robot()

    while True:
        # Get message from user input
        message = input("Enter message to send (or type 'exit' to quit): ")

        # Send the message to the server
        client_socket.send(message.encode('utf-8'))

        if message.lower() == 'exit':
            break
        
    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    main()