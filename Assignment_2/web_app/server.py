import bottle
from bottle import route, request, run, template
import sys

WEB_ROOT = ""
PORT = ""
UPLOAD_DIR = "uploads/"

# serve static files.
@bottle.get('/<filename:path>')
def serve_index(filename):
    return bottle.static_file(filename, root=WEB_ROOT)

# serve index.html for base request.
@route("/", method = "GET")
def home():
    bottle.redirect("/index.html")

# This is adapted from bottle example for file upload
# <http://bottlepy.org/docs/dev/tutorial.html>
@route('/upload', method='POST')
def do_upload():
    data = request.files.data
    filename = request.forms.name

    if filename and data and data.file:
        # make sure no-one is trying overwrite files lower than the uploads
        # directory.
        fasta_extension = ".fasta"
        if not fasta_extension in filename:
            return "file must have extension '.fasta'"

        if not filename[:-len(fasta_extension)].isalnum():
            return "filename must be alpha-numeric!"

        # save file
        with open(WEB_ROOT+UPLOAD_DIR+filename,'w') as open_file:
            open_file.write(data.file.read())

        # report successful upload.  This must be over-written once analysis
        # is done.
        return "You successfully uploaded %s." % filename

    return "You missed a field."

def main(argv):
    if len(argv) is not 3:
        print "invalid use: python server.py <WEB_ROOT> <PORT>"
        sys.exit(2)
    WEB_ROOT = argv[1]
    PORT = argv[2]
    bottle.debug(True)
    bottle.run(host='localhost', PORT=PORT)

if __name__ == "__main__":
    main(sys.argv)
