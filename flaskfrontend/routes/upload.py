from flask import Flask, Blueprint, request, render_template, redirect, session, url_for, flash, jsonify
from models.UploadDataset import UploadDataset
import requests
import json

Upload = Blueprint('upload', __name__)


@Upload.route('/upload')
def upload():
    if 'session_id' not in session:
        return redirect(url_for('auth.auth'))
    return render_template('upload.html')

@Upload.route('/upload/confirm', methods=['POST'])
def upload_confirm():
    if request.method == 'POST':
        if 'session_id' not in session:
            return redirect(url_for('auth.auth'))
        files = request.files.getlist("files")
        metadata = {
            	"SignalType": request.form['signalType'],
                "Species": request.form['species'],
                "Gender": request.form['gender'],
                "Age": request.form['age'],
                "Target": request.form['target'],
                "Action": request.form['action'],
                "DataSetName": request.form['dataset'],
                "ChannelCount":request.form['channelCount'],
                "Device":request.form['device'],
                "Tags": json.loads(request.form['tagData'])
        }
        upload = UploadDataset(files, metadata)
        upload.upload()
    return redirect(url_for('upload.upload'))

@Upload.route('/upload/projects/file', methods=['POST'])
def upload_projects_file():
    if request.method == 'POST':
        if 'session_id' not in session:
            return redirect(url_for('auth.auth'))
        info = {
            'Change': request.form['change'],
            'Filepath': request.form['action']
        }
        file = request.files
        upload = UploadDataset(file, info)
        response = upload.upload_change()
        flash(response['Message'])
    return redirect(url_for('projects.projects'))