
from flask import Flask
from config import Config
from routes import bp as routes_bp

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(routes_bp)

if __name__ == '__main__':
    app.run(debug=True)
