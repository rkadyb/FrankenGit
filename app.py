from flask import Flask, request
from git import *
app = Flask(__name__)

repoName = None

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/<handle>/<version>')
def get_version(handle, version):
    return "Getting handle: %s version: %s" % (handle, version)

@app.route('/<handle>', methods=['GET', 'POST'])
def root_handle(handle):
    if handle == "new":
        
        return "new file handle"
        ## TODO return handle
    if request.method == "POST":
        return "SAVING"
    else:
        return "Getting handle: %s recent version" % (handle)

### Handle the creation of new files
def createFile(name, data):
    pass

def parseConfig():
    try:
        global repoName
        config = open("config")
        repoName = config.readline()
        config.close()
    except:
        ## Nothing for now
        pass

    return repoName

if __name__ == '__main__':
    print parseConfig()
    app.run(debug=True)
