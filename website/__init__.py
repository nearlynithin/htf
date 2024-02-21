from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from os import path
from flask_login import LoginManager

# Create a SQLAlchemy database instance
db = SQLAlchemy()
DB_NAME = 'database.db'

# Initialize SocketIO
sio = SocketIO()

# Function to create the Flask app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'YourSecretKeyHere'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Initialize SQLAlchemy database with the app
    db.init_app(app)

    # Initialize SocketIO with the app
    sio.init_app(app)

    # Import blueprints and models
    from .views import views
    from .auth import auth
    from .complaint import complaint

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(complaint, url_prefix='/')

    # Import models
    from .models import Citizen, Complaint

    # Create the database tables
    with app.app_context():
        db.create_all()

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Load a user from the user ID
    @login_manager.user_loader
    def load_user(id):
        return Citizen.query.get(id)

    return app

# Function to run the Flask app
if __name__ == '__main__':
    app = create_app()
    sio.run(app, debug=True)
