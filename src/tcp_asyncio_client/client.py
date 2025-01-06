import socket

class PersistentClient:

    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port


    def start_client(self):
        print("Starting Client")

        host = socket.gethostname()

        print("Host: {}".format(host))

        port = 8888

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        s.connect((host, port))

        self.send_message(s, 1, 1, "test")

        s.close()
        
        print("End of Client Main")



    def encode_message(self, message_type, action_type, payload):

        print("Message Type:{}, Action Type: {}, Payload: {}".format(message_type, action_type, payload))

        # Convert payload to bytes
        payload_bytes = payload.encode('utf-8')
        
        # Calculate total length (4-byte length + 1-byte type + 1-byte type + payload)
        total_length = 4 + 1 + 1 + len(payload_bytes)
        
        # Construct message
        message = (
            total_length.to_bytes(4, byteorder='big') +  # Total length
            message_type.to_bytes(1, byteorder='big') +  # Message type
            action_type.to_bytes(1, byteorder='big') + # Action Type
            payload_bytes  # Payload
        )

        return message

    def decode_message(self, data):
        
        print("Data: {}".format(data))
        
        # Extract total length
        total_length = int.from_bytes(data[:4], byteorder='big')
        
        # Extract message type
        message_type = int.from_bytes(data[4:5], byteorder='big')
        
        # Extract action type
        action_type = int.from_bytes(data[5:6], byteorder='big')

        # Extract payload
        payload = data[6:].decode('utf-8')
        
        return {
            'length': total_length,
            'message_type': message_type,
            'action_type': action_type,
            'payload': payload
        }

        
    def send_message(self, socket, message, action, payload):

        encoded_message = self.encode_message(message, action, payload)

        socket.sendall(encoded_message)

        data = socket.recv(1024)

        decoded_message = self.decode_message(data)

        print("Response from Server: {}".format(decoded_message))


