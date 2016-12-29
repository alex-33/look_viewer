# look_viewer

# create and configure virtual environment
virtualenv venv_name
source venv_name/bin/activate
pip install -r requirements.txt

# install package
python setup.py install

# create web service
FLASK_APP=look_viewer/look_viewer.py python -m flask run --host=0.0.0.0

# TODO:
look_viewer --host=0.0.0.0
