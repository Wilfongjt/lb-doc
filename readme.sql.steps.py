#################
# SCRIPT: Write SQL ReadMe.md
#################
# set source folder relative to this file
# get list of files
# process .sql files
# pluck all lines with regex
# format as md table
# write to README.md in source file


from util import Util
import re
in_folder = '../one_db/sql'
out_folder = '../'
outname = 'README.sql.process.md'
## READ: Make list of file in a folder
files = Util().getFileList(in_folder, ext='sql')
files.sort()

#print('files: ', files)
## PROCESS: Read all files

readme = []
#print('# Changes')
readme.append('\n')
readme.append('# Process')
readme.append('\n')
indent = '  '
for f in files:
    first = True
    offset = '\t'
    indent = offset
    lines = Util().getLines(in_folder, f)

    #lines = [ln for ln in lines if re.search('[-]+[ ]+[\[A-Za-z]+[ ]+[\.0-9]+[\]]',ln)]
    lines = [ln for ln in lines if re.search('[ \t]+[-]+[ \t]+[\[]',ln)]
    fails =[]
    for ln in lines:
        ln = ln.lstrip(' ').replace('-- ','').replace('\n','')
        #ln = ln.replace('-- ','')
        if '[Function:' in ln:
            first = True

        if first:
            first = False
            ln = ln.replace('[','### ').replace(']','')
            readme.append('{}'.format(ln))
        elif ln.find('[Description') > -1:
            ln = ln.replace('[', '* ').replace(']', '')
            readme.append('{}'.format(ln))
        elif ln.find('[Parameters') > -1:
            ln = ln.replace('[', '* ').replace(']', '')
            readme.append('{}'.format(ln))
        elif ln.find('[Return') > -1:
            readme.append('{}{} \n'.format('1. ',ln))
            if len(fails) > 0:
                readme.append('* {}'.format('\n * '.join(fails)))
            fails =[]
        elif ln.find('Fail') > -1:
            fails.append(ln)
        else:
            readme.append('{}{}'.format('1. ',ln))


for ln in readme:
    print(ln)

Util().writeLines(out_folder,outname,readme)

