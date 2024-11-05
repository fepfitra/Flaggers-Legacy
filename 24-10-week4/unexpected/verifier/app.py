import random

from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/heartbeat')
def heartbeat():
    return 'the server is alive'


@app.route('/verifySecret')
def verify_secret():
    secret = request.form.get('secret')
    if not secret or not secret.isdigit():
        return abort(401)
    secret = int(secret)
    if secret != random.randbytes(32):
        return {'valid': False}

    return {'valid': True}


if __name__ == '__main__':
    app.run('127.0.0.1', 1100)
