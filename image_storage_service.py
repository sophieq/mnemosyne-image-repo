import boto3
import os
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
from botocore.signers import CloudFrontSigner
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from werkzeug.utils import secure_filename
from utils import month_dictionary
import tempfile

class ImageStorageService():
    @staticmethod
    def get_user_images(objects):
        image_sections = []
        for obj in objects:
            urls = []
            for path in obj[1]:
                url = ImageStorageService.generate_presigned_url(path)
                urls.append(url)
            image_section = {
                "date": month_dictionary[obj[0].month] + " " + str(obj[0].year),
                "urls": urls
            }
            image_sections.append(image_section)
        return image_sections

    @staticmethod
    def upload_image(image):
        # save image to folder and path to db
        from app import app
        filename = secure_filename(image.filename)
        path = os.path.join(tempfile.gettempdir(), filename)
        # path = os.path.abspath(relative_path)

        # save to temp file for now
        image.save(path)
        # save to s3
        s3 = boto3.client('s3')
        ExtraArgs = {
            'ContentType': image.content_type
        }

        try:
            s3.upload_file(
                path,
                app.config["BUCKET"],
                filename,
                ExtraArgs=ExtraArgs
            )
        except Exception as err:
            raise err

    @staticmethod
    def generate_presigned_url(filename):
        expire_date = datetime.utcnow() + timedelta(days=7) # expires in 2 days
        bucket_resource_url = filename
        url = ImageStorageService.create_cloudfront_signed_url(
            bucket_resource_url,
            expire_date
        )
        return url

    @staticmethod
    def create_cloudfront_signed_url(object_name, expiration_date):
        from app import app

        key_id = app.config['CF_ID']
        url = app.config['CF_DOMAIN'] + object_name

        cloudfront_signer = CloudFrontSigner(key_id, ImageStorageService.rsa_signer)
        signed_url = cloudfront_signer.generate_presigned_url(url, date_less_than=expiration_date)

        return signed_url

    # source: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html#generate-a-signed-url-for-amazon-cloudfront
    @staticmethod
    def rsa_signer(message: str) -> str:
        from app import app

        with open(app.config['CF_KEY'], 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())
