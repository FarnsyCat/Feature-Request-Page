from flask import Flask, render_template, request, jsonify, flash
import datetime
import models
from database import *
from sqlalchemy import func

app = Flask(__name__)

init_db()

@app.route('/featurerequest', methods=['Get'])
def display_featurerequest():
    return render_template("featurerequest.html");

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
    f = models.Feature(title, description, client, clientPriority, datetime.datetime.strptime(targetDate, '%Y-%m-%d'), url, productArea, addedby, addeddate, active, assigned)
    prioritycheck = models.Feature.query.filter(models.Feature.clientPriority == clientPriority).count()
    if prioritycheck > 0 :
        reshuffle =  models.Feature.query.filter(models.Feature.clientPriority >= clientPriority)
        for r in reshuffle :
            m = models.Feature.query.filter(models.Feature.id == r.id).update({"clientPriority": models.Feature.clientPriority + 1})
    db_session.add(f)
    db_session.commit()
    flash('New Feature Request Added')
    return render_template("featurerequest.html");

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
    priority = models.Feature.query.filter(models.Feature.client_id == client).count() + 1

    data = {
        'status': 'OK',
        'priority': priority,
    }
    return jsonify(data)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()