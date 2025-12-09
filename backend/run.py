import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from flask_wtf.csrf import CSRFProtect
from models import db, User, Role, Deck, Card, ReviewLog

app = Flask(__name__)
CORS(app)
csrf = CSRFProtect(app)

# Database Config
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'techrecall.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Security Config
app.config['SECRET_KEY'] = 'super-secret-key-change-prod'
app.config['SECURITY_PASSWORD_SALT'] = 'salt-change-prod'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False # Disable for dev
app.config['SECURITY_CSRF_PROTECT_MECHANISMS'] = []
app.config['SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS'] = True
app.config['WTF_CSRF_CHECK_DEFAULT'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
def create_user():
    with app.app_context():
        db.create_all()
        if not user_datastore.find_user(email="test@test.com"):
            user_datastore.create_user(email="test@test.com", password=hash_password("password"), fs_uniquifier="1", username="tester")
            db.session.commit()

@app.route('/')
def home():
    return jsonify({"message": "TechRecall API is running!", "status": "online"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/protected')
@auth_required()
def protected():
    return jsonify({"message": "You are logged in!"})

from routes import api
app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    create_user()
    app.run(debug=True, port=5000)
