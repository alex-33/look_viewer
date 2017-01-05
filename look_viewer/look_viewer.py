import os, os.path
from flask import Flask, render_template, send_from_directory
from util import ImageStorage, iterate_files

__version__ = "0.1"
IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), "static/img")
app = Flask(__name__, static_url_path="/static")


@app.route("/")
def main():
    lamoda_storage = ImageStorage.build_for(site_name="lamoda", static_image_path=IMAGE_FOLDER)
    shoe_images = lamoda_storage.get_random_image_paths("shoes")
    return render_template("index.html", image_collection=shoe_images)


@app.route("/<site>")
def show_image_types_for_site(site):
    site_storage = ImageStorage.build_for(site, static_image_path=IMAGE_FOLDER)
    image_types = site_storage.get_types()
    return render_template("site.html", image_types=image_types)

@app.route("/<site>/<top>/<bottom>")
def look_generator(site, top, bottom):
    site_storage = ImageStorage.build_for(site, static_image_path=IMAGE_FOLDER)
    top_images = site_storage.get_random_image_paths(top)
    bottom_images = site_storage.get_random_image_paths(bottom)
    return render_template("look.html", top_images=top_images, bottom_images=bottom_images)
