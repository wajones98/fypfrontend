from flask import Blueprint, request, render_template, redirect, session, url_for, flash, jsonify

import requests
import json

Projects = Blueprint('projects', __name__)

@Projects.route('/projects')
def projects():
    if 'session_id' not in session:
        return redirect(url_for('auth.auth'))
    return render_template('projects.html')