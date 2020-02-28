from flask import Flask, render_template, jsonify, send_file, request
from pathlib import Path
import sys, os, subprocess

def serve(e):
    def _serve():
        app = Flask(__name__)

        @app.route('/')
        def body(p):
            return "hey"

        @app.route('/kill')
        def endme():
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()

        @app.route('/<path:p>')
        def index_js(p):
            e.think(p, Path(p).resolve())
            return send_file(str(os.path.join(e.location, p)), mimetype='application')

        return app
    return _serve
