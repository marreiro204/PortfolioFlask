import os
import logging
from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix
from extensions import db

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configure logging for debugging
    logging.basicConfig(level=logging.DEBUG)
    
    # Configuration
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Configure WTF CSRF
    app.config['WTF_CSRF_ENABLED'] = True
    
    # Database configuration - Using SQLite
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Upload configuration
    UPLOAD_FOLDER = 'static/uploads'
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Initialize extensions
    db.init_app(app)
    
    # Import and register blueprints
    from routes import main_bp
    app.register_blueprint(main_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(error):
        """Handle 404 errors"""
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        app.logger.error(f"Internal server error: {error}")
        return render_template('500.html'), 500
    
    # Create tables within app context
    with app.app_context():
        import models  # noqa: F401
        db.create_all()
    
    return app