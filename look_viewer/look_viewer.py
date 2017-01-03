from flask import Flask, render_template, send_from_directory
import os, os.path

__version__ = "0.1"
IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), "static/img")
app = Flask(__name__, static_url_path="/static")


def _get_images(image_folder=IMAGE_FOLDER):
    filenames = os.listdir(image_folder)

    for filename in filenames:
        full_path = os.path.join(image_folder, filename)
        if os.path.isfile(full_path):
            yield filename


@app.route('/')
def main():
    filenames = list(_get_images())
    return render_template('index.html', image_collection=filenames)
