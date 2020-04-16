from flask import Blueprint, request, render_template, redirect, session, url_for, flash, jsonify
from models.SearchItem import SearchItem

import requests
import json

browse = Blueprint('browse', __name__)

search_items = []

BASE_URL = 'http://192.168.0.22:8080'


@browse.route('/browse')
def Browse():
    if 'session_id' not in session:
        return redirect(url_for('auth.Auth'))
    search_results = SearchItem.get_search_items({})
    return render_template('browse.html', items=search_results)

@browse.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        if 'session_id' not in session:
            return redirect(url_for('auth.Auth'))
        json_query = json.loads(request.form['jsonQuery'])
        print(json_query)
        search_results = SearchItem.get_search_items(json_query)
        return render_template('browse.html', items=search_results)