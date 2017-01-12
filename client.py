import socket
import sys
import argparse
import time
import threading




if __name__ == '__main__':

	HOST = '10.5.2.101' 	#
	Port = 5566

	#create socket
	try:
		#create an AF_INET, STREAM socket (TCP)
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		print('Socket created for '+ HOST + ':' + str(Port) )
	except socket.error as msg :
		print('Failed to create socket for '+ HOST + ':' + str(Port) + '. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1])
	

	#connect to server
	try:
		#Connet to remote server
		s.connect((HOST,Port))
		print('Socket connected to '+ HOST + ':' + str(Port) )
	except socket.error as msg :
		print('Failed to connect to '+ HOST + ':' + str(Port) + '. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1])
	



	

	
	ACTIVE = True

	while ACTIVE :

		command = raw_input("Please choose to login or signup : ")

		if command == 'login':
			# do login
			print('do login')
			s.send(command)
			reply = s.recv(4096)

			user = raw_input("Username : ")
			s.send(user)
			password = raw_input("Password : ")
			s.send(password)

			reply = s.recv(4096)
			print(reply)

		elif command == 'signup':
			# do register
			print('do signup')
			s.send(command)
			reply = s.recv(4096)

			user = raw_input("Username : ")
			s.send(user)
			password = raw_input("Password : ")
			s.send(password)

			reply = s.recv(4096)
			print(reply)
			







		'''
		s.send(command)
			
		reply = s.recv(4096)
		print(reply)
		'''
		

	#close socket
	s.close()
