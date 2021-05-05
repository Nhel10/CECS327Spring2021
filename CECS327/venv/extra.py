if userResponse[:2] == 'OK':
    print("sd3")
    with open(filename, 'rb') as f:
        print("sdfSD4")
        bytesToSend = f.read(1024)
        sock.send(bytesToSend)
        while bytesToSend.decode() != "":
            print("sdf5")
            bytesToSend = f.read(1024)
            sock.send(bytesToSend)
else:
    sock.send(b"ERR")
print("Error")