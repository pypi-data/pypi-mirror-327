import socket
import threading
import select

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.gaierror:
        return "127.0.0.1"

def handle_client(client_socket, backend_host, backend_port):
    try:
        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_socket.connect((backend_host, backend_port))

        while True:
            # Use select to monitor both client and backend sockets for data
            rlist, _, _ = select.select([client_socket, backend_socket], [], [])

            if client_socket in rlist:
                request = client_socket.recv(4096)
                if not request:
                    break  # Client disconnected
                backend_socket.sendall(request)

            if backend_socket in rlist:
                response = backend_socket.recv(4096)
                if not response:
                    break  # Backend disconnected
                client_socket.sendall(response)

    except Exception as e:
        print(f"Error in client handler: {e}")
        try:
            client_socket.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\nError connecting to backend")
        except Exception:
            pass # Client might be already disconnected

    finally:
        try:
            backend_socket.close()
        except Exception:
            pass # Backend might be already closed
        try:
            client_socket.close()
        except Exception:
            pass # Client might be already closed
        print("Client disconnected")


def setup(bind_interface='0.0.0.0', proxy_port=8080, backend_host='127.0.0.1', backend_port=5000):
    try:
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.bind((bind_interface, proxy_port))
        proxy_socket.listen(5)  # Increase backlog for more connections
        print(f"Your IP: {get_local_ip()}")
        print(f"Proxy server listening on port {proxy_port}")

        while True:
            client_socket, address = proxy_socket.accept()
            print(f"Connection from {address}")

            # Use threading to handle each client connection concurrently
            client_thread = threading.Thread(target=handle_client, args=(client_socket, backend_host, backend_port))
            client_thread.daemon = True # Allow main thread to exit even if clients are connected
            client_thread.start()

    except Exception as e:
        print(f"Error in setup: {e}")
    finally:
        if 'proxy_socket' in locals() and proxy_socket:
            proxy_socket.close()
            print("Proxy server closed")