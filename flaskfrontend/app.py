from flask import Flask, render_template, redirect, url_for
from routes.auth import auth

app = Flask(__name__)
app.debug = True

app.secret_key = b'_Q\xbd\x8d\x93E_\x82\xc5\x06\xa3\x17\xdd\n(\x1c'

app.register_blueprint(auth)


@app.route('/')
def index():
    return redirect('/auth')


@app.route('/home')
def home():
    return redirect(url_for(''))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
