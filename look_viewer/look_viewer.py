from flask import Flask, render_template

__version__ = "0.1"
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')
