import logging
import os, os.path
from collections import namedtuple
from random import shuffle

logger = logging.getLogger(__name__)
LookItem = namedtuple("LookItem", ["username", "top", "middle", "bottom"])


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
        logger.debug("location: === {}".format(self.location))

        types = sorted(list(iterate_subfolders(self.location)))
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
    # TODO: use jsonlines for better parsing
    formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler("look_viewer.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    flask_logger.addHandler(file_handler)
    flask_logger.setLevel(logging.INFO)


class LookLogParser(object):
    look_pattern = "user provided look:"

    def contain_look(self, log_line):
        if self.look_pattern not in log_line:
            return False

        look_items = log_line.split(self.look_pattern)[-1].split("+")
        if len(look_items) != 3:
            return False

        return True

    def parse(self, log_line):
        user_info, look_info = log_line.split(self.look_pattern)
        username = self._parse_username(user_info)
        top, middle, bottom = look_info.split("+")
        return LookItem(
            username=username, top=top.strip(),
            middle=middle.strip(), bottom=bottom.strip()
        )

    def _parse_username(self, user_info):
        username = user_info.strip().split()[-1]
        username = username.replace(":", "")
        return username


def parse_look_collection_from_log(log_file_path):
    look_log_parser = LookLogParser()
    with open(log_file_path) as fin:
        for line in fin:
            if look_log_parser.contain_look(line):
                look = look_log_parser.parse(line)
                yield look
