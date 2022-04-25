from flask import *
import yara
from werkzeug.utils import secure_filename

#from werkzeug import secure_filename
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = '/home/remnux/Downloads/'
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/uploader', methods = ['GET', 'POST'])
def save_upload():
  if request.method == "POST":
    yara_index = request.form['yaraindex']
    f = request.files["file"]
    filename = secure_filename(f.filename)
    f.save(app.config["UPLOAD_FOLDER"] + filename)
    filepath = str(app.config["UPLOAD_FOLDER"] + filename)
    matches = yaracheck(filepath, yara_index)
    return(str(matches).replace(',','<br/>'))


def yaracheck(filepath_u,yara_index):
    rules = yara.compile(filepath=str(yara_index).strip())
    matches = rules.match(filepath_u.strip())
    if len(matches) == 0:
        return ('No matches Found')
    else:
        return(matches) 


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)