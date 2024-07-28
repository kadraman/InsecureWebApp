import functools
import os

from flask import Blueprint, make_response
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from jinja2 import Template as Jinja2_Template
from jinja2 import Environment, DictLoader

bp = Blueprint("insecure", __name__, url_prefix="/insecure")

INITCMD="setup.bat"

"""
Some additional insecure examples not related to the functionality of the application.
"""

@bp.route("/xss", methods=("GET", "POST"))
def xss():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    if request.method == "GET":
        username = request.args.get('username')    
        password = request.args.get('password')    

    return "username: %s; password: %s" % username, password

@bp.route("/load_file", methods = ["GET"])
def load_file():
    filename = request.args.get('filename') 
    contents = source(filename)
    response = make_response(contents, 200)
    response.mimetype = "text/plain"
    return response

@bp.route("/command_injection", methods = ["GET"])
def command_injection():
    home = os.getenv('APPHOME')
    cmd = home.join(INITCMD)
    os.system(cmd);
    
@bp.route("/template_with_filedata", methods=['POST'])
def process_request(request):
    # Load the template
    template = request.GET['template']
    t = Jinja2_Template(template)
    name = source(request.GET['name'])
    # Render the template with the context data
    html = t.render(name=name)
    return html

def robotstxt():
    resp = make_response('')
    resp.headers.set('content-type', 'text/plain')
    return resp
    
"""
@bp.route("/template", methods=['POST'])
def process_request():
    # Load the template
    template = request.form['template']
    t = Jinja2_Template(template)
    name = source(request.form['name'])
    # Render the template with the context data
    html = t.render(name=name)
    return html
"""

def source(script_path):
    with open(script_path, 'r') as script_file:
        script_contents = script_file.read()
        exec(script_contents)
