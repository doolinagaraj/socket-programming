import socket
import ssl

def main():
    HOST = 'LocalHost'
    PORT = 9990

    # Create a regular socket connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Disable certificate verification
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # Wrap the socket with SSL
    ssl_socket = context.wrap_socket(client_socket, server_hostname=HOST)

    # Connect to the server
    ssl_socket.connect((HOST, PORT))

    print("Welcome to the Calculator Server")
    print("Type 'exit' to quit")

    while True:
        expression = input("Enter your expression: ")
        if expression.lower() == 'exit':
            break

        # Send the expression without any additional characters
        ssl_socket.send(expression.encode())

        # Receive and print the result
        result = ssl_socket.recv(1024).decode()
        print("Result:", result)

    # Close the SSL socket
    ssl_socket.close()

if __name__ == "__main__":
    main()