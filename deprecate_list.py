'''
Scan for files ending in .dep
Create a GIT command to remove the file from the repo
Leave .dep file in place

'''
from pprint import pprint
import os
from pathlib import Path

from util import Util

print('home', Util().getHomeFolder())
print('Repo folder: ', Util().getWorkFolder('..LyttleBit/code/Development/01-lb-api'))
print('')
# Starting folder
#in_folder = Util().getWorkFolder('..LyttleBit/code/Development/01-lb-api/#10.postres/lb-api/hapi-api/lib/environment')
repo_folder = Util().getWorkFolder('..LyttleBit/code/Development/01-lb-api/#10.postres/lb-api')
#files = Util().getFileList(in_folder, ext='.dep')
#files.sort()
#remove_files = ['GIT rm {}/{}'.format(in_folder, fn.replace('.dep','')) for fn in  Util().getFileList(in_folder, ext='.dep')]
#print('depricated files',files)
#for ln in remove_files:
#    print(ln)
#gitTemplate = 'GIT rm {}'
#print('cd {}'.format(repo_folder))
dep_files = [fn.replace('{}/'.format(repo_folder),'') for fn in  Util().getFileListWalk(repo_folder, ext='.dep')]
#remove_files = ['GIT rm {}'.format(fn.replace('{}/'.format(repo_folder),'').replace('.dep','')) for fn in  Util().getFileListWalk(repo_folder, ext='.dep')]

for fn in dep_files:
    lst = fn.split('/')
    #print(lst)
    filename = lst[len(lst)-1]
    #print('filename', filename)
    lst = lst[0:len(lst)-1]
    #print('lst', lst)
    print('cd {}/{}'.format(repo_folder,'/'.join(lst)))
    print('mv {} {}'.format(filename, filename.replace('.dep','')))
    print('GIT rm {}'.format(filename.replace('.dep','')))

#Util().getFileListWalk(work_folder, ext='.dep')

