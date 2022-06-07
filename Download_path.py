import os
import platform

rootpath='/Users'
plt = platform.system()

def get_home_path(home):
    if plt == "Windows":                    #if system is Windows
        path=os.path.join('C:\\','Users',home)
    elif plt == "Linux":                    #if system is Linux
        path=os.path.join(rootpath,home)
    elif plt == "Darwin":                  #if system is MacOS
        path=os.path.join(rootpath,home)
    else:
        print("Unidentified system")
    return path

def download_paths(home):
    dirs=[]
    path=get_home_path(home)
    for i in (os.listdir(path)):
        if os.path.isdir(os.path.join(path,i)) and not i.startswith('.'):
            dirs.append(i)
    return dirs
