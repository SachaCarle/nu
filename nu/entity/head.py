from flask import Flask, render_template, jsonify, send_file, request
from flask_script import Manager
from pathlib import Path
import sys, os, subprocess


def serve(e):
    def _serve():
        app = Flask(__name__)

        @app.route('/')
        def body():
            return send_file(str(os.path.join(e.location, 'body.html')), mimetype='application')
        @app.route('/kill')
        def endme():
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()

        @app.route('/<path:p>')
        def index_js(p):
            return send_file(str(os.path.join(e.location, p)), mimetype='application')

        return app
    return _serve
