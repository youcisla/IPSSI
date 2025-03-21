from flask import Flask
import os
from config import DevelopmentConfig, ProductionConfig
from .models import db, User
from .routes import bp as main_bp

def create_app():
    app = Flask(__name__)
    # Load dynamic configuration based on FLASK_ENV
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
        
    db.init_app(app)

    with app.app_context():
        db.create_all()
        # Always update or create default admin user using the same hasher as registration
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin', role='admin', status='active')
            db.session.add(admin_user)
        # Set password using Werkzeug's generate_password_hash
        admin_user.set_password('admin')
        db.session.commit()

    app.register_blueprint(main_bp)

    return app
