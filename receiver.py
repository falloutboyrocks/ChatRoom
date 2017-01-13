from socket import *
import struct
import csv
'''
class receiver(object):

	def __init__(self, s):
		self.socket = s
'''	
def receive(s,user,target_user,flag):
	
	'''
	HOST = '127.0.0.1'
	PORT = 8000
	BUFSIZE = 1024
	FILEINFO_SIZE=struct.calcsize('128s32sI8s')
	recvSock = socket(AF_INET,SOCK_STREAM)
	recvSock.bind((HOST,PORT))
	recvSock.listen(True)
	print "waiting"
	s,addr = recvSock.accept()
	print "sected ",addr
	'''
	BUFSIZE = 1024
	FILEINFO_SIZE=struct.calcsize('128s32sI8s')
	fhead = s.recv(FILEINFO_SIZE)
	filename,temp1,filesize,temp2=struct.unpack('128s32sI8s',fhead)
	#print filename,temp1,filesize,temp2
	print filename,len(filename),type(filename)
	print filesize
	filename = filename.strip('\00') #...
	x = filename.split("/")
	lenth = len(x)
	filename = x[lenth-1]

	if flag == True:
		path = 'database/' + target_user + '/'
		newInfo = [[user,filename]]
		print(newInfo)
		with open( path + 'file.log','a') as fileLog:
			csv.writer(fileLog).writerows(newInfo)
	else:
		path = ''

	fp = open(path+filename,'wb')
	restsize = filesize
	print "processing ",
	while 1:
	    if restsize > BUFSIZE:
	        filedata = s.recv(BUFSIZE)
	    else:
	        filedata = s.recv(restsize)
	    if not filedata: break
	    fp.write(filedata)
	    restsize = restsize-len(filedata)
	    if restsize == 0:
	     break
	print "finished"
	fp.close()
	'''
	s.close()
	recvSock.close()
	'''
	print "closed"
