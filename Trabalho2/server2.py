from flask import Flask, render_template, request
from werkzeug import secure_filename
import os
app = Flask(__name__)

UPLOAD_FOLDER = './tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

# URL
# file:///home/willdoliver/Desktop/2018.2/Integrados/Trabalho2/templates/front2.html
@app.route('/')
def upload():
   return render_template('front2.html')
    
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
        dados = request.form.to_dict()

        f = request.files['uploadedFile']
        alt = dados['alternancia']
        print('Numero de alternancia: ' + alt)

        f.save(secure_filename(os.path.join(app.config['UPLOAD_FOLDER'],f.filename)))
        #f = secure_filename(f.filename)
        #f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        print('file uploaded successfully')

        readFile(alt)
        return render_template('front2.html')

def readFile(alt):
    print('Tratamento do arquivo iniciado')

    file = open('tmp_sinal.txt', 'r')
    fila_saida = open('tmp_sinalMod.txt', 'w')
    #print file.read() 

    # Captura dadosdo arquivo original e altera o valor
    saida = []
    for line in file: 
        #print(line)
        saida.append(round((float(line) + float(alt)), 2))
    #print(saida)

    # Escreve no arquivo dados modificados
    for num in saida:
        fila_saida.write(str(num))
        fila_saida.write("\n")
        
    print('Tratamento do arquivo finalizado')

        
if __name__ == '__main__':
   app.run(debug = True)