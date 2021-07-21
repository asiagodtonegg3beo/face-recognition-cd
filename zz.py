import os
import sys


rootdir = 'dataset/B0642021'

def su():
    fileList = []
    fileSize = 0
    folderCount = 0
    for root, subFolders, files in os.walk(rootdir):
        folderCount += len(subFolders)
        for file in files:
            f = os.path.join(root,file)
            fileSize = fileSize + os.path.getsize(f)
            #print(f)
            fileList.append(f)
    return len(fileList)
'''
print("Total Size is {0} bytes".format(fileSize))
print("Total Files", len(fileList))
print("Total Folders", folderCount)
'''