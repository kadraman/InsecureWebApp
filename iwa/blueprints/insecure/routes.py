"""
        InsecureWebApp - an insecure Python/Flask Web application

        Copyright (C) 2024-2025  Kevin A. Lee (kadraman)

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging
import os

from flask import make_response, render_template_string
from flask import render_template
from flask import request

from jinja2 import Template as Jinja2_Template

from iwa.blueprints.insecure import insecure_bp


logger = logging.getLogger(__name__)

INITCMD = "setup.bat"


"""
Some additional insecure examples not related to the functionality of the application.
"""

@insecure_bp.route("/xss1", methods = ["GET"])
def xss1():   
    user_input = request.args.get('input') 
    return render_template("insecure/xss.jinja", input=user_input)


@insecure_bp.route("/xss2", methods = ["GET"])
def xss2():   
    user_input = request.args.get('input') 
    return render_template_string("<div><h1>XSS Example</h1><p>User Input: %s</p></div>" % user_input)


@insecure_bp.route("/load_file", methods = ["GET"])
def load_file(): 
    filename = request.args.get('filename') 
    contents = source(filename)
    response = make_response(contents, 200)
    response.mimetype = "text/plain"
    return response


@insecure_bp.route("/command_injection", methods = ["GET"])
def command_injection():   
    arguments = request.args.get('arguments') 
    home = os.getenv('APPHOME')
    logger.debug("Using home directory: {home}")
    cmd = home.join(INITCMD).join(arguments)
    os.system(cmd);
    

@insecure_bp.route("/template_injection", methods=['POST'])
def template_injection():
    template = request.form.get('template') 
    filename = request.form.get('filename') 
    t = Jinja2_Template(template)
    name = source(filename)
    html = t.render(name=name)
    return html


@insecure_bp.route("/insecure_headers", methods=['POST'])
def insecure_headers():
    response = make_response('')
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@insecure_bp.route("/insecure_cookies", methods=['POST'])
def insecure_cookies():
    email = request.form.get('email') 
    response = make_response('')
    response.set_cookie("emailCookie", email)
    return response   


def source(script_path):
    with open(script_path, 'r') as script_file:
        script_contents = script_file.read()
        exec(script_contents)
