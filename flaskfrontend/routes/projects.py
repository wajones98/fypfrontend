from flask import Blueprint, request, render_template, redirect, session, url_for, flash, jsonify
from models.Project import Project

import requests
import json

Projects = Blueprint('projects', __name__)

@Projects.route('/projects')
def projects():
    if 'session_id' not in session:
        return redirect(url_for('auth.auth'))
    projects = Project.get_users_projects()
    return render_template('projects.html', projects=projects)

@Projects.route('/projects/create', methods=['POST'])
def projects_create():
    if request.method == 'POST':
        if 'session_id' not in session:
            return redirect(url_for('auth.auth'))
        
        if 'public' in request.form:
            public = 1
        else:
            public = 0

        json_body = {
            "Name": request.form['projectName'],
            "Desc": request.form['projectDesc'],
            "Public": public
        }

        Project.create_project(json_body)

    return redirect(url_for('projects.projects'))