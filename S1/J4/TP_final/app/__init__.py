from flask import Flask
from config import Config
from .models import db, User
from .routes import bp as main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        # Create default admin account if not exists
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', role='admin', status='active')
            admin_user.set_password('admin')
            db.session.add(admin_user)
            db.session.commit()

    app.register_blueprint(main_bp)

    return app
