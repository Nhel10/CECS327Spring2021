import socket
import os
import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

sending = False
receiving = False


class Watcher:
    DIRECTORY_TO_WATCH = "C:/Users/Neru/PycharmProjects/CECS327/files"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        while True:
            time.sleep(5)
        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        print(event)
        global sending
        global receiving
        print("Sending: ", sending)
        print("Receiving: ", receiving)
        if event.is_directory:
            return None
        elif sending is False and receiving is False:
            file = event.src_path.split('\\')[1].split('~')[0]
            if event.event_type == 'moved':
                dest_file = event.dest_path.split('\\')[1].split('~')[0]
                print(file)
                print(dest_file)
                client(file, True)
                client(dest_file, False)
            elif event.event_type == 'modified' or event.event_type == 'created':
                client(file, False)
            elif event.event_type == 'deleted':
                client(file, True)


def client(filename, deleting):
    global sending
    sending = True
    host = '25.5.20.122'
    port = 5000

    s = socket.socket()
    s.connect((host, port))

    s.send(filename.encode())
    s.recv(1024).decode()
    s.send(str(deleting).encode())
    if deleting:
        print("Sent delete order for ", filename)
        time.sleep(1)
        sending = False
        return
    s.recv(1024)
    s.send(str(os.path.getsize(filename)).encode())
    s.recv(1024).decode()
    with open(filename, 'rb') as f:
        packet = f.read(1024)
        s.send(packet)
        while packet.decode() != "":
            packet = f.read(1024)
            s.send(packet)
    print("Sent ", filename)
    s.close()
    time.sleep(1)
    sending = False


def RetrFile(name, sock):
    global receiving
    receiving = True
    filename = sock.recv(1024).decode()
    sock.send(b'FILE')
    deleting = sock.recv(1024).decode()
    if deleting == "True":
        print("Deleting ", filename)
        os.remove(filename)
        time.sleep(1)
        receiving = False
        return
    sock.send(b'DELETE')
    file_size = int(sock.recv(1024).decode())
    sock.send(b'DATA')
    f = open(filename, 'wb')
    data = sock.recv(1024)
    totalRecv = len(data)
    f.write(data)
    while totalRecv < file_size:
        data = sock.recv(1024)
        totalRecv += len(data)
        f.write(data)
    print("Received ", filename)
    sock.send(b'DONE')
    f.close()
    sock.close()
    time.sleep(1)
    receiving = False


def server():
        host = '25.112.148.146'
        port = 5000

        s = socket.socket()
        s.bind((host, port))
        s.listen(5)

        # Define main directory where all files contain
        print (os.listdir())
        print ("Server Started.")
        while True:
            c, addr = s.accept()
            print ("client connected ip:<" + str(addr) + ">")
            t = threading.Thread(target=RetrFile, args=("RetrFile", c))
            t.start()
        s.close()


os.chdir(r"C:/Users/Neru/PycharmProjects/CECS327/files")
server = threading.Thread(target=server, args=())
server.start()
w = Watcher()
w.run()