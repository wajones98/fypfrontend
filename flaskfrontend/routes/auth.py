from flask import Blueprint, request, render_template, redirect, session, url_for, flash

auth = Blueprint('auth', __name__)


@auth.route('/auth')
def Auth():
    return render_template(('auth.html'))