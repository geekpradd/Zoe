import os, sys
from core import ftp 
from subprocess import check_output
import pickle 
import getpass

is_git_directory = '.git' in os.listdir(os.getcwd())

def push():
	if not 'zoe.conf' in os.listdir(os.getcwd()):
		main()
	else:
		output = check_output(["git", "show", "--name-status"])
		string = output.decode('utf-8').split('\n\n')[-1]
		print (string)
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
		with open('zoe.conf', 'wb') as f:
			f.write(pickle.dumps(dictionary))
	else:
		with open('zoe.conf', 'rb') as f:
			dictionary = pickle.loads(f.read())
		try:
			client = ftp(dictionary['host'], dictionary['user'], dictionary['passwd'])
			print ("Connection Successful to FTP.. Everything is working fine")
		except Exception as e:
			print ("You have given incorrect password, username or host. Enter zoe --override to override your previous settings and fix your mistakes")

if __name__=='__main__':
	if sys.argv[1] == "push":
		push()
	else:
		main()