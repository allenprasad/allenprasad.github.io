# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 22:21:21 2019

@author: Allen Prasad
"""

import os
from flask import Flask, flash, request, redirect, url_for, render_template, session, send_file, Response
from werkzeug.utils import secure_filename




import os.path
import pandas as pd
#os.path.isfile('E:/CA EXAM/templates/upload.html')

os.chdir('/Users/allen-9207/Documents/doc_convertor_app')
#templateEnv.get_template('E:\CA EXAM')
UPLOAD_FOLDER = 'E:/CA EXAM'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            print(">>>>>>>> yes>>>>>>")
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            session['myvar'] = filename
            
            text = pdfparser(file)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            text_file = open("Output_new.txt", "w")
            text_file.write(text)
            return Response(text,
                       mimetype="text/plain",
                       headers={"Content-Disposition":
                                    "attachment;filename=test.txt"})
    return render_template('upload.html')



#@app.route('/dashboard', methods=['GET', 'POST'])
#def dashboard():
#    filter1 = ''
#    filter2 = ''
#    filter3 = ''
#    if request.method == 'POST':
#        chart = request.form['filter_1']
#        filter1 = request.form['filter_1']
#        filter2 = request.form['filter_2']
#        filter3 = request.form['filter_4']   
#    filename = session['myvar']        
#    data = pd.read_csv(UPLOAD_FOLDER+'/'+filename)
#    if filter1 == None or filter1 == '':
#        filter1 = data.columns.tolist()[2]
#    data_new = pd.DataFrame({'x':data[filter1].value_counts().keys().tolist(),
#                             'y':data[filter1].value_counts().values.tolist()})
#    return render_template('dashboard.html',data = data_new.to_json(orient = 'records') ,chart = ['bar_chart'
#                           ,'scatter_plot','bubble_chart'],colours = data.columns.tolist())

import io

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

def pdfparser(data):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    
    count = 0
    for page in PDFPage.get_pages(data.stream,
                                  pagenos, 
                                  maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=False):
        interpreter.process_page(page)
        count +=1
        if count == 1:
           break

    # As pointed out in another answer, this goes outside the loop
    text = retstr.getvalue()

    device.close()
    retstr.close()
    return text


if __name__ == '__main__':
   app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
   app.run(debug = True)    
