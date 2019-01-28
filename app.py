# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 22:21:21 2019

@author: Allen Prasad
"""

import os
from flask import Flask, flash, request, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename


import os.path
import pandas as pd
os.path.isfile('E:/CA EXAM/templates/upload.html')

os.chdir('E:/CA EXAM')
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('dashboard',
                                    filename=filename))
    return render_template('upload.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    filter1 = ''
    filter2 = ''
    filter3 = ''
    if request.method == 'POST':
        chart = request.form['filter_1']
        filter1 = request.form['filter_1']
        filter2 = request.form['filter_2']
        filter3 = request.form['filter_4']   
    filename = session['myvar']        
    data = pd.read_csv(UPLOAD_FOLDER+'/'+filename)
    if filter1 == None or filter1 == '':
        filter1 = data.columns.tolist()[2]
    data_new = pd.DataFrame({'x':data[filter1].value_counts().keys().tolist(),
                             'y':data[filter1].value_counts().values.tolist()})
    return render_template('dashboard.html',data = data_new.to_json(orient = 'records') ,chart = ['bar_chart'
                           ,'scatter_plot','bubble_chart'],colours = data.columns.tolist())

if __name__ == '__main__':
   app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
   app.run(debug = True)    