import socket
import sys
import time
import argparse
import thread
import threading
import csv
import loggedInAction as act 

path = 'database/'
updateRecord = []			# contains update records like "Alice_Bob" (Alice write to Bob)

def clientThread(client,addr):
	
	loggedIn = False
	checkout = False
	
	while 1:

		
		userInfo = []
		userList = []
		
		with open(path + 'Registration.log','r') as file:
			for info in csv.reader(file):
				userInfo.append(info)
				userList.append(info[0])


		if(loggedIn == False):
			command = client.recv(4096)
			if command == 'login':
				client.send('LOGIN_START')

				user = client.recv(4096)
				password = client.recv(4096)

				if user not in userList:
					client.send('No such user!')
				elif [user,password] not in userInfo:
					client.send('Wrong password!')
				else:
					loggedIn = True
					action = act.loggedInAction(client, user, readlock, writelock)
					action.render_all_user(userList)

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
		else:	# logged in operation
			client.setblocking(0)
			while(loggedIn == True):
				try:
					command = client.recv(4096)
				except:
					pass
				
				if checkout == True and target_user + '_' + user in updateRecord:
					action.rcv()
					updateRecord.remove(target_user + '_' + user)

				if command == 'checkout':
					client.setblocking(1)
					target_user = client.recv(4096)
					client.setblocking(0)
					if target_user not in userList:
						client.send("Check out failed!")
					else:
						client.send("Sucess")
						action.checkout(target_user)
						if target_user + '_' + user in updateRecord:
							updateRecord.remove(target_user + '_' + user)
						checkout = True
						command = ''
				elif command == 'talk':
					client.setblocking(1)
					sentence = client.recv(4096)
					action.talk(sentence)
					client.setblocking(0)
					record = user + "_" + target_user
					if record not in updateRecord:
						updateRecord.append(record)
					command = ''
				elif command == 'signout':
					break	
			
	client.close()



if __name__ == '__main__':

	HOST = 'localhost' 	#
	PORT = 5566
	readlock = threading.RLock()
	writelock = threading.Lock()
				
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
