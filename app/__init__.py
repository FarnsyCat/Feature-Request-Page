import datetime

import bcrypt
from flask import Flask, render_template, request, jsonify, flash, session, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_heroku import Heroku
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
heroku = Heroku(app)
heroku.init_app(app)
db = SQLAlchemy(app)
from app import models
db.create_all([None])
username = "";



@app.route('/')
def index():
    if 'username' in session:
        features = models.Feature.query.filter(models.Feature.assigned == session['username']).order_by(
            models.Feature.clientPriority.asc())
        return render_template('home.html', name=session['username'], features=features)
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
            f = models.User(name=request.form['username'], password=hashpass, active=True)
            db.session.add(f)
            db.session.commit()
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        session.pop('_flashes', None)
        flash('User Already Exists', 'error')
    return render_template('register.html')


@app.route('/featurerequest', methods=['Get'])
def display_featurerequest():
    if 'username' in session:
        return render_template("featurerequest.html", name=session['username']);
    return redirect(url_for('index'))


@app.route('/features', methods=['Get'])
def display_features():
    if 'username' in session:
        featurerequest = models.Feature.query.all()
        return render_template("features.html", featurerequest=featurerequest, name=session['username'])
    return redirect(url_for('index'))

@app.route('/features/<feature_identifier>', methods=['Get'])
def show_item_info(feature_identifier):
    if 'username' in session:
        feature = models.Feature.query.get(feature_identifier)
        messages = models.MessageBoard.query.filter(models.MessageBoard.feature_id == feature_identifier).order_by(
            models.MessageBoard.date.asc())
        return render_template('feature.html',feature=feature, messages=messages, name=session['username'])
    return redirect(url_for('index'))

@app.route('/features/<feature_identifier>', methods=['Post'])
def save_item_info(feature_identifier):
    if 'username' in session:
        feature = models.Feature.query.get(feature_identifier)
        if request.form['submit']=='Assign':
            feature.assigned = name=session['username']
            feature.completed = 2
            session.pop('_flashes', None)
            flash('Feature assigned to you!')
        elif request.form['submit']=='Complete':
            priority = feature.clientPriority
            feature.completed = 3
            feature.assigned = "Complete"
            feature.clientPriority = 0
            prioritycheck = models.Feature.query.filter(
                models.Feature.clientPriority == priority and models.Feature.client == feature.client).count()
            if prioritycheck > 0:
                reshuffle = models.Feature.query.filter(models.Feature.client_id == feature.client_id).filter(
                    models.Feature.clientPriority > priority)
                for r in reshuffle:
                    print(prioritycheck)
                    m = models.Feature.query.filter(models.Feature.id == r.id).update(
                        {"clientPriority": models.Feature.clientPriority - 1})
            db.session.commit()
            session.pop('_flashes', None)
            flash('Completed!')
        elif request.form['submit']=='AddComment' and len(request.form['comment']) > 0:
            m = models.MessageBoard(request.form['comment'], session['username'], feature_identifier, datetime.datetime.now())
            db.session.add(m)
            session.pop('_flashes', None)
            flash('Comment Added')
        db.session.commit()
        messages = models.MessageBoard.query.filter(models.MessageBoard.feature_id == feature_identifier).order_by(
            models.MessageBoard.date.asc())
        return render_template('feature.html',feature=feature, messages=messages, name=session['username'])
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
    active = 1
    status = 1
    userassigned = "Unassigned"

    f = models.Feature(title, description, client, clientPriority, datetime.datetime.strptime(targetDate, '%Y-%m-%d'),
                       url, productArea, active, userassigned, status)
    prioritycheck = models.Feature.query.filter(
        models.Feature.clientPriority == clientPriority and models.Feature.client == client).count()
    if prioritycheck > 0:
        reshuffle = models.Feature.query.filter(models.Feature.client_id == client).filter(
            models.Feature.clientPriority >= clientPriority)
        for r in reshuffle:
            m = models.Feature.query.filter(models.Feature.id == r.id).update(
                {"clientPriority": models.Feature.clientPriority + 1})
    db.session.add(f)
    db.session.commit()
    session.pop('_flashes', None)
    flash('New Feature Request Added')
    return render_template("featurerequest.html", name=session['username'])


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


@app.route('/fillfeaturerequest', methods=['Post'])
def fillpriority():
    client = request.form['client_id']
    priority = models.Feature.query.filter(models.Feature.client_id == client).filter(
        models.Feature.completed <= 2).count() + 1

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


app.secret_key = 'so1-super2-secret3-key4'




admin = Admin(app, name='Feature Request Administration', template_mode='bootstrap3')
admin.add_view(ModelView(models.Client, db.session))
admin.add_view(ModelView(models.ProductArea, db.session))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
