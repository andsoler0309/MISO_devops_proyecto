import os
import time
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from views import *
from models import db
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_SECRET_KEY"] = "frase-secreta"


app_context = app.app_context()
app_context.push()

db.init_app(app)
max_retires = 5
retry_interval = 1
for retry in range(max_retires):
    try:
        with app.app_context():
            db.create_all()
        break
    except OperationalError as e:
        if retry < max_retires - 1:
            print(f"Database connection failed. Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
            continue
        else:
            raise e

cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)
api.add_resource(ViewCreateBlacklist, '/blacklists')
api.add_resource(ViewGetBlacklist, '/blacklists/<string:email>')
api.add_resource(ViewHealthCheck, '/blacklists/ping')
api.add_resource(ResetDatabase, '/blacklists/reset')

jwt = JWTManager(app)

if __name__ == "__main__":
    PORT = os.environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=PORT, debug=True)
