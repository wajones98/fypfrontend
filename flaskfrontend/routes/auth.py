from flask import Blueprint, request, render_template, redirect, session, url_for, flash
import requests

Auth = Blueprint('auth', __name__)

BASE_URL = 'http://192.168.0.22:8080'

@Auth.route('/auth')
def auth():
    if 'session_id' in session:
        return redirect(url_for('browse.browse'))
    return render_template(('auth.html'))

@Auth.route('/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        r = requests.post(
            f'{BASE_URL}/auth/login',
            json={
                'Email': request.form['email'],
                'Password': request.form['password']
            }
        )
        response = r.json()
        status = response['Status']
        if status == 500:
            flash(response['Message'])
            return redirect('/auth')
        session['session_id'] = response['Message']
        session['email'] = request.form['email']

        return redirect(url_for('browse.browse'))

@Auth.route('/auth/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.auth'))

@Auth.route('/auth/register', methods=['POST'])
def register():
    if request.method == 'POST':
        if request.form['registerPassword'] != request.form['confirmPassword']:
            flash('Passwords do not match')
            return redirect(url_for('auth.auth'))
        
        r = requests.post(
            f'{BASE_URL}/auth/register',
            json={
                'Email': request.form['registerEmail'],
                'Password': request.form['registerPassword'],
                'FirstName': request.form['registerFirstName'],
                'LastName': request.form['registerLastName']
            }
        )

        response = r.json()

        if response['Status'] != 200:
            flash(response['Message'])
        return redirect(url_for('auth.auth'))