import socket
import sys
import time
import argparse
import thread
import csv

path = 'database/'

def clientThread(client,addr):
	while 1:

		
		userInfo = []
		userList = []
		
		with open(path + 'Registration.log','r') as file:
			for info in csv.reader(file):
				userInfo.append(info)
				userList.append(info[0])

		print(userInfo)
		print(userList)
		
		

		


		command = client.recv(4096)

		if command == 'login':
			client.send('LOGIN_START')

			user = client.recv(4096)
			password = client.recv(4096)

			if user not in userList:
				client.send('==== No such user ====')
			elif [user,password] not in userInfo:
				client.send('==== Wrong password ====')
			else:
				client.send('LOGIN_OK')



		elif command == 'signup':
			client.send('SIGNUP_START')

			user = client.recv(4096)
			password = client.recv(4096)

			if user in userList:
				client.send('==== Username has been used ====')
			else:
				newInfo = [[user,password]]
				print(newInfo)
				with open( path + 'Registration.log','a') as userFile:
					csv.writer(userFile).writerows(newInfo)
				client.send('SIGNUP_OK')


		#client.send(data)






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