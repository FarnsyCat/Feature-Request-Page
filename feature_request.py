import os
import random
from flask_wtf import Form
from flask import Flask, render_template, request, jsonify, flash, session, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import datetime
import models
from flask.ext.wtf import Form
from wtforms.ext.appengine.db import model_form
from database import *
from sqlalchemy.sql import *
import bcrypt

app = Flask(__name__)
init_db()

admin = Admin(app, name='Feature Request Administration', template_mode='bootstrap3')
admin.add_view(ModelView(models.Client, db_session))
admin.add_view(ModelView(models.ProductArea, db_session))
username = "";

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('display_featurerequest'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    login_user = models.User.query.filter(models.User.name == request.form['username'])
    salt = bcrypt.gensalt()
    if login_user.count() == 1:
        for r in login_user:
            hashed = bcrypt.hashpw(request.form['pass'].encode('utf-8'), r.password)
            if hashed == r.password and request.form['username'] == r.name:
                session['username'] = request.form['username']
                session['userrole'] = r.role
                session['userid'] = r.id
                return redirect(url_for('index'))
    session.pop('_flashes', None)
    flash('User name or password does not match', 'error')
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        existing_user = models.User.query.filter(models.User.name == request.form['username']).count()
        if existing_user == 0:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            f = models.User(name=request.form['username'], password=hashpass, active=1)
            db_session.add(f)
            db_session.commit()
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        session.pop('_flashes', None)
        flash('User Already Exists', 'error')
    return render_template('register.html')

@app.route('/featurerequest', methods=['Get'])
def display_featurerequest():
    if 'username' in session:
        return render_template("featurerequest.html");
    return redirect(url_for('index'))

@app.route('/features', methods=['Get'])
def display_features():
    if 'username' in session:
        featurerequest = models.Feature.query.all()
        return render_template("features.html", featurerequest=featurerequest)
    return redirect(url_for('index'))

@app.route('/featurerequest', methods=['Post'])
def save_featurerequest():
    title = request.form['inputTitle']
    description = request.form['inputDescription']
    client = request.form['selectClient']
    clientPriority = request.form['selectPriority']
    targetDate = request.form['inputDate']
    url = request.form['inputURL']
    productArea = request.form['selectProduct']
    addedby = 1
    addeddate = datetime.datetime.now()
    active = 1
    assigned = 1
    client_id = models.Client.query.filter(models.Client.client == client)
    f = models.Feature(title, description, client, clientPriority, datetime.datetime.strptime(targetDate, '%Y-%m-%d'), url, productArea, addedby, addeddate, active, assigned)
    prioritycheck = models.Feature.query.filter(models.Feature.clientPriority == clientPriority and models.Feature.client == client).count()
    if prioritycheck > 0 :
        for c in client_id:
            reshuffle =  models.Feature.query.filter(models.Feature.client_id == c).filter(models.Feature.clientPriority >= clientPriority)
            for r in reshuffle :
                m = models.Feature.query.filter(models.Feature.id == r.id).update({"clientPriority": models.Feature.clientPriority + 1})
    db_session.add(f)
    db_session.commit()
    session.pop('_flashes', None)
    flash('New Feature Request Added')
    return render_template("featurerequest.html")

@app.route('/fillfeaturerequest', methods=['Get'])
def fillclient():
    client = models.Client.query.all()
    product = models.ProductArea.query.all()
    cliententries = [dict(client_id=c.id, clientName=c.client) for c in client]
    productentries = [dict(product_id=p.id, productName=p.productarea) for p in product]
    data = {
        'status': 'OK',
        'clients': cliententries,
        'products': productentries
    }
    return jsonify(data)

@app.route('/ViewFeatures', methods=['Get'])
def viewFeatures():
    client = models.Client.query.all()
    product = models.ProductArea.query.all()
    cliententries = [dict(client_id=c.id, clientName=c.client) for c in client]
    productentries = [dict(product_id=p.id, productName=p.productarea) for p in product]
    data = {
        'status': 'OK',
        'clients': cliententries,
        'products': productentries
    }

@app.route('/fillfeaturerequest', methods=['Post'])
def fillpriority():
    client = request.form['client_id']
    priority = models.Feature.query.filter(models.Feature.client_id == client).count() + 1

    data = {
        'status': 'OK',
        'priority': priority,
    }
    return jsonify(data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/getclients', methods=['Get'])
def getclients():
    clients = models.Client.query.all()
    cliententries = [dict(client_id=c.id, clientName=c.client) for c in clients]
    data = {
        'status': 'OK',
        'clients': cliententries,
    }
    return jsonify(data)

@app.route('/adminclients', methods=['Get'])
def clientspage():
    return render_template("adminclients.html");


if __name__ == '__main__':
    app.secret_key = 'so1-super2-secret3-key4'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()