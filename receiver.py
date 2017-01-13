from socket import *
import struct
HOST = '127.0.0.1'
PORT = 8000
BUFSIZE = 1024
FILEINFO_SIZE=struct.calcsize('128s32sI8s')
recvSock = socket(AF_INET,SOCK_STREAM)
recvSock.bind((HOST,PORT))
recvSock.listen(True)
print "waiting"
conn,addr = recvSock.accept()
print "connected ",addr
fhead = conn.recv(FILEINFO_SIZE)
filename,temp1,filesize,temp2=struct.unpack('128s32sI8s',fhead)
#print filename,temp1,filesize,temp2
print filename,len(filename),type(filename)
print filesize
filename = filename.strip('\00') #...
x = filename.split("/")
lenth = len(x)
filename = x[lenth-1]
fp = open(filename,'wb')
restsize = filesize
print "processing ",
while 1:
    if restsize > BUFSIZE:
        filedata = conn.recv(BUFSIZE)
    else:
        filedata = conn.recv(restsize)
    if not filedata: break
    fp.write(filedata)
    restsize = restsize-len(filedata)
    if restsize == 0:
     break
print "finished"
fp.close()
conn.close()
recvSock.close()
print "closed"
