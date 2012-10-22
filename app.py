from flask import Flask, request, send_file
from git import *
import uuid
import os.path
import time

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

app = Flask(__name__)

repoName = None

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/<handle>/<version>')
def get_version(handle, version):
    return getFile(handle, version)

@app.route('/<handle>', methods=['GET', 'POST'])
def root_handle(handle):

    ## Adding in a new file
    if handle == "new":
        global repoName
        newFile = request.files['data']
        id = uuid.uuid1().hex
        try:
            ## Saving the file
            f = open(repoName+"/files/"+id, 'w')
            f.write(newFile.stream.read())
            f.close()
            fname = open(repoName+"/files/"+id+'-filename', 'w')
            fname.write(newFile.filename)
            fname.close()

            repo = Repo(repoName)
            index = repo.index

            index.add([repoName+"/files/"+id])
            index.add([repoName+"/files/"+id+'-filename'])
            commit = index.commit("added file with uuid "+id)

        except:
            pass

        return id

    ## Over-writing an exiting file
    if request.method == "POST":
        saved = False
        id = str(handle)
        newFile = request.files['data']

        try:
            ## Make sure that we are trying to update a valid file
            if os.path.isfile(repoName+"/files/"+id):
                f = open(repoName+"/files/"+id, 'w')
                f.write(newFile.stream.read())
                f.close()
                fname = open(repoName+"/files/"+id+'-filename', 'w')
                fname.write(newFile.filename)
                fname.close()

                repo = Repo(repoName)
                index = repo.index

                index.add([repoName+"/files/"+id])
                index.add([repoName+"/files/"+id+'-filename'])
                commit = index.commit("changed file with uuid "+id+ " at "+str(time.time()))

                saved = True

        except:
            ## Nothing for now
            pass

        if saved:
            return "saved new file to "+str(id)
        else:

            return "could not save file"

    else:
        return getFile(handle)

def getFilename(handle):
    fname = open(repoName + '/files/' + handle + "-filename")
    return fname.readline()

def getFile(handle, version=None):
    if not version:
        f = open(repoName + '/files/' + handle)
    else:
        sha = versionSha(handle, version=version)
        g = Git(repoName)
        output = g.show('%s:files/%s' % (sha, handle))
        f = StringIO()
        f.write(output)
        f.seek(0)

    filename = getFilename(handle)
    return send_file(f, as_attachment=True, attachment_filename=filename)

def versionSha(handle, version=None):
    g = Git(repoName)
    shas = g.log('--pretty=%H','--follow','--','files/'+handle).split('\n')
    shas.reverse()
    if not version:
        version = 0
    return shas[int(version)]

## Get the repoName from our config
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
