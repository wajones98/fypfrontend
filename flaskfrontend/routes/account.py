from flask import Blueprint, request, render_template, redirect, session, url_for, flash, jsonify

import requests
import json

Account = Blueprint('account', __name__)

@Account.route('/account')
def account():
    if 'session_id' not in session:
        return redirect(url_for('auth.auth'))
    return render_template('account.html')