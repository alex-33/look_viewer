import os, os.path
from flask import Flask, render_template, request, send_from_directory, redirect
from util import (
    ImageStorage, configure_flask_logger,
    iterate_files, iterate_subfolders,
    parse_look_collection_from_log,
)

__version__ = "0.1"
IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), "static/img")
IMAGE_PER_TYPE = 24
app = Flask(__name__, static_url_path="/static")


@app.route("/")
def main():
    site_name = iterate_subfolders(IMAGE_FOLDER).next()
    return redirect("/{}".format(site_name))


@app.route("/<site>")
def show_image_types_for_site(site):
    if site == "favicon.ico":
        # what is the hell?
        return ""

    app.logger.debug("request site page: {}".format(site))

    site_storage = ImageStorage.build_for(site, static_image_path=IMAGE_FOLDER)
    image_types = site_storage.get_types()
    return render_template("site.html", site=site, image_types=image_types)


@app.route("/<site>/<top>/<middle>/<bottom>", methods=["GET", "POST"])
def look_generator(site, top, middle, bottom):
    username = None
    if request.method == "POST":
        username = request.form["username"]
        look_top = request.form["top"]
        look_middle = request.form["middle"]
        look_bottom = request.form["bottom"]
        app.logger.info("{}: user provided look: {} + {} + {}".format(
            username, look_top, look_middle, look_bottom
        ))

        top_images = request.form["top_images"]
        middle_images = request.form["middle_images"]
        bottom_images = request.form["bottom_images"]
        app.logger.info("user '{}' chose look ('{}','{}','{}') when shown: ({}; {}; {})".format(
            username, look_top, look_middle, look_bottom,
            top_images, middle_images, bottom_images,
        ))
        
    site_storage = ImageStorage.build_for(site, static_image_path=IMAGE_FOLDER)
    top_images = site_storage.get_random_image_paths(top, limit=IMAGE_PER_TYPE)
    middle_images = site_storage.get_random_image_paths(middle, limit=IMAGE_PER_TYPE)
    bottom_images = site_storage.get_random_image_paths(bottom, limit=IMAGE_PER_TYPE)
    return render_template(
        "look.html",
        username=username or "default_user",
        top_images=top_images, top_name=top,
        middle_images=middle_images, middle_name=middle,
        bottom_images=bottom_images, bottom_name=bottom,
    )


@app.route("/look")
def look_viewer():
    look_collection = parse_look_collection_from_log("look_viewer.log")
    return render_template("look_viewer.html", look_collection=look_collection)


if __name__ == "__main__":
    configure_flask_logger(app.logger)
    app.run(host="0.0.0.0", port=5000)
