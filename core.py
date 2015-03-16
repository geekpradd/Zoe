from ftplib import FTP 
from io import BytesIO

class ftp(FTP):
	def __init__(self,host, user='', passwd=''):

		super(ftp,self).__init__(host) 
		self.login(user=user, passwd=passwd)

	def read_file(self, file):
		class Reader:
			def __init__(self):
				pass
			def __call__(self,s):
				self.data = s
		r = Reader()
		self.retrbinary('RETR ' + file, r)
		return r.data 

	def get_files(self):
		return self.nlist()

	def write_file(self,filename, newname=None):
		file = open(filename, 'rb')
		if newname is None:
			stor_str = "STOR {0}".format(filename)
		else:
			stor_str = "STOR {0}".format(newname)

		self.storbinary(stor_str, file)
		file.close()

if __name__ == '__main__':
	a = ftp('127.0.0.1','geek','12345')
	a.write_file('steps.md', newname='process.md')
	with open('new.md','wb') as f:
		f.write(a.read_file('process.md'))
	print (a.nlst())