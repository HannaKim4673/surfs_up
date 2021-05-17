# Imports flask dependency
from flask import Flask

# Creates app Flask instance
app = Flask(__name__)

# Creates Flask routes
@app.route('/')
def hello_world():
    return 'Hello world'