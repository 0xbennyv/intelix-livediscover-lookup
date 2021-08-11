import validators
from app.mod_utils.intelix import intelixlookup
from flask import Blueprint, request, redirect, url_for, render_template

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

@mod_web.route("lookup/ui/<ioc>")
def ui(ioc):
    if validators.ipv4(ioc) or validators.md5(ioc) or validators.sha256(ioc):
        r = intelixlookup(ioc)
        return render_template('mod_web/index.html', response=r)
    else:
        return redirect(url_for('web.index'))
    
