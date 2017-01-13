import os.path
import socket
import StringIO

class loggedInAction(object):
	# target_user: the person user's talking to

	def __init__(self, socket, user, rlock, wlock):
		self.socket = socket
		self.user = user
		self.readlock = rlock
		self.writelock = rlock
	
	def checkout(self, target_user):
		self.target_user = target_user
		if(self.user > self.target_user):
			self.filename = self.user + "_" + self.target_user
		else:
			self.filename = self.target_user + "_" + self.user
		
		if(os.path.isfile(self.filename)):	# if the log file exist, return all logs to user
			output = StringIO.StringIO()
			self.readlock.acquire()
			logfile = open(self.filename)
			with logfile as f:
				output.write(f.read())
			self.readlock.release()
			self.socket.send(output.getvalue())
		else:				# if the log file doesn't exist, create the logfile
			self.writelock.acquire()
			logfile = open(self.filename, 'w') 
			self.writelock.release()
			self.socket.send('Empty')

	def talk(self, sentence):
		self.writelock.acquire()
		logfile = open(self.filename, 'a')
		logfile.write(self.user + ": " + sentence + "\n")
		logfile.close()
		self.writelock.release()
		self.rcv()		
			
	def rcv(self):
		output = StringIO.StringIO()
		self.readlock.acquire()
		logfile = open(self.filename, 'r')
		with logfile as f:
			output.write(f.read())
		self.readlock.release()
		self.socket.send(output.getvalue())
		print('send back')
	
	def render_all_user(self, user_list):
		output = StringIO.StringIO()
		output.write("========UserList=========\n")
		for i in iter(user_list):
			if(user_list[i] == 1):
				output.write(i + "		Online\n")
			else:
				output.write(i + "		Offline\n")
		output.write("=========================\n")
		self.socket.send(output.getvalue())		
