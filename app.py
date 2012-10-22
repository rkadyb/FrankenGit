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


@app.route('/<handle>/versions')
def get_versions(handle):
    return str(numSha(handle)-1)


@app.route('/<handle>/<version>')
def get_version(handle, version):
    return getFile(handle, version)


@app.route('/<handle>', methods=['GET', 'POST'])
def root_handle(handle):
    if handle == "favicon.ico":
        return ""

    ## Adding in a new file
    if handle == "new":
        newFile = request.files['data']
        newHandle = uunewHandle.uunewHandle1().hex
        saved = saveFile(newFile, newHandle)

        return newHandle

    ## Over-writing an exiting file
    if request.method == "POST":
        newFile = request.files['data']

        if os.path.isfile(repoName+"/files/"+handle):
            saved = saveFile(newFile, handle)
        else:
            return make_response("No such file", 404)
        return "saved new file to "+str(handle)
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
        # reset to 0 so the read() actually does something
        f.seek(0)

    filename = getFilename(handle)
    return send_file(f, as_attachment=True, attachment_filename=filename)


def saveFile(fileObj, handle):

    f = open(repoName+"/files/"+handle, 'w')
    f.write(fileObj.stream.read())
    f.close()
    fname = open(repoName+"/files/"+handle+'-filename', 'w')
    fname.write(fileObj.filename)
    fname.close()

    repo = Repo(repoName)
    index = repo.index

    index.add([repoName+"/files/"+handle])
    index.add([repoName+"/files/"+handle+'-filename'])
    commit = index.commit("file with uuhandle "+handle+ " at "+str(time.time()))

    return True


def versionSha(handle, version=None):
    g = Git(repoName)
    shas = g.log('--pretty=%H','--follow','--','files/'+handle).split('\n')
    shas.reverse()
    if not version:
        version = 0
    try:
        return shas[int(version)]
    except IndexError:
        return "No such version number", 400


def numSha(handle, version=None):
    g = Git(repoName)
    shas = g.log('--pretty=%H','--follow','--','files/'+handle).split('\n')
    return len(shas)


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
