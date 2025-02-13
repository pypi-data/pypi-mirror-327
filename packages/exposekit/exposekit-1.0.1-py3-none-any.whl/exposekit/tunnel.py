import socket, subprocess
import requests

class Tunnel:
    def __init__(self, port):
        self.running = True
        self.port = port
    
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except socket.gaierror:
            return "127.0.0.1"

    def get_public_ip(self):
        response = requests.get('https://api.ipify.org?format=json')
        public_ip = response.json()['ip']
        return public_ip

    def host(self, address='0.0.0.0'):
        if address is None:
            address = self.get_public_ip or self.get_local_ip()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind((address, self.port))
        except socket.error as e:
            print(f"Error binding to {address}:{self.port} - {e}")
            return
        
        # Start listening for incoming connections
        sock.listen(5)
        sock.settimeout(1.0)  # Set timeout to 1 second
        print(f'Tunnel started on {address}:{self.port}')
        print(f'Access your service at http://{address}:{self.port}')
        while self.running:
            try:
                client_socket, client_address = sock.accept()
                print(f'Connection established with {client_address}')
                # Here you would handle the client connection
                client_socket.close()
            except socket.timeout:
                self.running=False
                continue  # Continue loop and check for self.running
            except KeyboardInterrupt:
                print("Exiting loop due to keyboard interrupt.")
                self.running = False
            except Exception as e:
                print(f"Error: {e}")
                self.running = False

class SSHTunnel:
    def __init__(self, local_port):
        self.local_port = local_port

    def run(self):
        command = f"ssh -R 80:localhost:{self.local_port} nokey@localhost.run"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if process.returncode == 0:
            print(f"You can access your service via the public URL provided by localhost.run.")
        else:
            print(f"Failed to create localhost tunnel. Error: {err.decode()}")
            