import os.path
import socket

class loggedInAction:
	# target_user: the person user's talking to
	logfile
	target_user
	user

	def _init_(socket, user):
		self.socket = socket
		self.user = user
	
	def checkout(target_user):
		self.target_user = target_user
		if(user > target_user):
			filename = user + "_" + target_user
		else
			filename = target_user + "_" + target_user
		
		if(os.path.isfile(filename)):	# if the log file exist, return all logs to user
			logfile = open(filename)
			with logfile as f:
				self.socket.sendall(f.readlines())
		else:				# if the log file doesn't exist, create the logfile
			logfile = open(filename, 'w') 
		self.socket.sendall("END\n")


	def talk(sentence):
		logfile.write(user + ": " + sentence + "\n")
			
	def rcv():
		with logfile as f:
			self.socket.sendall(f.readlines())
		self.socket.sendall("END\n")
	
	def render_all_user(user_list):
		for i in iter(user_list):
			if(user_list[i] == 1):
				self.socket.sendall(i + "	Online\n")
			else:
				self.socket.sendall(i + "	Offline\n")
		self.socket.sendall("END\n")
