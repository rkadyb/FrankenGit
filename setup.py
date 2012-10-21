import sys
import os
from git import *

## Call me from the command line with the location where
## you want your document git repo to exist, for exampte:
## '/Users/rkadyb/document-store.git
def initialize(path):
    repo = Repo.init(path, bare=True)
    return repo.bare

def addDocRepoToConfig(docRepoPath):
    docRepoPath = os.path.expanduser(docRepoPath)
    docRepoPath = os.path.abspath(docRepoPath)
    success = False
    try:
        config = open("config", "w")
        config.write(docRepoPath)
        config.close()
        success = True
    except:
        pass
    return success

if __name__ == "__main__":
    if not (len(sys.argv) == 2):
        print("Call me from the command line with the location where \n" + \
              "you want your document git repo to exist, for example: \n" + \
              "/Users/rkadyb/document-store.git")

    else:
        if initialize(str(sys.argv[1])):
            print("initialized an empty git repo at "+str(sys.argv[1]))
            if addDocRepoToConfig(sys.argv[1]):
                print("Config file updated appropriately")
            else:
                print("WARNING: Config file incorrect")

        else:
            print("Something went wrong")
