import logging
import os, os.path
from random import shuffle


def iterate_subfolders(folder):
    for item in os.listdir(folder):
        full_path = os.path.join(folder, item)
        if os.path.isdir(full_path):
            yield item


def iterate_files(image_folder):
    for file_name in os.listdir(image_folder):
        full_path = os.path.join(image_folder, file_name)
        if os.path.isfile(full_path):
            yield file_name


class ImageStorage(object):
    def __init__(self, site_name, location=None):
        self.site_name = site_name
        self.location = location

    def get_types(self):
        print "=== DEBUG location: === {}".format(self.location)

        types = list(iterate_subfolders(self.location))
        return types


    def get_random_image_names(self, type_name, limit=None):
        type_folder = self._get_folder_for_type(type_name)
        image_names = list(iterate_files(type_folder))
        shuffle(image_names)
        return image_names[:limit]

    def get_random_image_paths(self, type_name, limit=None, prefix=None):
        image_names = self.get_random_image_names(type_name, limit=limit)

        prefix = prefix or os.path.join(self.site_name, type_name)
        image_paths = list(
            os.path.join(prefix, image_name)
            for image_name in image_names
        )
        return image_paths

    @classmethod
    def build_for(cls, site_name, static_image_path):
        location = os.path.join(static_image_path, site_name)
        return cls(site_name, location)

    def _get_folder_for_type(self, type_name):
        return os.path.join(self.location, type_name)


def configure_flask_logger(flask_logger):
    formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler("look_viewer.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    flask_logger.addHandler(file_handler)
    flask_logger.setLevel(logging.INFO)
