import socket
import ssl

def calculate(num1, num2, operation):
    try:
        if operation == '+':
            return num1 + num2
        elif operation == '-':
            return num1 - num2
        elif operation == '*':
            return num1 * num2
        elif operation == '/':
            if num2 != 0:
                return num1 / num2
            else:
                raise ZeroDivisionError("Error: Division by zero")
        else:
            raise ValueError("Error: Invalid operation")
    except Exception as e:
        return str(e)

def main():
    HOST = 'LocalHost'
    PORT = 9990
    MAX_BUFFER_SIZE = 1024

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"Server listening on {HOST}:{PORT}...")

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")

    client_socket, client_address = server_socket.accept()
    secure_socket = context.wrap_socket(client_socket, server_side=True)

    try:
        print(f"Successfully connected to client at {client_address}")

        while True:
            buffer = secure_socket.recv(MAX_BUFFER_SIZE).decode('utf-8')
            if buffer.startswith("exit"):
                print("Server exiting...")
                break

            try:
                # Check if the buffer contains enough values
                expression_parts = buffer.split()
                if len(expression_parts) != 3:
                    raise ValueError("Error: Invalid expression")

                num1, operation, num2 = expression_parts
                num1 = float(num1)
                num2 = float(num2)
                result = calculate(num1, num2, operation)
                secure_socket.send(str(result).encode('utf-8'))

            except ValueError as ve:
                print(f"ValueError: {ve}")
                secure_socket.send(str(ve).encode('utf-8'))

    except ssl.SSLEOFError as e:
        print(f"SSLEOFError: {e}")

    finally:
        # Close the SSL socket and then close the regular socket
        secure_socket.close()
        server_socket.close()

if __name__ == "__main__":
    main()
