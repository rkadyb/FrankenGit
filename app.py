from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/file/<handle>/<version>')
def get_version(handle, version):
    return "Getting handle: %s version: %s" % (handle, version)

@app.route('/file/<handle>', methods=['GET', 'POST'])
def root_handle(handle):
    if request.method == "POST":
        return "SAVING"
    else:
        return "Getting handle: %s recent version" % (handle)

@app.route('/new/')
def new_handle():
    return "new file handle"

if __name__ == '__main__':
    app.run(debug=True)
