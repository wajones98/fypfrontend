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
    invitations = Project.get_users_invitations()
    return render_template('projects.html', projects=projects, invitations=invitations)

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

        response = Project.create_project(json_body)
        flash(response['Message'])
    return redirect(url_for('projects.projects'))

@Projects.route('/projects/invite', methods=['POST'])
def projects_invite():
    if request.method == 'POST':
        if 'session_id' not in session:
            return redirect(url_for('auth.auth'))
        json_body = {
            "Email": request.form['projectEmail'],
            "ProjectId": request.form['action']
        }
        response = Project.invite_project(json_body)
        flash(response['Message'])
    return redirect(url_for('projects.projects'))

@Projects.route('/projects/leave', methods=['POST'])
def projects_leave():
    if request.method == 'POST':
        if 'session_id' not in session:
            return redirect(url_for('auth.auth'))
        json_body = {
            "ProjectId": request.form['action']
        }
        response = Project.leave_project(json_body)
        flash(response['Message']) 
    return redirect(url_for('projects.projects'))      

@Projects.route('/projects/mode', methods=['POST'])
def projects_make_public_or_private():
    if request.method == 'POST':
        if 'session_id' not in session:
            return redirect(url_for('auth.auth'))
        json_body = {
            "ProjectId": request.form['action'],
            "Mode": request.form['val']
        }
        response = Project.make_public(json_body)
        flash(response['Message']) 
    return redirect(url_for('projects.projects'))     
        