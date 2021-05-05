import socket

def Main():
        host = '127.0.0.1'
        port = 5000

        s = socket.socket()
        s.connect((host,port))

        fileName = raw_input("Filename? -> ")
        if filename != 'q':
            s.send(filename)
            data = s.recv(1024)
            if data[:6] == 'EXISTS':
                fileSize = long(data[6:])
                message = raw_input("File Exists, "+str(fileSize) + "Bytes, download? (Y/N)? ->")
                if message == 'Y':
                    s.send('OK')
                    f = open('new_'+filename, 'wb')
                    data = s.recv(1024)
                    totalRecv = len(data)
                    f.write(data)
                    while totalRecv < fileSize:
                        data = s.recv(1024)
                        totalRecv += len(data)
                        f.write(data)
                        print"{0:.2f}".format((totalRecv/float(fileSize))*100) + "% Done"
                        print "Download Complete!"
            else:
                    print b"File does not Exist!"
            s.close()

if __name__ == '__main__':
    Main()