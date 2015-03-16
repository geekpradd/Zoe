import os, sys
from core import ftp
from collections import defaultdict
from subprocess import check_output
import pickle 
import getpass

is_git_directory = '.git' in os.listdir(os.getcwd())
tupled = lambda a: (a.split('\t')[1],a.split('\t')[0])

class Config(object):
	@property 
	def configuration(self):
		try:
			with open('zoe.conf', 'rb') as f:
				self._dictionary = pickle.loads(f.read())
			return self._dictionary
		except:
			print("Configuration files have not been set", file=sys.stderr)

	@configuration.setter 
	def configuration(self, dic):
		with open('zoe.conf', 'wb') as f:
			self._dictionary = pickle.dumps(dic)
			f.write(self._dictionary)

	@property
	def commit(self):
		try:
			with open('.zoe.commit', 'r') as f:
				self._commit = f.read()
			return self._commit
		except:
			print("Initial Commit has not been made", file=sys.stderr)

	@commit.setter 
	def commit(self, c):
		with open('.zoe.commit', 'w') as f:
			self._commit = c
			f.write(self._commit)

CONFIG = Config()

class Connection(ftp, Config):
	def __init__(self):
		print ("Initializing Connection to Server")
		super(Connection,self).__init__(self.configuration['host'],self.configuration['user'],self.configuration['passwd'])
		print ("Connection Successful")

	def push_total(self):
		files = check_output(["git", "ls-files"]).decode('utf-8').split('\n')[:-1:]
		for f in files:
			print ("Pushing {0} to FTP Host {1}".format(f,self.configuration['host']))
			self.write_file(f)
		if not '.zoe.commit' in os.listdir(os.getcwd()):
			CONFIG.commit = check_output(["git","rev-parse","--short", "HEAD"]).decode('utf-8')
			

	def push_changed(self,dictionary):
		if check_output(["git","rev-parse","--short", "HEAD"]).decode('utf-8') == CONFIG.commit:
			print ("All changes in the latest commit are already pushed. Please commit your changes in git first.")
			sys.exit(0)
		maps = {'A':self.write_file, 'M':self.write_file, 'D':self.remove_file}
		for file in dictionary:
			if dictionary[file]=="A":
				print ("Adding ", end='')
			elif dictionary[file]=="M":
				print ("Modifying ", end='')
			elif dictionary[file]=="D":
				print ("Deleting", end='')
			print (file)
			maps[dictionary[file]](file)


def generate_dict(output):
	string = output.decode('utf-8').split('\n\n')[-1]
	tuples_list =  [tupled(a) for a in string.split('\n')[:-1:]]
	return dict(tuples_list)

def push(FORCE=False):
	if not 'zoe.conf' in os.listdir(os.getcwd()):
		main()
	else:
		output = check_output(["git", "show", "--name-status"])
		con = Connection()

		if FORCE:
			print ("Pushing all files added in git by force.")
			con.push_total()
			sys.exit(0)
		if not '.zoe.commit' in os.listdir(os.getcwd()):
			print ("First Push: Pushing all files to server")
			con.push_total()
		else:
			con.push_changed(generate_dict(output)) #Push files changed in latest commit 

def main():
	if not is_git_directory:
		print("Current directory is not a git directory", file=sys.stderr) 
		sys.exit(1)

	if not 'zoe.conf' in os.listdir(os.getcwd()):
		print ("Enter Your Configuration Variables ")
		host = input("Enter host IP: ")
		user = input("Enter User Name (Leave blank for none): ")
		passwd = getpass.getpass(prompt="Enter FTP Password (Leave blank for none): ")

		dictionary = {"host": host, "user": user, "passwd": passwd}
		CONFIG.configuration = dictionary
	else:
		dictionary = CONFIG.configuration
		try:
			client = ftp(dictionary['host'], dictionary['user'], dictionary['passwd'])
			print ("Connection Successful to FTP.. Everything is working fine")
		except Exception as e:
			print ("You have given incorrect password, username or host. Enter zoe --override to override your previous settings and fix your mistakes")

if __name__=='__main__':
	if "push" in sys.argv:
		push(FORCE='--force' in sys.argv)
	else:
		main()