import socket
import sys
import argparse
import time
import thread
import threading
import select
import Tkinter as tk
from time import sleep


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
		log.set(reply)
	except:
		pass
	win.after(500, polling, server)

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
	

	#connect to server
	try:
		#Connet to remote server
		s.connect((HOST,Port))
		print('Socket connected to '+ HOST + ':' + str(Port) )
	except socket.error as msg :
		print('Failed to connect to '+ HOST + ':' + str(Port) + '. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1])
	

	
	ACTIVE = True
	loggedIn = False
	checkout = False
	target_user = ''

	while ACTIVE :
		
		if loggedIn == False:
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
				
		else:
			if checkout == False:
				s.send('checkout')
				target_user = raw_input("Check out users:\n")
				s.send(target_user)
				reply = s.recv(4096)
				if reply != "Check out failed!":
					checkout = True
					print(reply)
			else:
				# a thread to handle input
				global terminate
				win = tk.Tk()
				log = tk.StringVar()
				input_text = tk.StringVar()
				label = tk.Label(win, textvariable=log).pack()		
				send_button = tk.Button(win, text='Send', command= lambda: send(s)).pack()
				quit_button = tk.Button(win, text='Quit', command=quit).pack()
				entry = tk.Entry(win, textvariable=input_text).pack()
				win.after(0, polling, s)
				win.mainloop()
				checkout = False
						
								
	





		'''
		s.send(command)
			
		reply = s.recv(4096)
		print(reply)
		'''
		

	#close socket
	s.close()
