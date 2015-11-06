import bottle
import random
import classifier
import json
import threading
from bottle import route, request, run, template
from Bio import SeqIO
import blastquery
import sys
import os

WEB_ROOT = ""
PORT = ""
UPLOAD_DIR = "/uploads/"

def query_seqs_in_file(filename, new_dir_path):
    print "printing out sequences!"
    try:
        os.stat(new_dir_path)
    except:
        os.mkdir(new_dir_path)

    records = SeqIO.parse(filename, "fastq")
    i = 0
    file_names=[]
    json_dest = new_dir_path+"data.json"
    for record in records:
        print "printing out a sequence!"
        print "%s: %d" % (record.id, len(record.seq))
        xml_obj = blastquery.query(record.seq)
#        print str(xml_obj.read())
        xml_dest=new_dir_path+"file_"+str(i)+".xml"
        with open(xml_dest,'w') as open_file:
            open_file.write(xml_obj.read())
        open_file.close()
        file_names.append(xml_dest)
        species_counts = classifier.getSpeciesFromXMLs(file_names,0)
        with open(json_dest,'w') as open_file:
            json.dump(species_counts,open_file)
        open_file.close()
        i+=1

# serve static files.
@bottle.get('/<filename:path>')
def serve_index(filename):
    print "web_root: " + WEB_ROOT
    return bottle.static_file(filename, root=WEB_ROOT)

# serve index.html for base request.
@route("/", method = "GET")
def home():
    bottle.redirect("/index.html")

# This will return the data needed for pie chart
@route("/get_data",method = "POST")
def get_data():
    #fn=bottle.request.json["file_name"]
    fn = request.forms.get('file_name')
    json_path = WEB_ROOT+UPLOAD_DIR+fn+"_dir/data.json"
    species_counts = json.load(json_path)
    data_to_return = []
    r = lambda: random.randint(0,255)
    for species in species_counts:
        color = ('#%02X%02X%02X' % (r(),r(),r()))
        color_highlight = ('#%02X%02X%02X' % (r(),r(),r()))
        count = species_counts[species]
        data_to_return.append({"label":species,
            "value":count,"color":color,"highlight":color_highlight})
    return data_to_return


# This is adapted from bottle example for file upload
# <http://bottlepy.org/docs/dev/tutorial.html>
@route('/upload', method='POST')
def do_upload():
    data = request.files.data
    filename = request.forms.name
    print "in route"

    print "filename: "+filename
    if filename and data and data.file:
        print "valid info"
        # make sure no-one is trying overwrite files lower than the uploads
        # directory.
        fastq_extension = ".fastq"
        if not fastq_extension in filename:
            return "file must have extension '.fastq'"

        if not filename[:-len(fastq_extension)].isalnum():
            return "filename must be alpha-numeric!"

        # save file
        dest = WEB_ROOT+UPLOAD_DIR+filename
        with open(dest,'w') as open_file:
            open_file.write(data.file.read())
        open_file.close()

        print "querying now!"
        threading.Thread(target=query_seqs_in_file, args =
                (dest,WEB_ROOT+UPLOAD_DIR+filename+"_dir/")).start()
#        query_seqs_in_file(dest,WEB_ROOT+UPLOAD_DIR+filename+"_dir/")

        # report successful upload.  This must be over-written once analysis
        # is done.
#        return "You successfully uploaded %s." % filename
    
        bottle.redirect("/index.html")

    else:
        return "You missed a field."

def main(argv):
    if len(argv) is not 3:
        print "invalid use: python server.py <WEB_ROOT> <PORT>"
        sys.exit(2)
    global WEB_ROOT
    WEB_ROOT = argv[1]
    PORT = argv[2]
    bottle.debug(True)
    bottle.run(host='localhost', PORT=PORT)

if __name__ == "__main__":
    main(sys.argv)
