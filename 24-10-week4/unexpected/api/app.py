import os
import random

import requests
from flask import Flask, request, abort
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def check_heartbeat():
    try:
        requests.get('http://verifier:1100/heartbeat', timeout=1)
    except Exception:
        with open('/shared/reload', 'w') as f:
            f.close()
        return False
    return True


@app.route('/forwardSecret', methods=['POST'])
def forward_secret():
    secret = request.form.get('secret')

    if not secret:
        abort(400)
    elif not check_heartbeat():
        abort(429)

    is_valid = True
    try:
        resp = requests.get('http://verifier:1100/verifySecret',
                            data={'secret': secret}, timeout=5)
    except Exception:  # noqa
        pass
    else:
        if resp.status_code == 401 or not resp.json()['valid']:
            is_valid = False

    if is_valid:
        return os.environ.get('FLAG')
    return 'oOpS! you just forwarded a wrong secret'


if __name__ == '__main__':
    app.run('127.0.0.1', 7681, debug=True)
