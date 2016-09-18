from app import app
from flask_heroku import Heroku
from flask_sqlalchemy import SQLAlchemy

if __name__ == '__main__':
    heroku = Heroku(app)
    heroku.init_app(app)
    db = SQLAlchemy(app)
    db.create_all([None])
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
