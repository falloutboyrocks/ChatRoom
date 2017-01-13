import socket
import sys
import time
import argparse
import thread
import threading
import csv
import loggedInAction as act 

path = 'database/'
loggedUser = {}
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



		command = client.recv(4096)

		if(loggedIn == False):
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
					loggedUser[user] = 1
					action = act.loggedInAction(client, user, readlock, writelock)
					action.render_all_user(loggedUser)

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
			if checkout == True and target_user + '_' + user in updateRecord:
				action.rcv()
				updateRecord.remove(target_user + '_' + user)

			if command == 'checkout':
				target_user = client.recv(4096)
				if target_user not in userList:
					client.send("Check out failed!")
				else:
					client.send("Sucess")
					action.checkout(target_user)
					checkout = True
			elif command == 'talk':
				sentence = client.recv(4096)
				action.talk(sentence)
				record = user + "_" + target_user
				if record not in updateRecord:
					updateRecord.append(record)
				
			
	client.close()



if __name__ == '__main__':

	HOST = 'localhost' 	#
	PORT = 5566
	readlock = threading.RLock()
	writelock = threading.Lock()

	#initialize user logged in list
	with open( path + 'Registration.log', 'r') as userfile:
		for info in csv.reader(userfile):		
			loggedUser[info[0]] = 0
				
					
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
