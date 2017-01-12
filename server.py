import socket
import sys
import time
import argparse
import thread


def clientThread(client,addr):
	while 1:
		data = client.recv(4096)

		'''
		if data:
			print('recv from ' + addr[0] + ':' + str(addr[1]) + ', command = ' + data)
			client.send(data)
		'''

		if data == 'login':
			

	client.close()



if __name__ == '__main__':

	HOST = '' 	#
	PORT = 5566

	#create socket
	try:
		#create an AF_INET, STREAM socket (TCP)
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		print('Socket created')
	except socket.error as msg :
		print('Failed to create socket. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1])
		sys.exit()


	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	#create server
	try:
		s.bind((HOST,PORT))
		print('Socket bind completed')
	except socket.error as msg :
		print('Bind Failed. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1])
		sys.exit()



	# listen to client
	s.listen(10) # 10 
	print('Socket now listening')

	while 1:

		try:
			(client,addr) = s.accept()
			print('Connecting with ' + addr[0] + ':' + str(addr[1]))
		except KeyboardInterrupt:
			sys.exit()

		thread.start_new_thread(clientThread,(client,addr))

		
	s.close()