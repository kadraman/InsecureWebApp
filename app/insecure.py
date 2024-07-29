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

@bp.route("/xss", methods = ["GET"])
def xss():
    if (os.environ.get('FORTIFY_IF_DJANGO')):
        input = request.GET['input', '']
    else:    
        user_input = request.args.get('input') 
    return render_template("insecure/xss.html", input=user_input)

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

@bp.route("/insecure_headers", methods=['POST'])
def insecure_headers():
    response = make_response('')
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@bp.route("/insecure_cookies", methods=['POST'])
def insecure_cookies():
    if (os.environ.get('FORTIFY_IF_DJANGO')):
        email = request.POST['email', '']
    else:    
        email = request.form.get('email') 
    response = make_response('')
    response.set_cookie("emailCookie", email)
    return response   

def source(script_path):
    with open(script_path, 'r') as script_file:
        script_contents = script_file.read()
        exec(script_contents)
