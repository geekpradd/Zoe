import os, sys
from core import ftp
from collections import defaultdict
from subprocess import check_output
import pickle 
import getpass

is_git_directory = '.git' in os.listdir(os.getcwd())
tupled = lambda a: (a.split('\t')[1],a.split('\t')[0])

# class Connection(ftp):
# 	def __init__(self):

class Dictionary(object):
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

D = Dictionary()

def generate_dict(output):
	string = output.decode('utf-8').split('\n\n')[-1]
	tuples_list =  [tupled(a) for a in string.split('\n')[:-1:]]
	return dict(tuples_list)

def push():
	if not 'zoe.conf' in os.listdir(os.getcwd()):
		main()
	else:
		output = check_output(["git", "show", "--name-status"])
		print(generate_dict(output))

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
		D.configuration = dictionary
	else:
		dictionary = D.configuration
		try:
			client = ftp(dictionary['host'], dictionary['user'], dictionary['passwd'])
			print ("Connection Successful to FTP.. Everything is working fine")
		except Exception as e:
			print ("You have given incorrect password, username or host. Enter zoe --override to override your previous settings and fix your mistakes")

if __name__=='__main__':
	if "push" in sys.argv:
		push()
	else:
		main()