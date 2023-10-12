from flask import Flask, request
import socket
import requests

app = Flask(__name__)
registered_server = {}

def register_with_authoritative_server(hostname, ip, as_ip, as_port):
    # Send a UDP registration request to the Authoritative Server (AS)
    registration_data = f"HTTP/1.1 PUT /register\r\n"
    registration_data += f"Host: {as_ip}:{as_port}\r\n"
    registration_data += f"Content-Length: {len(f'TYPE=A NAME={hostname} VALUE={ip} TTL=10')}\r\n"
    registration_data += f"Content-Type: application/json\r\n\r\n"
    registration_data += f"TYPE=A NAME={hostname} VALUE={ip} TTL=10"
    
    as_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    as_address = (as_ip, as_port)
    
    print(f"Sending registration data to AS server at {as_address}: {registration_data}")  # Debugging line
    
    as_socket.sendto(registration_data.encode(), as_address)
    as_socket.close()

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    hostname = data['hostname']
    ip = data['ip']
    as_ip = data['as_ip']
    as_port = int(data['as_port'])  # Convert port to an integer

    # Register the server with the Authoritative Server (AS)
    registered_server[hostname] = {
        'ip': ip,
        'as_ip': as_ip,
        'as_port': as_port
    }

    # Register with the AS
    register_with_authoritative_server(hostname, ip, as_ip, as_port)

    return "Server registered", 201

@app.route('/fibonacci', methods=['GET'])
def calculate_fibonacci():
    number = request.args.get('number')

    if not number.isdigit():
        return "Invalid input", 400

    number = int(number)
    if number < 0:
        return "Invalid input", 400

    if number == 0:
        return "0", 200
    elif number == 1:
        return "1", 200

    a, b = 0, 1
    for _ in range(2, number + 1):
        a, b = b, a + b

    return str(b), 200

if __name__ == '__main__':
    app.run(port=9090)
