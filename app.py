from dotenv import load_dotenv
import os
from datetime import date
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql

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
@login_required
def index():
    name = current_user.first_name + "'s"
    # get previously uploaded photos
    image_sections = []
    image_objects = db.session.query(Image.date_uploaded, postgresql.array_agg(Image.path)).join(User).group_by(Image.date_uploaded).all()
    for obj in image_objects:
        section = {
            "date": obj[0],
            "paths": obj[1]
        }
        image_sections.append(obj)
    return render_template('index.html', name=name, image_sections=image_sections)

@app.route('/images', methods=["POST"])
@login_required
def upload_images():
    print("got request")
    print(request.files)
    if request.files:
        images = request.files.getlist("images")
        img_objects = []
        paths = []

        for image in images:
            # check that images where uploaded
            if image.filename == "":
                flash('Please add photos.')
                return redirect(url_for('index'))

            # save image to folder and path to db
            abs_path = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
            relative_path = os.path.join(app.config["RELATIVE_PATH"], image.filename)
            image.save(abs_path)
            img_obj = Image(
                date_uploaded=date.today(),
                path=relative_path,
                user_id=current_user.id
            )
            img_objects.append(img_obj)
            paths.append(relative_path)
        db.session.bulk_save_objects(img_objects)
        db.session.commit()
        return redirect(url_for('index')

if __name__ == '__main__':
    app.run()
