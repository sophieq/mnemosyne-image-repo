import os

from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
from datetime import date
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
from image_storage_service import ImageStorageService

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

@app.route('/', methods=["GET"])
@login_required
def index():
    name = current_user.first_name + "'s"
    # get previously uploaded photos
    image_sections = []
    image_objects = db.session.query(Image.date_uploaded, postgresql.array_agg(Image.path)).join(User).group_by(Image.date_uploaded).all()
    url = ImageStorageService.generate_presigned_url("blank")
    return render_template('index.html', name=name, url=url)

@app.route('/images', methods=["POST"])
@login_required
def upload_images():
    print(request.files)
    if request.files:
        images = request.files.getlist("images")
        img_objects = []

        for image in images:
            # check that images where uploaded
            if image.filename == "":
                flash('Please add photos.')
                return redirect(url_for('index'))

            try:
                ImageStorageService.upload_image(image)
            except FileNotFoundError:
                flash('Internal Error: The file was not found. Please try again later.')
                return redirect(url_for('index'))
            except NoCredentialsError:
                flash('Internal Error: Credentials not available. Please try again later.')
                return redirect(url_for('index'))

            # create database object
            img_obj = Image(
                date_uploaded=date.today(),
                path=image.filename,
                user_id=current_user.id
            )
            img_objects.append(img_obj)

        # save images into database
        db.session.bulk_save_objects(img_objects)
        db.session.commit()
        flash('Uploaded Successfully.')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
