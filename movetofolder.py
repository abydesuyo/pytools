import os

access_rights = 0o755

confpath = os.getcwd()
conf = open(confpath + '/config/movetofolder.conf')

rootdir = conf.readline().rstrip()
splitter = conf.readline().rstrip()
exclude = conf.readline().rstrip().split(',')


os.chdir(rootdir)

for item in os.listdir(rootdir):
	# print(rootdir+item)
	if os.path.isfile(rootdir+item):
		# print(item)
		foldername = item.split('.')[0].split(splitter)
		# print(foldername)
		counter = 0
		for wildcard in foldername:
			if wildcard in exclude:
				foldername = foldername[:counter]
				break
			counter = counter + 1
		foldername = '-'.join(foldername)
		# print(foldername)
		os.chdir(rootdir + "../")
		if not foldername in os.listdir("."):
			print("Need to Create Directory %s" % foldername)
			try:
			    os.mkdir(foldername, access_rights)
			except OSError:
			    print ("Creation of the directory %s failed" % foldername)
			else:
			    print ("Successfully created the directory %s" % foldername)
		else:
			print("Directory Exists %s" %foldername)

		try:
			# print(len(rootdir+foldername+"/"+item))
			# print(oct(os.stat(rootdir+item).st_mode))
			targetDir = os.getcwd().replace('\\','/')
			# print("Source %s" % os.access(rootdir+item,os.W_OK))
			# print("Dest %s" % os.access(targetDir+'/'+foldername,os.W_OK))

			os.rename(rootdir+item, targetDir+'/'+foldername+"/"+item)
			print ("%s moved to %s" %(item, targetDir+'/'+foldername))
		except OSError as ex:
			print("Move failed for %s" % item)
			print(ex)
			exit(1)
		else:
			continue


