import socket
import time
import sys
import threading

def run_client(client_id):
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to server
        server_address = ('localhost', 8888)
        print(f'Client {client_id}: Connecting to localhost port 8888')
        sock.connect(server_address)
        
        try:
            # Send multiple messages with delays
            for i in range(3):
                message = f"Message {i} from Client {client_id}"
                message_bytes = message.encode('utf-8')
                
                # Construct protocol message
                total_length = 4 + 1 + 1 + len(message_bytes)
                full_message = (
                    total_length.to_bytes(4, byteorder='big') +  # Total length
                    (1).to_bytes(1, byteorder='big') +          # Message type
                    (1).to_bytes(1, byteorder='big') +          # Action type
                    message_bytes                               # Payload
                )
                
                print(f'Client {client_id}: Sending {message}')
                sock.sendall(full_message)
                
                # Wait for response
                data = sock.recv(1024)
                print(f'Client {client_id} received: {data.decode()}')
                
                # Wait a bit before sending next message
                time.sleep(1)
                
        finally:
            print(f'Client {client_id}: Closing socket')
            sock.close()
            
    except Exception as e:
        print(f'Client {client_id} error: {e}')

def start_multiple_clients(num_clients=3):
    threads = []
    for i in range(num_clients):
        thread = threading.Thread(target=run_client, args=(i,))
        threads.append(thread)
        thread.start()
        # Small delay between starting clients
        time.sleep(0.5)
    
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    num_clients = 3  # Default number of clients
    if len(sys.argv) > 1:
        num_clients = int(sys.argv[1])
    
    print(f"Starting {num_clients} clients...")
    start_multiple_clients(num_clients)