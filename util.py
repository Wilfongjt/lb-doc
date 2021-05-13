import os
from os.path import isfile, join
from os import listdir
from pathlib import Path

class Util():
    def toClassName(self, fileName):
        #parts = fileName.split('.')
        fileName = fileName.replace('-', '.')
        parts = [p.capitalize() for p in fileName.split('.')]
        return ''.join(parts)
    '''
    def harden(self, alist):
        for ln in alist:

            ln = ln.replace('\n','')
            print('            \'{}\','.format(ln))
        return self
    '''
    def getFileExtension(self, filename):
        lst = filename.split('.')[1:]
        ext = '.'.join(lst)
        return ext

    def folder_exists(self, folder):
        exists = os.path.isdir('{}'.format(folder))
        return exists

    def file_exists(self, folder, filename):
        exists = os.path.isfile('{}/{}'.format(folder, filename))
        return exists

    def createFolder(self, folder):
        # create all folders in a given path
        # No trailing / in folder
        #path = folder

        try:
            p=''
            for sub in folder.split('/'):
                if len(sub) > 0:
                    p += '/{}'.format( sub )
                    #print('check folder ', p)
                    if not os.path.exists(p):
                        #print('create folder ', p)
                        os.mkdir('{}/'.format(p))



            #if not self.folder_exists('{}/'.format(path)):
            #    os.mkdir('{}/'.format(path))

            #print("Successfully created the directory %s " % path)
        except OSError:
            path=None
            print("FAILURE: Creation of the directory %s failed" % path)

        return self

    '''
        def createFolder(self, folder):
        # No trailing / in folder
        path = folder

        try:
            
            if not self.folder_exists('{}/'.format(path)):
                os.mkdir('{}/'.format(path))

            #print("Successfully created the directory %s " % path)
        except OSError:
            path=None
            #print("Creation of the directory %s failed" % path)

        return self
    '''

    def deleteFolder(self, folder):
        # Note: You can only remove empty folders.
        if self.folder_exists(folder ):
            print('deleteFolder', folder)
            os.rmdir(folder)
        return self

    def deleteFile(self, folder, file_name):

        if self.file_exists(folder, file_name):
            os.remove("{}/{}".format( folder, file_name ))
        return self

    def getFileList(self, path, ext=None):
        onlyfiles=[]

        if len(listdir(path)) > 0:
            onlyfiles = [f for f in listdir(path) if isfile(join(path, f) )]
            if ext != None:
                onlyfiles = [f for f in onlyfiles if f.startswith(ext) or f.endswith(ext)]

        #return onlyfiles
        return [fn for fn in onlyfiles if '.DS_Store' not in fn]

    def getFileListWalk(self, path, ext=None):
        pathAndFile=[]
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(ext):
                    #print(os.path.join(root, file))
                    pathAndFile.append(os.path.join(root,file))
        return pathAndFile

    def getFolderList(self, path):
        onlyfolders = []

        if len(listdir(path)) > 0:
            onlyfolders = ['{}/{}'.format(path,f) for f in listdir(path) if not isfile(join(path, f))]
            #if ext != None:
            #    onlyfolders = [f for f in onlyfolders if f.startswith(ext) or f.endswith(ext)]

        # return onlyfiles
        return [fn for fn in onlyfolders]

    def stringify(self, key_list):
        # convert integers in list to str
        if len(key_list) == 0:
            return []

        if not (type(key_list[0] is int)):
            return key_list

        return [ str(k) for k in key_list]

    def loadEnv(self, filepath):

        with open(filepath) as file:

            lines = file.readlines()
            for ln in lines:
                if not ln.startswith('#'):
                    #print('lb', ln)
                    #print('split', ln.split('='))
                    ln = ln.split('=')
                    if len(ln) > 2:
                        os.environ[ln[0]]=ln[1]

            #print('type', type(data))
        return self

    def getHomeFolder(self):
        return str(Path.home())

    def getWorkFolder(self, path):
        return '{}/{}'.format(self.getHomeFolder(),path)

    def getResourceProjectFolder(self, suffix=None):
        '''
        returns path to resource folder in the source code
        suffix can be a folder name or a file name
        '''
        rc = os.getcwd()

        #if not (rc.endswith('_app' or rc.endswith('_res'))):
        #    rc = '{}/_res'.format(rc)

        if rc.endswith('_app'):
            rc = rc.replace('/_app','')

        if suffix != None:
            rc ='{}/{}'.format(rc, suffix)

        return rc

    def getLines(self, folder, filename):
        rc = []
        with open('{}/{}'.format(folder, filename)) as f:
           rc = f.readlines()

        return rc

    def writeLines(self, folder, filename, lines):
        rc = []
        with open('{}/{}'.format(folder, filename),'w') as f:
            f.writelines(['{}\n'.format(ln) for ln in lines])
        return self


def main():
    from app_settings import AppSettingsTest
    from dotenv import load_dotenv
    import os

    os.environ['LB-TESTING'] = '1'
    load_dotenv()

    env_folder = Util().getResourceProjectFolder()
    Util().loadEnv('{}/.env'.format(env_folder))

    #appSettings = AppSettingsTest()
    test_folder = "{}/{}".format(str(Path.home()), "test-me" )# user folder
    assert(Util().createFolder(test_folder).folder_exists(test_folder))
    assert(Util().folder_exists(test_folder))
    #
    test_file='test.txt'
    with open('{}/{}'.format(test_folder, test_file), "w") as f:
        f.write("test line")
    assert(Util().file_exists(test_folder, test_file))
    assert(Util().getFileList(test_folder, 'txt') == [test_file])
    assert(not Util().deleteFile(test_folder, test_file).file_exists(test_folder, test_file))
    assert(not Util().deleteFolder(test_folder).folder_exists(test_folder))
    # get extension
    #c_file = 'credentials.db-api-table-table.pg.json._DEP'
    #print('Util().getFileExtension(c_file)',Util().getFileExtension(c_file))
    #assert(Util().getFileExtension(c_file)=='db-api-table-table.pg.json')
    # source folder
    #working_folder_name_default = 'example'
    folderlist = Util().getFolderList(env_folder)
    print('folderlist', folderlist)
    os.environ['LB-TESTING'] = '0'

if __name__ == "__main__":
    main()