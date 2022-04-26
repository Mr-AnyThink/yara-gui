from flask import *
import yara
import shutil
import os
from werkzeug.utils import secure_filename

#from werkzeug import secure_filename
app = Flask(__name__)
CWD = os.path.dirname(os.path.realpath(__file__)) #get current path
outputdir = CWD + '/upload/'	
file_exists = os.path.exists(outputdir) #check if upload folder exists
if file_exists == False: # if not exist create one
	os.mkdir(outputdir) 

app.config["UPLOAD_FOLDER"] = outputdir #mention full path where uploaded files will be stored

#Call index.html whenever web is accessed
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deleteUpload')
def deleteUpload():
    file_exists = os.path.exists(outputdir) #check if upload folder exists
    if file_exists == True:
        for f in os.listdir(outputdir):
            print(f)
            os.remove(os.path.join(outputdir, f))   
    return redirect('/')
 
#upload file
@app.route('/uploader', methods = ['GET', 'POST'])
def save_upload():
    if request.method == "POST":
        #yara_index = request.form['yaraindex']
        f = request.files["file"]

        #Handle if file is not provided
        if f.filename == '':
            return render_template('index.html', no_file = 0)

        #Read filname and save to "upload folder"
        filename = secure_filename(f.filename)
        f.save(app.config["UPLOAD_FOLDER"] + filename)
        filepath = str(app.config["UPLOAD_FOLDER"] + filename)

        #call fucntion to check yara
        matches = yaracheck(filepath)

        # Send matched rule back to index.html with name "rule_matches", it'll be referenced in index.html
        return render_template('index.html', rule_matches = matches, filename = filename)

#check file against yara
def yaracheck(filepath_u):
    yara_index = CWD + '/rules/active_index.yar'
    rules = yara.compile(filepath=str(yara_index).strip())
    matches = rules.match(filepath_u.strip()) #in index.yar, included file must have full path. Also remove "MALW_AZORULT.yar" entry as it is causing error for yara-python
    if len(matches) == 0:
        return ('None')
    else:
        return(matches) 


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)