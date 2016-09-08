from flask import Flask, render_template, request, jsonify
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
    f = models.Feature(title, description, client, clientPriority, targetDate, url, productArea, addedby, addeddate, active, assigned)
    db_session.add(f)
    db_session.commit()
    return render_template("featurerequest.html");

@app.route('/fillclient')
def fillclient():
    client = models.Client.query.all()
    entries = [dict(client_id=c.id, clientName=c.client) for c in client]
    data = {
        'status': 'OK',
        'clients': entries
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()