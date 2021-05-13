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
outname = 'README.sql.md'
## READ: Make list of file in a folder
files = Util().getFileList(in_folder, ext='sql')
files.sort()

#print('files: ', files)
## PROCESS: Read all files

readme = []
#print('# Changes')
readme.append('\n')
readme.append('# Changes')
readme.append('\n')
readme.append('| file | type | detail |')
readme.append('| ---- | ------- | ------ |')


for f in files:

    lines = Util().getLines(in_folder, f)

    lines = [ln for ln in lines if re.search('[-]+[ ]+[A-Za-z]+[ ]+[\.0-9]+[:]',ln)]

    for ln in lines:
        ln = '| {} | {} |'.format(f , ln.strip().replace('-- ','').replace(': ', ' | ').replace('\n',''))
        readme.append(ln)

#print('# Order of Creation')
readme.append('\n')
readme.append('# Order of Creation')
readme.append('\n')
readme.append('| file | type | detail |')
readme.append('| ---- | ------- | ------ |')

for f in files:

    lines = Util().getLines(in_folder, f)

    lines = [ln for ln in lines if re.search('[-]+[ ]+[A-Za-z]+[:]',ln)]
    #lines = [ln for ln in lines if re.search('[ACEGLNRST]+[;]',ln)]

    for ln in lines:
        ln = '| {} | {} |'.format(f , ln.strip().replace('-- ','').replace(': ', ' | ').replace('\n',''))
        readme.append(ln)
#print('# Functions')
'''
readme.append('\n')

readme.append('# Functions')
readme.append('\n')
readme.append('| file | version | name | returns |')
readme.append('| ---- | ------- | ------- | ------ |')

for f in files:
    lines = Util().getLines(in_folder, f)
    lines = [ln for ln in lines if re.search('[CREATE][ ]+[OR]+[ ]+[REPLACE]+[ ]+[FUNCTION]',ln)]
    for ln in lines:
        ln = '| {} | {} |'.format(f , ln.strip().replace('CREATE OR REPLACE FUNCTION','').replace('.',' | ').replace('RETURNS',' | ').replace('\n',''))
        #print('ln: ', ln)
        readme.append(ln)
'''
readme.append('\n')
readme.append('# Database')
readme.append('\n')
readme.append('| file | Database | role')
readme.append('| ---- | ------- | --------- |')
# commands = ['CREATE','ALTER', 'GRANT','SET']

for f in files:
    lines = Util().getLines(in_folder, f)
    #    lines = [ln for ln in lines if re.search('^[Cc][Rr][Ee][Aa][Tt][Ee][ ]+ ',ln)]
    # print('lines', lines)

    lines = [ln for ln in lines if re.search("^CREATE DATABASE", ln)]

    for ln in lines:
        ln = ln.split('--')
        ln = '| {} | {} |'.format(f, ln[0].replace('CREATE DATABASE','').replace(';', ' ').replace(' to ', ' | ').replace('\n', ''))

        readme.append(ln)

readme.append('\n')
readme.append('# EXTENSION')
readme.append('\n')
readme.append('| file | EXTENSION |')
readme.append('| ---- | ------- |')
# commands = ['CREATE','ALTER', 'GRANT','SET']

for f in files:
    lines = Util().getLines(in_folder, f)
    #    lines = [ln for ln in lines if re.search('^[Cc][Rr][Ee][Aa][Tt][Ee][ ]+ ',ln)]
    # print('lines', lines)

    lines = [ln for ln in lines if re.search("^CREATE EXTENSION", ln)]

    for ln in lines:
        ln = ln.split('--')
        ln = '| {} | {} |'.format(f, ln[0].replace('CREATE EXTENSION IF NOT EXISTS','').replace('.',' | ').replace(';', ' ').replace(' to ', ' | ').replace('\n', ''))

        readme.append(ln)

readme.append('# Roles')
readme.append('\n')
readme.append('| file | Role |')
readme.append('| ---- | ------- |')
#commands = ['CREATE','ALTER', 'GRANT','SET']

for f in files:
    lines = Util().getLines(in_folder, f)
    #    lines = [ln for ln in lines if re.search('^[Cc][Rr][Ee][Aa][Tt][Ee][ ]+ ',ln)]
    #print('lines', lines)

    lines = [ln for ln in lines if re.search("^CREATE ROLE",ln)]
    
    for ln in lines:
        ln = ln.split('--')
        ln = '| {} | {} |'.format(f , ln[0].replace('CREATE ROLE','').replace('.',' | ').replace(';',' ').replace(' to ',' | ').replace('\n',''))

        readme.append(ln)

readme.append('# Schema')
readme.append('\n')
readme.append('| file | Schema |')
readme.append('| ---- | ------- |')
# commands = ['CREATE','ALTER', 'GRANT','SET']

for f in files:
    lines = Util().getLines(in_folder, f)
    #    lines = [ln for ln in lines if re.search('^[Cc][Rr][Ee][Aa][Tt][Ee][ ]+ ',ln)]
    # print('lines', lines)

    lines = [ln for ln in lines if re.search("^CREATE SCHEMA", ln)]

    for ln in lines:
        ln = ln.split('--')
        ln = '| {} | {} |'.format(f, ln[0].replace('CREATE SCHEMA if not exists','').replace('.',' | ').replace(';', ' ').replace(' to ', ' | ').replace('\n', ''))

        readme.append(ln)

readme.append('# Type')
readme.append('\n')
readme.append('| file | Schema | Name')
readme.append('| ---- | ------- | --------- |')
# commands = ['CREATE','ALTER', 'GRANT','SET']

for f in files:
    lines = Util().getLines(in_folder, f)
    #    lines = [ln for ln in lines if re.search('^[Cc][Rr][Ee][Aa][Tt][Ee][ ]+ ',ln)]
    # print('lines', lines)

    lines = [ln for ln in lines if re.search("^CREATE TYPE", ln)]

    for ln in lines:
        ln = ln.split('--')
        ln = '| {} | {} |'.format(f, ln[0].replace('CREATE TYPE','').replace('.',' | ').replace(';', ' ').replace(' to ', ' | ').replace('\n', ''))

        readme.append(ln)


readme.append('# Table')
readme.append('\n')
readme.append('| file | Schema | Table')
readme.append('| ---- | ------- | --------- |')
# commands = ['CREATE','ALTER', 'GRANT','SET']

for f in files:
    lines = Util().getLines(in_folder, f)
    #    lines = [ln for ln in lines if re.search('^[Cc][Rr][Ee][Aa][Tt][Ee][ ]+ ',ln)]
    # print('lines', lines)

    lines = [ln for ln in lines if re.search("^CREATE TABLE", ln.upper())]

    for ln in lines:
        ln = ln.split('--')
        ln = '| {} | {} |'.format(f, ln[0].replace('CREATE TABLE if not exists','').replace('.',' | ').replace(';', ' ').replace(' to ', ' | ').replace('\n', ''))

        readme.append(ln)

readme.append('# Unique Index')
readme.append('\n')
readme.append('| file | Name | Schema | Table and Indices |')
readme.append('| ---- | ------- | ------ | ------------- |')
# commands = ['CREATE','ALTER', 'GRANT','SET']

for f in files:
    lines = Util().getLines(in_folder, f)
    #    lines = [ln for ln in lines if re.search('^[Cc][Rr][Ee][Aa][Tt][Ee][ ]+ ',ln)]
    # print('lines', lines)

    lines = [ln for ln in lines if re.search("^CREATE UNIQUE", ln.upper())]

    for ln in lines:
        ln = ln.split('--')
        ln = '| {} | {} |'.format(f, ln[0].replace('CREATE UNIQUE INDEX IF NOT EXISTS','').replace('ON',' | ').replace('.',' | ').replace(';', ' ').replace(' to ', ' | ').replace('\n', ''))

        readme.append(ln)


readme.append('# Functions')
readme.append('\n')
readme.append('| file | Schema | FUNCTION | Returns |')
readme.append('| ---- | ------- | --------- | ------- |')
for f in files:
    lines = Util().getLines(in_folder, f)
    #    lines = [ln for ln in lines if re.search('^[Cc][Rr][Ee][Aa][Tt][Ee][ ]+ ',ln)]
    # print('lines', lines)

    lines = [ln for ln in lines if re.search("^CREATE OR REPLACE FUNCTION", ln)]

    for ln in lines:
        ln = ln.split('--')
        ln = '| {} | {} |'.format(f, ln[0].replace('CREATE OR REPLACE FUNCTION','').replace('.',' | ').replace('RETURNS',' | ').replace(';', ' ').replace(' to ', ' | ').replace('\n', ''))

        readme.append(ln)

'''

readme.append('\n')
readme.append('| file | privileges | role')
readme.append('| ---- | ------- | --------- |')
for f in files:
    lines = Util().getLines(in_folder, f)
    lines = [ln for ln in lines if re.search('^[Gg][Rr][Aa][Nn][Tt]+ ',ln)]
    lines = [ln for ln in lines if re.search('^[Gg][Rr][Aa][Nn][Tt]+ ',ln)]

    for ln in lines:
        ln = ln.split('--')
        ln = '| {} | {} |'.format(f , ln[0].replace(';',' ').replace(' to ',' | ').replace('\n',''))

        readme.append(ln)
'''
for ln in readme:
    print(ln)

Util().writeLines(out_folder,outname,readme)

