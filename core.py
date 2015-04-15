from ftplib import FTP 

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

	def get_files(self, dir=None):
		print (self.pwd(),dir)
		if dir is None:
			folders = self.get_folders()
			return [x for x in self.nlst() if not x in folders]

		
		folders = [dir+'/'+x for x in self.get_folders(dir)]
		try:
			return [x for x in self.nlst(self.pwd()+'/'+dir) if not x in folders]
		except:
			return [x for x in self.nlst() if not x in folders]
	def get_folders(self,dir=None):
		ret = []
		def parse(line):
			    if line[0] == 'd':
			        ret.append(line.rpartition(' ')[2])   # gives you the name of a directory
		if dir is not None:
			self.cwd(dir)
		self.dir(parse)
		self.cwd('/')
		return ret
	def remove_file(self, filename):
		original = filename 
		while '/' in filename:
			folder, filename = filename.split('/')[0], filename.replace(filename.split('/')[0]+'/','')
			if not folder in self.nlst():
				self.mkd(folder)
			self.cwd(folder)
			if '/' in filename:
				continue 
			else:
				self.delete(filename)
				self.cwd('/')
		if not '/' in original:
			self.delete(filename)
	def write_file(self,filename, newname=None):
		original = filename 
		while '/' in filename:
			folder, filename = filename.split('/')[0], filename.replace(filename.split('/')[0]+'/','')
			if not folder in self.nlst():
				self.mkd(folder)
			self.cwd(folder)
			if '/' in filename:
				continue 
			else:
				file = open(original, 'rb')
				stor_str = "STOR {0}".format(filename)
				self.storbinary(stor_str, file)
				self.cwd('/')
				file.close()

		if not '/' in original:
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