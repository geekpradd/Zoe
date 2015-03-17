import subprocess, os

is_git_directory = '.git' in os.listdir(os.getcwd())
tupled = lambda a: (a.split('\t')[1],a.split('\t')[0])
is_folder = lambda a: not '.' in a
#This is for Python 2.4 to 2.6 
def ch(array):
	p = subprocess.Popen(array, stdout=subprocess.PIPE)
	out, err = p.communicate()
	return out

if not 'check_output' in dir(subprocess):
	check_output = ch 
else:
	 check_output = subprocess.check_output
