from flask import Flask, render_template, request
from werkzeug import secure_filename
import os
app = Flask(__name__)

UPLOAD_FOLDER = './tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

# URL
# file:///home/willdoliver/Desktop/2018.2/Integrados/trabalho2/client/front.php
@app.route('/upload')
def upload():
   return render_template('front2.html')
    
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['uploadedFile']

        f.save(secure_filename(os.path.join(app.config['UPLOAD_FOLDER'],f.filename)))
        #f = secure_filename(f.filename)
        #f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        print('file uploaded successfully')

        readFile()
        return('ok')

def readFile():
    print('teste')

    file = open('tmp_sinal.txt', 'r')
    #print file.read() 
    for line in file: 
        print (line)


        
if __name__ == '__main__':
   app.run(debug = True)