import sys
from git import *

## Call me from the command line with the location where
## you want your document git repo to exist, for exampte:
## '/Users/rkadyb/document-store.git
def initialize(path):
    repo = Repo.init(path, bare=True)
    return repo.bare



if __name__ == "__main__":
    if not (len(sys.argv) == 2):
        print("Call me from the command line with the location where \n" + \
              "you want your document git repo to exist, for example: \n" + \
              "/Users/rkadyb/document-store.git")

    else:
        if initialize(str(sys.argv[1])):
            print("initialized an empty git repo at "+str(sys.argv[1]))
        else:
            print("Something went wrong")
