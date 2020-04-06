import os
from run import app
from flask import Flask,Response, url_for,request,render_template,redirect,flash,jsonify
from app.forms import *
from werkzeug.utils import secure_filename
from dxf_generator import dxf_generator as gen
import io
import json


#scheduler = BlockingScheduler(timezone="Europe/Helsinki")

@app.route('/')
def index():
    return render_template('generator_base.html')


@app.route('/analyse/')
def analyse():
    return render_template('analyse.html')

def allowed_file(filename,extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extensions

@app.route('/gen/watchstrap')
def watchstrap():
    return render_template('watchstrap.html')


@app.route('/gen/phonecase', methods=['GET', 'POST'])
def phonecase():
    form = PhonecaseForm(request.form)
    if request.method == 'POST' and form.validate():

        dxf = gen.generate_phonecase(float(form.height.data), float(form.width.data), float(form.depth.data), form.text.data)
        with io.StringIO() as f:
            dxf.write(f)
            return Response(f.getvalue(), mimetype="application/dxf", headers={"Content-disposition":"attachment; filename=phonecase.dxf"})
    return render_template('phonecase.html', form=form)

@app.route('/gen/pencilcase', methods=['GET', 'POST'])
def pencilcase():
    form = TextForm(request.form)
    if request.method == 'POST' and form.validate():

        dxf = gen.generate_pencilcase(form.text.data)
        with io.StringIO() as f:
            dxf.write(f)
            return Response(f.getvalue(), mimetype="application/dxf", headers={"Content-disposition":"attachment; filename=pencilcase.dxf"})
    return render_template('pencilcase.html', form=form)

@app.route('/gen/glassescover', methods=['GET', 'POST'])
def glassescover():
    form = TextForm(request.form)
    if request.method == 'POST' and form.validate():
        dxf = gen.generate_glassescover( form.text.data)
        with io.StringIO() as f:
            dxf.write(f)
            return Response(f.getvalue(), mimetype="application/dxf", headers={"Content-disposition":"attachment; filename=glassescover.dxf"})
    return render_template('glassescover.html', form=form)

@app.route('/gen/wallet', methods=['GET', 'POST'])
def wallet():
    form = WalletForm(request.form)
    if request.method == 'POST' and form.validate():
        if int(form.version.data) == 1:
            dxf = gen.generate_wallet_one(form.text.data)
        elif int(form.version.data) == 2:
            dxf = gen.generate_wallet_two(form.text.data)
        with io.StringIO() as f:
            dxf.write(f)
            return Response(f.getvalue(), mimetype="application/dxf", headers={"Content-disposition":"attachment; filename=wallet.dxf"})
    return render_template('wallet.html', form=form)

@app.route('/gen/watchstrap', methods=['GET', 'POST'])
def watch():
    form = WatchstrapForm(request.form)
    if request.method == 'POST' and form.validate():
        if  form.nail.data:
            dxf = gen.generate_watchstrap(float(form.top.data),float(form.buckle.data),float(form.length.data), text=form.text.data, nail=float(form.nail.data),version=int(form.version.data))
        else:
            dxf = gen.generate_watchstrap(float(form.top.data),float(form.buckle.data),float(form.length.data), text=form.text.data,version=int(form.version.data))
        with io.StringIO() as f:
            dxf.write(f)
            return Response(f.getvalue(), mimetype="application/dxf", headers={"Content-disposition":"attachment; filename=watchstrap.dxf"})
    return render_template('watchstrap.html', form=form)


@app.route('/about')
def about():
    return 'The about page'

