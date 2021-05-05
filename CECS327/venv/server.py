import socket as skt

ME = '25.112.148.146'
NOT_ME = '25.5.20.122'
PORT = 65432


with skt.socket(skt.AF_INET, skt.SOCK_STREAM) as s:
    s.bind((ME, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

print('Received', repr(data))

with skt.socket(skt.AF_INET, skt.SOCK_STREAM) as s:
    s.connect((NOT_ME, PORT))
    s.sendall(b'Hello, Ryan')
    data = s.recv(1024)

print('Received', repr(data))
