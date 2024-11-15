from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'app/uploads'

    from .analyzer import analyzer_bp
    app.register_blueprint(analyzer_bp)

    return app
