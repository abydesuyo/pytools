import os

rootdir = "x:/Movies/"
allfiles = []
for root,dirs,files in os.walk(rootdir, topdown=True):
	# print (files)
	# print (type (files))
	# print (len(files))
	allfiles.extend(files)
	print ("processing ..") 
allfiles.sort()
print (allfiles)
print ("Size of list = ",len(allfiles))


