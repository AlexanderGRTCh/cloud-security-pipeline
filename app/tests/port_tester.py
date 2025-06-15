import socket

ip = "44.248.236.26"
ports = [22, 5000, 8080, 80, 443, 3306]  # Add/remove as needed

for port in ports:
    s = socket.socket()
    s.settimeout(1)
    try:
        s.connect((ip, port))
        print(f"Port {port} is OPEN")
    except Exception:
        print(f"Port {port} is CLOSED")
    s.close()
