from socket import *
import os
import struct
'''
class sender(object):

    def __init__(self, s):
        self.socket = s
'''      
def send(s,filename):
    '''
    ADDR = ('127.0.0.1',8000)
    BUFSIZE = 1024
    #filename = 'ChatRoom/1.zip'
    '''
    BUFSIZE = 1024

    print filename
    if os.path.isfile(filename):
        FILEINFO_SIZE=struct.calcsize('128s32sI8s')
        '''
        s = socket(AF_INET,SOCK_STREAM)
        s.connect(ADDR)
        '''
        fhead=struct.pack('128s11I',filename,0,0,0,0,0,0,0,0,os.stat(filename).st_size,0,0)
        s.send(fhead)
        fp = open(filename,'rb')
        while 1:
            filedata = fp.read(BUFSIZE)
            if not filedata: break
            s.send(filedata)
        print "finshed"
        fp.close()
        '''
        s.close()
        '''
        print "closed"
    else:
        print "NoFile!! closed~"
