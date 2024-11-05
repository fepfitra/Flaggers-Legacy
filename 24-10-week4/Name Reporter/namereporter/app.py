#!/usr/bin/python3

from flask import Flask, render_template, request, render_template_string, redirect, url_for, abort, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["50000 per hour"],
    storage_uri="memory://",
)

@app.route('/', methods=['GET'])
@limiter.limit("2 per second")
def index():
	return render_template('index.html')

@app.route('/about', methods=['GET'])
@limiter.limit("2 per second")
def about():
	return render_template('about.html')

@app.route('/report', methods=['GET', 'POST'])
@limiter.limit("2 per second")
def report():
    if request.method == 'POST':
        name = request.form["name"]
        return redirect(url_for("report", name=name))
    elif request.method == 'GET':
        message = "Thanks for submitting the name. We'll give surveillance."
        name = request.args.get("name", None)
        header = "{% include 'header.html' %}"
        footer = "{% include 'footer.html' %}"
        if len(name) > 130:
            message = "That's too long"
            name = "Write the name with a reasonable number of letters"
        if any(i in name for i in ['|join','[',']', 'mro', 'base', "'", '#', '&', '_']):
            message = "Malcious character detected!"
            name = "Don't try to hack this site, it is used for good"
        html_string = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Name Reporter</title>
                <link rel="stylesheet" type="text/css" href="static/css/congrats.css">
            </head>
            <body>
                <!-- /source to look how it works -->
                {header}
                <div id="message-parent">
                <h1>{message}</h1>
                <p>{name}</p>
                </div>
                {footer}
            </body>
            </html>
        '''
        return render_template_string(html_string)
    else:
        return abort(404)

@app.route('/source', methods=['GET'])
@limiter.limit("2 per second")
def source():
    return Response(open(__file__).read(), mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)