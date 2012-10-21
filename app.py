from flask import Flask, request, send_file
from git import *
import uuid
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
        global repoName
        newFile = request.files['data']
        id = uuid.uuid1().hex
        try:
            ## Saving the file
            f = open(repoName+"/files/"+id, 'w')
            f.write(newFile.stream.read())
            f.close()

            repo = Repo(repoName)
            index = repo.index

            index.add([repoName+"/files/"+id])
            commit = index.commit("added file with uuid "+id)

        except:
            pass

        return id

    if request.method == "POST":
        return "SAVING"
    else:
        f = open(repoName + '/files/' + handle)
        return send_file(f, as_attachment=True)

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
