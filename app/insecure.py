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

@bp.route("/xss", methods = ["POST"])
def xss():
    if (os.environ.get('FORTIFY_IF_DJANGO')):
        content = request.POST['content', '']
    else:    
        content = request.form.get('content') 
    return render_template("insecure/xss.html", content=content)

@bp.route("/load_file", methods = ["GET"])
def load_file():
    if (os.environ.get('FORTIFY_IF_DJANGO')):
        filename = filename.GET['content', '']
    else:    
        filename = request.args.get('filename') 
    contents = source(filename)
    response = make_response(contents, 200)
    response.mimetype = "text/plain"
    return response

@bp.route("/command_injection", methods = ["GET"])
def command_injection():
    if (os.environ.get('FORTIFY_IF_DJANGO')):
        arguments = request.GET['arguments', '']
    else:    
        arguments = request.args.get('arguments') 
    home = os.getenv('APPHOME')
    cmd = home.join(INITCMD).join(arguments)
    os.system(cmd);
    
@bp.route("/template_injection", methods=['POST'])
def template_injection():
    if (os.environ.get('FORTIFY_IF_DJANGO')):
        template = request.POST['content', '']
        filename = request.POST['content', '']
    else:    
        template = request.form.get('template') 
        filename = request.form.get('filename') 
    t = Jinja2_Template(template)
    name = source(filename)
    html = t.render(name=name)
    return html

@bp.route("/set_headers")
def set_headers():
    resp = make_response('')
    resp.headers.set("Access-Control-Allow-Origin", "*")
    resp.headers.set('content-type', 'text/plain')
    return resp
    

def source(script_path):
    with open(script_path, 'r') as script_file:
        script_contents = script_file.read()
        exec(script_contents)
