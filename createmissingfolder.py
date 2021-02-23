import os

rootdir = "x:/Movies/"

for item in os.listdir(rootdir):
	if os.path.isdir(rootdir + item):
		for subitem in os.listdir(rootdir+item):
			if os.path.isfile(rootdir+item+'/'+subitem):
				movienamearr =  subitem.split('.')
				movienamearr.pop()
				moviename = ''.join(movienamearr)
				if moviename != 'Thumbs' and moviename != '_' and moviename != '':
					# print moviename
					cmdmake = rootdir+item+'/'+moviename
					print cmdmake
					os.mkdir(cmdmake)
					# os.system(cmdmake)
					movoriginal = rootdir+item+'/'+subitem 
					movenew = rootdir+item+'/'+moviename+'/'+subitem
					# print cmdmove
					print movoriginal, movenew
					os.rename(movoriginal, movenew)
				print "All done, I love Fluffs"


