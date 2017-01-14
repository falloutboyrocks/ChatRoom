import socket
import sys
import argparse
import time
import thread
import threading
import select
import Tkinter as tk
from time import sleep
import receiver
import sender
import os
import time

def quit():
	global aid
	win.after_cancel(aid)
	win.destroy()

def send(server):
	userinput = input_text.get()
	input_text.set('')
	server.setblocking(1)
	server.send('talk')
	server.send(userinput)
	
def polling(server):
	server.setblocking(0)
	try:
		reply = server.recv(4096)
		print(reply)
		log.set(reply)
	except:
		pass
	server.setblocking(1)
	global aid
	aid = win.after(500, polling, server)

if __name__ == '__main__':

	HOST = 'localhost' 	#
	Port = 5566
	#create socket
	try:
		#create an AF_INET, STREAM socket (TCP)
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		print('Socket created for '+ HOST + ':' + str(Port) )
	except socket.error as msg :
		print('Failed to create socket for '+ HOST + ':' + str(Port) + '. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1])
		sys.exit(0)

	#connect to server
	try:
		#Connet to remote server
		s.connect((HOST,Port))
		print('Socket connected to '+ HOST + ':' + str(Port) )
	except socket.error as msg :
		print('Failed to connect to '+ HOST + ':' + str(Port) + '. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1])
		sys.exit(0)	

	
	ACTIVE = True
	loggedIn = False
	target_user = ''

	while ACTIVE :
		
		if loggedIn == False:
			command = raw_input("Please choose to login/signup/quit: ")

			if command == 'login':
				# do login
				s.send(command)
				reply = s.recv(4096)

				user = raw_input("Username : ")
				s.send(user)
				password = raw_input("Password : ")
				s.send(password)
				reply = s.recv(4096)
				print(reply)
				if reply != 'No such user!' and reply != 'Wrong password!':
					loggedIn = True

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
			elif command == 'quit':
				break
			else:
				print('Invalid command!')	
				
		else:
			command = raw_input('Checkout/Signout/Upload/Download?: ')
			if command == 'Checkout':
				s.send('checkout')
				target_user = raw_input("Check out user:")
				s.send(target_user)
				reply = s.recv(4096)
				print(reply)
				if reply != 'No such user!':
					win = tk.Tk()
					input_text = tk.StringVar()
					log = tk.StringVar()
					label = tk.Label(win, textvariable=log).pack()		
					send_button = tk.Button(win, text='Send', command= lambda: send(s)).pack()
					quit_button = tk.Button(win, text='Quit', command=quit).pack()
					entry = tk.Entry(win, textvariable=input_text).pack()
					win.after(0, polling, s)
					win.mainloop()
				else:
					pass
			elif command == 'Signout':
				s.send('signout')
				loggedIn = False
			elif command == 'Upload':
				s.send('upload')
				target_user = raw_input("Upload user:")
				s.send(target_user)
				reply = s.recv(4096)
				if reply == 'success':
					files = raw_input("Please select file(s)(delimited by space):")
					files = files.split(' ')
					filenames = []
					for file in files:
						if os.path.isfile(file):
							filenames.append(file)
						else:
							print(file + ' is not a file')
					filenum = len(filenames)
					s.send(str(filenum))
					time.sleep(1)						
					for filename in filenames:
						sender.send(s,filename)
						print(filename + ' upload completd')
						time.sleep(1)
				elif reply == 'No such user!!!':
					print(reply)
			elif command == 'Download':
				s.send('download')
				reply = s.recv(4096)
				print(reply)
				if reply == 'No file':
					pass
				else:
					index = raw_input("Download file(by index):")
					s.send(index)
					reply = s.recv(4096)
					if reply == 'success':
						receiver.receive(s,'','',False)
						print('download completd')
					elif reply == 'No such index!!!':
						print(reply)
			else:
				print('Invalid command!')

	#close socket
	s.close()
