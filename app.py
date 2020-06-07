from dotenv import load_dotenv
import os
from datetime import date
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

# app set up
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from models import Image, User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# TODO: splash screen
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/profile', methods=["GET"])
@login_required
def profile():
    name = current_user.first_name + "'s"
    return render_template('index.html', name=name)

@app.route('/images', methods=["POST"])
def upload_images():
    if request.files:
        images = request.files.getlist("images")

        if not images:
            return redirect('index')

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
