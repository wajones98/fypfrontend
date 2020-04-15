from flask import Blueprint, request, render_template, redirect, session, url_for, flash
import requests

browse = Blueprint('browse', __name__)

@browse.route('/browse')
def Browse():
    if 'session_id' not in session:
        return redirect(url_for('auth.Auth'))
    return render_template(('browse.html'))