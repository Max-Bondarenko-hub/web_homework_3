import os, shutil


folder1 = r'E:\folder1'
folder2 = r'E:\folder2'
shutil.rmtree(folder2)
shutil.copytree(folder1, folder2)

print('Files and folders are restored!')


