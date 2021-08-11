import validators
from app.mod_utils.intelix import intelixlookup
from flask import Blueprint, render_template, request, redirect, url_for

mod_web = Blueprint('web', __name__, url_prefix='/')
@mod_web.route("/")
def index():
    return f"<p> Setup Sophos Live discover to point to {request.base_url}lookup/ioc </p>"

@mod_web.route("lookup/")
def lookup():
    return redirect(url_for('web.index'))

@mod_web.route("lookup/<ioc>")
def ioc(ioc):
    if validators.ipv4(ioc) or validators.md5(ioc) or validators.sha256(ioc):
        r = intelixlookup(ioc)
        return r
    else:
        return redirect(url_for('web.index'))
