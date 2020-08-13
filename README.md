# Mnemosyne

Simple Interface to securely add and display images.

> **What's in a Name?** <br>
> Mnemosyne is the goddess of memory in greek mythology. With this tool you will be able to upload images and take a walk through memory lane.

## Features

- Authentication to see your photos
- Uploaded photos are securely added and fetched from s3 using presigned urls

## Tech Stack

- Python
- Flask
- S3
- Postgres
- CloudFront

## Next Steps

- Better adhere to the Flask Factory Model (app blueprint)
- Improve feedback with error checking
- Pagination
- More research - currently generating urls one at a time
- Seperating logic better
- Creating unit tests

## Looking Forward

- Middle of creating a link sharing
- Delete functionality
- Download functionality
