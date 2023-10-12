import socket
import json

as_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

as_ip = "10.18.135.90"
as_port = 53533

as_socket.bind((as_ip, as_port))

dns_database = {}

while True:
    data, addr = as_socket.recvfrom(1024)
    query = data.decode("utf-8")
    
    print(f"Received data from {addr}: {query}")  # Debugging line
    
    lines = query.strip().split('\n')
    
    if len(lines) >= 3:
        _, dns_type, dns_name, dns_value, dns_ttl = [line.strip() for line in lines[:4]]
        
        if dns_type == "TYPE=A" and dns_name and dns_value and dns_ttl:
            dns_database[dns_name] = (dns_value, int(dns_ttl))
            response = "HTTP/1.1 201 Created\r\n\r\n"
        else:
            response = "HTTP/1.1 400 Bad Request\r\n\r\n"
    else:
        query_type, query_name = [line.strip() for line in lines]
        if query_type == "TYPE=A" and query_name:
            if query_name in dns_database:
                ip, ttl = dns_database[query_name]
                response = f"TYPE=A\nNAME={query_name}\nVALUE={ip} TTL={ttl}\n"
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
        else:
            response = "HTTP/1.1 400 Bad Request\r\n\r\n"
    
    as_socket.sendto(response.encode(), addr)
    print(f"Sent response to {addr}: {response}")  # Debugging line

