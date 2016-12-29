from setuptools import setup, find_packages
from look_viewer import look_viewer

setup(
    name='look_viewer',
    version=look_viewer.__version__,
    packages=find_packages(),
    package_data={'': ['*.dict', '*.list', 'hjudge.conf.default']},
    install_requires=['python (>= 2.7)'],
    description='Look Viewer to collect human feedback',
    license='Apache License v2.0',
    entry_points={'console_scripts': ['look_viewer = look_viewer.look_viewer:main']},
    platforms=["Linux"],
)
