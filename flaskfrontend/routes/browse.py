from flask import Blueprint, request, render_template, redirect, session, url_for, flash, jsonify
from models.SearchItem import SearchItem
from models.Project import Project

import requests
import json

Browse = Blueprint('browse', __name__)

search_items = []

BASE_URL = 'http://192.168.0.22:8080'


@Browse.route('/browse')
def browse():
    if 'session_id' not in session:
        return redirect(url_for('auth.auth'))
    search_results = SearchItem.get_search_items({'Parameters': {"ProjectName": 'none'}})
    projects = Project.get_users_projects()  
    return render_template('browse.html', items=search_results, projects=projects, session=session['session_id'])

@Browse.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        if 'session_id' not in session:
            return redirect(url_for('auth.auth'))
        json_query = json.loads(request.form['jsonQuery'])
        search_results = SearchItem.get_search_items(json_query)
        return render_template('browse.html', items=search_results)


@Browse.route('/download/file', methods=['POST'])
def download_file():
    if request.method == 'POST':
        if 'session_id' not in session:
            return redirect(url_for('auth.auth'))
        file_info = {'filePath': request.form['action'], 
                    'fileName': request.form['fileName'],
                    'dataset': request.form['dataset']}
        return SearchItem.download_file(file_info)
    return redirect(url_for('browse.browse'))

@Browse.route('/download/dataset', methods=['POST'])
def download_dataset():
    if request.method == 'POST':
        if 'session_id' not in session:
            return redirect(url_for('auth.auth'))
        dataset_info = {'dataset': request.form['datasetName'],
                        'fileInfo': session[request.form['datasetId']]}   
        return SearchItem.download_dataset(dataset_info)
    return redirect(url_for('browse.browse'))