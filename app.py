from dotenv import load_dotenv
import os
from datetime import date
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from models import Image

def get_response(status, code, message):
    return jsonify({"{}".format(status): "{}".format(code), "message": "{}".format(message)}), code

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/images', methods=["POST"])
def upload_images():
    if request.files:
        images = request.files.getlist("images")

        if not images:
            return render_template('index.html')

        img_objects = []
        paths = []

        for image in images:
            # save image to folder and path to db
            abs_path = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
            relative_path = os.path.join(app.config["RELATIVE_PATH"], image.filename)
            image.save(abs_path)
            img_obj = Image(
                date_uploaded=date.today(),
                path=relative_path
            )
            img_objects.append(img_obj)
            paths.append(relative_path)
        db.session.bulk_save_objects(img_objects)
        db.session.commit()
        return redirect(url_for('index', image_paths=paths))

if __name__ == '__main__':
    app.run()
