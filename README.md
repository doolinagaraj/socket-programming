# socket-programming
client server calculator using socket programming with ssl implementation
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM): Create a TCP socket.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1): Allow reuse of the address to avoid "Address already in use" errors.
server_socket.bind((HOST, PORT)): Bind the socket to the specified host and port.
server_socket.listen(1): Listen for incoming connections (only one at a time).
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH): Create an SSL context for server-side communication.
context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem"): Load the server certificate and private key.
client_socket, client_address = server_socket.accept(): Accept a client connection.
secure_socket = context.wrap_socket(client_socket, server_side=True): Wrap the client socket with SSL/TLS.
Inside a try block:
Print a message indicating a successful connection to the client.
Enter a loop to continuously receive and process messages from the client.
Check if the received message starts with "exit" to terminate the server.
Split the message into three parts (number1, operation, number2) and convert them to float.
Perform the calculation using the calculate function and send the result back to the client.
If an error occurs, catch the exception, print an error message, and send the error message back to the client.
