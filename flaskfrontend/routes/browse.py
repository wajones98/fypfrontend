from flask import Blueprint, request, render_template, redirect, session, url_for, flash
from models.SearchItem import SearchItem

import requests

browse = Blueprint('browse', __name__)

search_items = []

@browse.route('/browse')
def Browse():
    if 'session_id' not in session:
        return redirect(url_for('auth.Auth'))
    search_results = SearchItem.get_search_items({})
    return render_template('browse.html', items=search_results)

