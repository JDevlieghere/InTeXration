import os

__author__ = 'Jonas'


for root, dirs, files in os.walk('./intexration/'):
    print(root)
    print("@")
    print(dirs)
    print("@")
    print(files)

